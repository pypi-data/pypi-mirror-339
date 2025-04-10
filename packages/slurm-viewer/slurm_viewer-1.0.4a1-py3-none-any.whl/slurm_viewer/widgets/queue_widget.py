from __future__ import annotations

import csv
import datetime
from io import StringIO
from pathlib import Path
from typing import Any

from loguru import logger
from rich.text import Text
from textual import work, on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, Horizontal, ScrollableContainer
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Static, Label, Button, Checkbox, Switch
from textual.widgets.data_table import RowKey
from textual_sortable_datatable import SortableDataTable

from slurm_viewer.data.config import Config
from slurm_viewer.data.models import SlurmError
from slurm_viewer.data.queue_model import JobStateCodes, Queue
from slurm_viewer.data.slurm_communication import SlurmPermissionDenied
from slurm_viewer.data.slurm_protocol import SlurmProtocol
from slurm_viewer.widgets.loading import Loading
from slurm_viewer.widgets.screens.detail_screen import DetailScreen
from slurm_viewer.widgets.screens.select_columns_screen import SelectColumnsScreen
from slurm_viewer.widgets.widget_types import AutoUpdate


def sort_column(value: Any) -> Any:
    if value is None:
        return ''

    if isinstance(value, Text):
        value = value.plain

    if isinstance(value, datetime.datetime):
        value = value.timestamp()

    if isinstance(value, datetime.timedelta):
        value = value.total_seconds()

    if isinstance(value, str):
        if value.endswith(' GB'):
            return float(value[:-len(' GB')])
        if value == '-':
            return 0

    try:
        return float(value)
    except ValueError:
        pass

    return value


class QueueWidget(Static):
    CSS_PATH = Path(__file__) / 'slurm_viewer.tcss'

    BINDINGS = [
        Binding('c', 'columns', 'Select Columns'),
        Binding('d', 'details', 'Details'),
        Binding('shift+left', 'move_left', 'Column Left', show=False),
        Binding('shift+right', 'move_right', 'Column Right', show=False)
    ]

    config: reactive[Config] = reactive(Config, layout=True, always_update=True)

    def __init__(self, _slurm: SlurmProtocol, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.slurm = _slurm
        self.queue_info: list[Queue] = []
        self._map_running: dict[RowKey, Queue] = {}
        self._map_pending: dict[RowKey, Queue] = {}

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal(id='queue_horizontal'):
                yield Static(id='horizontal_spacer')
                yield Label(id='queue_label')
                yield Button(label='Refresh', id='queue_refresh')
                yield Label(f'Auto refresh ({self.config.ui.refresh_interval} s)', id='queue_auto_refresh')
                yield Switch(name='auto_refresh', id='queue_auto_refresh_switch', value=False)
            with ScrollableContainer(id='queue_scrollable_container'):
                table = SortableDataTable(id='queue_running_table')
                table.sort_function = sort_column
                yield table
                table = SortableDataTable(id='queue_pending_table')
                table.sort_function = sort_column
                yield table

    @work(name='queue_widget_watch_config')
    async def watch_config(self, _: Config, __: Config) -> None:
        try:
            self.query_one('#queue_scrollable_container', ScrollableContainer)
        except NoMatches:
            return

        self.query_one('#queue_auto_refresh', Label).update(f'Auto refresh ({self.config.ui.refresh_interval} s)')
        self.query_one('#queue_auto_refresh_switch', Switch).value = self.config.ui.auto_refresh
        self.query_one('#queue_refresh', Button).display = not self.config.ui.auto_refresh

        with Loading(self):
            await self.timer_update()

    def copy_to_clipboard(self) -> None:
        with StringIO() as fp:
            fieldnames = list(self.queue_info[0].model_dump().keys())
            writer = csv.DictWriter(fp, fieldnames=fieldnames)
            writer.writeheader()
            for node in self.queue_info:
                writer.writerow(node.model_dump())

        # noinspection PyUnresolvedReferences
        self.app.copy_to_clipboard(fp.getvalue())
        self.app.notify('Copied queues to clipboard')

    async def timer_update(self) -> None:
        try:
            last_update_time = datetime.datetime.now().strftime('%A %H:%M:%S')
            self.queue_info = await self.slurm.queue(self.config.ui.user_only)
            self.query_one('#queue_label', Label).update(f'Last update: {last_update_time}')
            await self._update_table()
        except SlurmPermissionDenied as e:
            self.app.notify(message=str(e), title='Permission Denied!', severity='error', timeout=20)
        except SlurmError as e:
            cluster_name = self.slurm.cluster().name
            logger.error(f'Cluster: "{cluster_name}", {e.func}')
            self.app.notify(title=f'[squeue] Error retrieving data from cluster "{cluster_name}"',
                            message='Could not retrieve data from the cluster\n'
                                    f'See {(Path.cwd() / "slurm_viewer.log").absolute()} for more information',
                            severity='error', timeout=15)

    async def _update_table(self) -> None:
        if not self.is_mounted:
            return

        table = self.query_one('#queue_running_table', SortableDataTable)

        # it appears that the selected partitions is not always honored in the squeue output so add another filter here.
        jobs = [x for x in self.queue_info if
                (JobStateCodes.RUNNING in x.states and x.partition in self.slurm.cluster().partitions)]
        table.border_title = f'Running Jobs ({len(jobs)} for {"user" if self.config.ui.user_only else "all users"})'
        self._queue_data_table(jobs, table, self._map_running)

        table = self.query_one('#queue_pending_table', SortableDataTable)

        jobs = [x for x in self.queue_info if
                (JobStateCodes.PENDING in x.states and x.partition in self.slurm.cluster().partitions)]
        table.border_title = f'Pending Jobs ({len(jobs)}) for {"user" if self.config.ui.user_only else "all users"}'
        self._queue_data_table(jobs, table, self._map_pending)

        self.query_one('#queue_label', Label).update(f'Last update: {datetime.datetime.now().strftime("%H:%M:%S")}')

    def _queue_data_table(self, queue: list[Queue], data_table: SortableDataTable, _map: dict[RowKey, Queue]) -> None:
        _map.clear()
        data_table.cursor_type = 'row'
        data_table.clear(columns=True)
        data_table.zebra_stripes = True
        data_table.add_columns(*self.config.ui.queue_columns)

        for row in queue:
            data = [getattr(row, key) for key in self.config.ui.queue_columns]
            row_key = data_table.add_row(*data)
            _map[row_key] = row

    @work(name='queue_widget_refresh_info')
    @on(Button.Pressed, '#queue_refresh')
    async def refresh_info(self, _: Checkbox.Changed) -> None:
        await self._update_table()

    @on(Switch.Changed, '#queue_auto_refresh_switch')
    def on_auto_refresh(self, event: Switch.Changed) -> None:
        self.post_message(AutoUpdate.Changed(event.control.value))

    def action_details(self) -> None:
        data_table = self.query_one('#queue_running_table', SortableDataTable)
        selected = data_table.coordinate_to_cell_key(data_table.cursor_coordinate).row_key
        item = self._map_running[selected]

        if not data_table.has_focus:
            data_table = self.query_one('#queue_pending_table', SortableDataTable)
            selected = data_table.coordinate_to_cell_key(data_table.cursor_coordinate).row_key
            item = self._map_pending[selected]

        self.app.push_screen(DetailScreen(item))

    async def action_columns(self) -> None:
        async def check_result(selected: list[str] | None) -> None:
            if selected is None:
                return

            self.config.ui.queue_columns = selected
            await self._update_table()

        current_columns = [x.label.plain for x in self.query_one('#queue_running_table', SortableDataTable).column_names()]
        # noinspection PyUnresolvedReferences
        all_columns = list(Queue.model_fields.keys())
        all_columns.extend([name for name, value in vars(Queue).items() if isinstance(value, property)])
        remaining_columns = sorted(set(all_columns) - set(current_columns))

        await self.app.push_screen(SelectColumnsScreen(current_columns, remaining_columns), check_result)

    async def action_move_left(self) -> None:
        tables = self.query(SortableDataTable)
        focus_table = None
        for table in tables:
            if table.has_focus:
                focus_table = table
                break

        if focus_table is None:
            return

        self.config.ui.queue_columns.insert(
            focus_table.cursor_column - 1,
            self.config.ui.queue_columns.pop(focus_table.cursor_column)
        )
        old_pos = focus_table.cursor_coordinate

        await self._update_table()

        for table in tables:
            table.cursor_coordinate = old_pos.left()

    async def action_move_right(self) -> None:
        tables = self.query(SortableDataTable)
        focus_table = None
        for table in tables:
            if table.has_focus:
                focus_table = table
                break

        if focus_table is None:
            return

        self.config.ui.queue_columns.insert(
            focus_table.cursor_column + 1,
            self.config.ui.queue_columns.pop(focus_table.cursor_column)
        )
        old_pos = focus_table.cursor_coordinate

        await self._update_table()

        for table in tables:
            table.cursor_coordinate = old_pos.right()

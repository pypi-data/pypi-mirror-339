from __future__ import annotations

import asyncio
import datetime
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from loguru import logger
from rich.text import Text
from textual import on, work
from textual.app import ComposeResult
from textual.containers import ScrollableContainer, Vertical
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Checkbox, Markdown, Static, TabPane, TabbedContent
from textual_sortable_datatable import SortableDataTable

from slurm_viewer.data.config import Config
from slurm_viewer.data.models import SlurmError
from slurm_viewer.data.node_model import Node, State
from slurm_viewer.data.partitions_model import PartitionInfo, condense_string_list
from slurm_viewer.data.queue_model import JobStateCodes, Queue
from slurm_viewer.data.slurm_communication import SlurmPermissionDenied
from slurm_viewer.data.slurm_protocol import SlurmProtocol
from slurm_viewer.widgets.loading import Loading


@dataclass
class UserInfo:
    running: int = 0
    queued: int = 0
    errors: int = 0
    cpus: int = 0
    gpus: int = 0
    account: str = ''

    def add_job(self, _job: Queue) -> None:
        if _job.account is not None:
            self.account = _job.account

        if JobStateCodes.RUNNING in _job.states:
            self.running += 1

        if JobStateCodes.PENDING in _job.states:
            self.queued += 1

        if JobStateCodes.FAILED in _job.states:
            self.errors += 1

        for gpu in _job.gres_detail:
            self.gpus += gpu.amount

        if _job.cpus is not None:
            if isinstance(_job.cpus, int):
                self.cpus += _job.cpus
            else:
                self.cpus += _job.cpus.number


class StatusWidget(Static):
    CSS_PATH = Path(__file__) / 'slurm_viewer.tcss'

    config: reactive[Config] = reactive(Config, layout=True, always_update=True)

    def __init__(self, _slurm: SlurmProtocol, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.slurm = _slurm
        self.cluster_info: list[Node] = []
        self.queue_info: list[Queue] = []

    def compose(self) -> ComposeResult:
        with Vertical():
            # with Horizontal():
            #     yield Static(id='horizontal_spacer')
            #     yield Label(id='status_label')
            #     yield Button(label='Refresh', id='status_refresh')
            with ScrollableContainer(id='status_scrollable_container'):
                with TabbedContent(id='cluster_tab'):
                    with TabPane('Resource Information'):
                        yield Markdown(id='resource_md')
                    with TabPane('Partition Information'):
                        yield SortableDataTable(id='partition_table')
                    with TabPane('User Information'):
                        yield SortableDataTable(id='user_table')

    @work(name='status_widget_watch_config')
    async def watch_config(self, _: Config, __: Config) -> None:
        try:
            widget: Widget = self.query_one('#status_scrollable_container', ScrollableContainer)
        except NoMatches:
            return

        with Loading(widget):
            await self.timer_update()

    @work(name='status_widget_refresh_info')
    @on(Button.Pressed, '#status_refresh')
    async def refresh_info(self, _: Checkbox.Changed) -> None:
        await self.timer_update()

    async def timer_update(self) -> None:
        try:
            self.cluster_info = await self.slurm.nodes()
            self.queue_info = await self.slurm.queue(user_only=False)
            self.border_title = f'Last update: {datetime.datetime.now().strftime("%A %H:%M:%S")}'
            await asyncio.gather(self.update_resource_info(), self.update_user_info(), self.update_partition_info())
        except SlurmPermissionDenied as e:
            self.app.notify(message=str(e), title='Permission Denied!', severity='error', timeout=20)
        except SlurmError as e:
            cluster_name = self.slurm.cluster().name
            logger.error(f'{cluster_name}, {e.func}')
            self.app.notify(title=f'[scontrol/squeue] Error retrieving data from cluster "{cluster_name}"',
                            message='Could not retrieve data from the cluster\n'
                                    f'See {(Path.cwd() / "slurm_viewer.log").absolute()} for more information',
                            severity='error', timeout=15)

    async def update_resource_info(self) -> None:
        with Loading(self):
            data: defaultdict[str, UserInfo] = defaultdict(UserInfo)
            for job in self.queue_info:
                data[job.user].add_job(job)

            running = pending = failed = 0
            for user in data:
                running += data[user].running
                pending += data[user].queued
                failed += data[user].errors

            # noinspection PyTypeChecker
            gpu_nodes = [x for x in self.cluster_info if x.gpu_tot > 0]  # type: ignore
            exe_nodes = [x for x in self.cluster_info if x.gpu_tot == 0]

            gpu_alloc = sum(x.gpu_alloc for x in self.cluster_info)  # type: ignore
            gpu_avail = sum(y.gpu_avail for y in self.cluster_info)  # type: ignore
            gpu_tot = sum(y.gpu_tot for y in self.cluster_info)  # type: ignore
            cpu_avail = sum(x.cpu_avail for x in self.cluster_info)  # type: ignore

            md = [
                '### Job Information',
                '|Job Status|#|',
                '|--|--|',
                f'|Running|`{running:>6d}`|',
                f'|Pending|`{pending:>6d}`|',
                f'|Failed|`{failed:>6d}`|',
                '### Resource Information',
                f' SLURM version: {await self.slurm.slurm_version()}',
                '\n\n',
                'Nodes:',
                f'- Total nodes: {len(self.cluster_info)}',
                f'- EXE nodes: {len(exe_nodes)}',
                f'- GPU nodes: {len(gpu_nodes)}',
                '\n\n',
                '||CPU|GPU|',
                '|--|--|--|',
                f'|Allocated|`{sum(x.cpu_alloc for x in self.cluster_info):>6d}`|`{gpu_alloc:>6d}`|',
                f'|Idle|`{cpu_avail:>6d}`|`{gpu_avail:>6d}`|',
                f'|Total|`{sum(x.cpu_tot for x in self.cluster_info):>6d}`|`{gpu_tot:>6d}`|',
                '### Partition info',
                '|Partition|State|Timelimit|Groups|# Nodes|Nodelist|',
                '|--|--|--|--|--|--|'
            ]

            cluster = await self.slurm.partition_info()
            for (name, state), infos in dict(sorted(cluster.items(), key=lambda y: (y[0][0].casefold(), y[0][1]))).items():
                nodes = []
                for info in infos:
                    nodes.extend(cast(PartitionInfo, info).nodes)

                md.append(
                    f'|{name}|{state}|{cast(PartitionInfo, infos[0]).timelimit}|{cast(PartitionInfo, infos[0]).groups}|'
                    f'{len(set(nodes))}|{"〡".join(condense_string_list(nodes))}|')

            await self.query_one('#resource_md', Markdown).update('\n'.join(md))

    async def update_user_info(self) -> None:
        data: defaultdict[str, UserInfo] = defaultdict(UserInfo)
        for job in self.queue_info:
            data[job.user].add_job(job)

        user_table = self.query_one('#user_table', SortableDataTable)
        user_table.cursor_type = 'row'
        user_table.clear(columns=True)
        user_table.zebra_stripes = True
        user_table.add_columns('User', 'Account', 'Running', 'Queued', 'Error', 'CPUs', 'GPUs')

        for key, value in sorted(data.items()):
            user_table.add_row(
                key,
                Text(str(value.account), justify='right'),
                Text(str(value.running), justify='right'),
                Text(str(value.queued), justify='right'),
                Text(str(value.errors), justify='right'),
                Text(str(value.cpus), justify='right'),
                Text(str(value.gpus), justify='right'),
            )

    async def update_partition_info(self) -> None:
        @dataclass
        class CpuGpu:
            tot_cpu: int = 0
            alloc_cpu: int = 0
            offline_cpu: int = 0
            tot_gpu: int = 0
            alloc_gpu: int = 0
            offline_gpu: int = 0

            @property
            def idle_cpu(self) -> int:
                return self.tot_cpu - self.alloc_cpu - self.offline_cpu

            def add_cpu(self, tot: int, alloc: int) -> None:
                self.tot_cpu += tot
                self.alloc_cpu += alloc

            def add_offline_cpu(self, tot: int, alloc: int) -> None:
                self.tot_cpu += tot
                self.alloc_cpu += alloc
                self.offline_cpu += (tot - alloc)

            @property
            def idle_gpu(self) -> int:
                return self.tot_gpu - self.alloc_gpu - self.offline_gpu

            def add_gpu(self, tot: int, alloc: int) -> None:
                self.tot_gpu += tot
                self.alloc_gpu += alloc

            def add_offline_gpu(self, tot: int, alloc: int) -> None:
                self.tot_gpu += tot
                self.alloc_gpu += alloc
                self.offline_gpu += (tot - alloc)

        data: defaultdict[str, CpuGpu] = defaultdict(CpuGpu)
        for node in self.cluster_info:
            for partition in node.partitions:
                if len(set.intersection({State.DOWN, State.DRAIN}, node.states)) > 0:
                    data[partition].add_offline_cpu(node.cpu_tot, node.cpu_alloc)
                    data[partition].add_offline_gpu(node.gpu_tot, node.gpu_alloc)  # type: ignore
                    continue

                data[partition].add_cpu(node.cpu_tot, node.cpu_alloc)
                data[partition].add_gpu(node.gpu_tot, node.gpu_alloc)  # type: ignore

        partition_table = self.query_one('#partition_table', SortableDataTable)
        partition_table.cursor_type = 'row'
        partition_table.clear(columns=True)
        partition_table.zebra_stripes = True
        partition_table.add_columns('Partition', 'CPU (Tot)', 'CPU (Alloc)', 'CPU (Idle)', 'CPU (Offline)',
                                    'GPU (Tot)', 'GPU (Alloc)', 'GPU (Idle)', 'GPU (Offline)')

        for key, value in sorted(data.items()):
            partition_table.add_row(
                key,
                Text(str(value.tot_cpu), justify='right'),
                Text(str(value.alloc_cpu), justify='right'),
                Text(str(value.idle_cpu), justify='right'),
                Text(str(value.offline_cpu), justify='right'),
                Text(str(value.tot_gpu), justify='right'),
                Text(str(value.alloc_gpu), justify='right'),
                Text(str(value.idle_gpu), justify='right'),
                Text(str(value.offline_gpu), justify='right')
            )

    async def auto_update(self, value: bool) -> None:
        pass

    def copy_to_clipboard(self) -> None:
        # self.app.copy_to_clipboard('statusWidget copy to clipboard')
        self.app.notify('statusWidget copy to clipboard')

    async def _status_data_table(self) -> None:
        pass

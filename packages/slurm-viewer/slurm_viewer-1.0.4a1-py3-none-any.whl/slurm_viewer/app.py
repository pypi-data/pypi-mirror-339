import platform
from collections import defaultdict
from pathlib import Path
from typing import cast, Generator, Callable, Union

import rich
from textual import on

# pylint: disable=wrong-import-position,
rich.print('Starting application .', end='')
from textual.app import App, ComposeResult  # noqa: E402

rich.print('.', end='')
from textual.binding import Binding  # noqa: E402

rich.print('.', end='')
from textual.containers import Vertical  # noqa: E402

rich.print('.', end='')
from textual.reactive import reactive  # noqa: E402

rich.print('.', end='')
from textual.widget import Widget  # noqa: E402
from textual.widgets import Footer, Header, TabbedContent, TabPane, HelpPanel  # noqa: E402
from textual.timer import Timer  # noqa: E402

rich.print('.', end='')
from textual.css.query import NoMatches  # noqa: E402

rich.print('.', end='')
from slurm_viewer.data.slurm_communication import Slurm, SlurmPermissionDenied  # noqa: E402
from slurm_viewer.data.slurm_protocol import SlurmProtocol  # noqa: E402
from slurm_viewer.data.config import Config, Tabs, Cluster  # noqa: E402

rich.print('.', end='')
from slurm_viewer.widgets.nodes_widget import NodesWidget  # noqa: E402

rich.print('.', end='')
from slurm_viewer.widgets.queue_widget import QueueWidget  # noqa: E402

rich.print('.', end='')
from slurm_viewer.widgets.status_widget import StatusWidget  # noqa: E402

rich.print('.', end='')
from slurm_viewer.widgets.screens.select_partitions_screen import SelectPartitionScreen  # noqa: E402
from slurm_viewer.widgets.screens.help_screen import HelpScreen  # noqa: E402
from slurm_viewer.widgets.widget_types import SlurmTabBase, default_factory, setup_logging, SHOW_CLOCK, \
    AutoUpdate  # noqa: E402

rich.print('')

try:
    from slurm_viewer.widgets.plot_widget import PlotWidget
except ImportError:
    PlotWidget = None  # type: ignore

# pylint: enable=wrong-import-position


class SlurmViewer(App):
    CSS_PATH = Path(__file__).parent / 'widgets/slurm_viewer.tcss'

    BINDINGS = [
        Binding(key='f1', action='help', description='Help'),
        Binding(key='shift+f1', action='help_panel', description='Help panel'),
        Binding(key='q', action='quit', description='Quit'),
        Binding(key='u', action='user', description='User only'),
        Binding(key='p', action='partitions', description='Select Partitions'),
        Binding(key='f2', action='copy_to_clipboard', description='Copy to clipboard', show=False),
        Binding(key='f3', action='reload_config', description='Reload config', show=False),
        Binding(key='f5', action='refresh', description='Refresh', show=False),
        Binding(key='f12', action='screenshot', description='Screenshot', show=False),
    ]

    config: reactive[Config] = reactive(Config.init, layout=True, always_update=True)

    def __init__(self, factory: Callable[[Cluster], SlurmProtocol] = default_factory) -> None:
        super().__init__()
        setup_logging()
        self.title = f'{self.__class__.__name__}'  # type: ignore
        if len(self.config.clusters) == 0:
            self.app.notify(title='No clusters defined',
                            message='The settings file does not contain any cluster definitions.', severity='error')
        self.slurms: list[SlurmProtocol] = []
        self._widgets: defaultdict[str, list[SlurmTabBase]] = defaultdict(list)
        self._factory = factory
        self._auto_refresh_timer: Union[Timer, None] = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=SHOW_CLOCK)
        with Vertical():
            with TabbedContent(id='cluster_tab'):
                for idx, cluster in enumerate(self.config.clusters):
                    if len(cluster.name) == 0:
                        cluster_name = '(Fetching ...)'
                    else:
                        cluster_name = cluster.name + ' (Fetching ...)'
                    with TabPane(cluster_name, id=f'cluster_tab_{idx}'):
                        slurm = Slurm(cluster)
                        self.slurms.append(slurm)
                        yield from self.compose_tab(slurm)
        yield Footer()

    async def on_mount(self) -> None:
        self._auto_refresh_timer = self.set_interval(
            name='auto_update_timer',
            interval=self.config.ui.refresh_interval,
            callback=self.timer_update,
            pause=True
        )
        self.call_after_refresh(self._update_tab_titles)

    async def _update_tab_titles(self) -> None:
        for idx, slurm in enumerate(self.slurms):
            static_name = slurm.cluster().name  # Name from the config file

            try:
                dynamic_name = await slurm.cluster_name()  # Name returned by the cluster. Some clusters don't have this.
            except SlurmPermissionDenied:
                self.notify('Permission denied', title=f'Cluster: {static_name}')
                dynamic_name = platform.node()

            if len(static_name) > 0:
                name = static_name + f' @ {dynamic_name}'
            elif len(dynamic_name) != 0:
                name = dynamic_name
            else:
                name = 'Unknown cluster'

            self.query_one(TabbedContent).get_tab(f'cluster_tab_{idx}').label = name  # type: ignore

    def compose_tab(self, _slurm: SlurmProtocol) -> Generator[Widget, None, None]:
        with TabbedContent():
            for tab in _slurm.cluster().tabs:
                if tab == Tabs.NODES:
                    with TabPane('Nodes'):
                        nodes_widget = NodesWidget(_slurm).data_bind(SlurmViewer.config)
                        self._widgets[_slurm.cluster().name].append(nodes_widget)
                        yield nodes_widget
                        continue

                if tab == Tabs.JOBS:
                    with TabPane('Jobs'):
                        queue_widget = QueueWidget(_slurm).data_bind(SlurmViewer.config)
                        self._widgets[_slurm.cluster().name].append(queue_widget)
                        yield queue_widget
                        continue

                if tab == Tabs.STATUS:
                    with TabPane('Status'):
                        status_widget = StatusWidget(_slurm).data_bind(SlurmViewer.config)
                        self._widgets[_slurm.cluster().name].append(status_widget)
                        yield status_widget
                        continue

                if tab == Tabs.GPU:
                    if PlotWidget is None:
                        continue

                    with TabPane('GPU usage'):
                        plot_widget = PlotWidget(_slurm).data_bind(SlurmViewer.config)
                        self._widgets[_slurm.cluster().name].append(plot_widget)
                        yield plot_widget
                        continue

    async def timer_update(self) -> None:
        for widget_list in self._widgets.values():
            for widget in widget_list:
                await widget.timer_update()

    @on(AutoUpdate.Changed)
    def _auto_update_changed(self, event: AutoUpdate.Changed) -> None:
        if self.config.ui.auto_refresh == event.value:
            return

        assert self._auto_refresh_timer

        self.config.ui.auto_refresh = event.value
        # notify children of the change in auto_update state so they can update the various UI elements.
        self.mutate_reactive(SlurmViewer.config)

        if event.value:
            self.notify('Auto refresh resumed')
            self._auto_refresh_timer.resume()
        else:
            self.notify('Auto refresh paused')
            self._auto_refresh_timer.pause()

    async def action_help(self) -> None:
        await self.app.push_screen(HelpScreen(self.slurms, self.config))

    async def action_help_panel(self) -> None:
        try:
            await self.query_one(HelpPanel).remove()
        except NoMatches:
            await self.mount(HelpPanel())

    async def action_reload_config(self) -> None:
        self.notify('Reloading configuration')
        self.config = Config.init()  # type: ignore

    async def action_refresh(self) -> None:
        active_cluster_tab = self.query_one('#cluster_tab', TabbedContent).active_pane
        assert active_cluster_tab
        pane = active_cluster_tab.query_one(TabbedContent).active_pane
        assert pane

        children = pane.children
        assert len(children) == 1

        await cast(SlurmTabBase, children[0]).timer_update()

    def action_copy_to_clipboard(self) -> None:
        active_cluster_tab = self.query_one('#cluster_tab', TabbedContent).active_pane
        assert active_cluster_tab
        pane = active_cluster_tab.query_one(TabbedContent).active_pane
        assert pane

        children = pane.children
        assert len(children) == 1

        cast(SlurmTabBase, children[0]).copy_to_clipboard()

    async def action_user(self) -> None:
        self.config.ui.user_only = not self.config.ui.user_only
        self.mutate_reactive(SlurmViewer.config)
        self.notify('User only' if self.config.ui.user_only else 'All users')

    async def action_partitions(self) -> None:
        def _update_partitions(selected: Union[list[str], None]) -> None:
            if selected is None:
                return

            if active_cluster.partitions == selected:
                # selection has not changed, don't update the config to stop updating the widgets.
                return

            for cluster in self.config.clusters:
                if cluster.name == active_cluster.name:
                    cluster.partitions = selected
                    break

            self.mutate_reactive(SlurmViewer.config)

        active_pane = self.query_one('#cluster_tab', TabbedContent).active_pane
        assert active_pane
        nodes = active_pane.query_one(NodesWidget)
        assert nodes

        active_cluster = nodes.slurm.cluster()
        all_partitions = await nodes.slurm.partitions()
        screen = SelectPartitionScreen(all_partitions, active_cluster.partitions)
        await self.push_screen(screen, _update_partitions)


if __name__ == "__main__":
    app = SlurmViewer()
    app.run()

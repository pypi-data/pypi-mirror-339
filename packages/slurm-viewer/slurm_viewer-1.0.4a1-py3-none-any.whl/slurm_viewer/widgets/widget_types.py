from typing import Protocol

from loguru import logger
from textual.dom import DOMNode
from textual.message import Message

from slurm_viewer.data.config import Cluster
from slurm_viewer.data.slurm_communication import Slurm
from slurm_viewer.data.slurm_protocol import SlurmProtocol

# Use in snapshot testing to disable clock in header
SHOW_CLOCK = True


class AutoUpdate(DOMNode):
    class Changed(Message):
        def __init__(self, value: bool) -> None:
            super().__init__()
            self.value = value


class SlurmTabBase(Protocol):
    def copy_to_clipboard(self) -> None:
        ...

    async def timer_update(self) -> None:
        ...


def default_factory(cluster: Cluster) -> SlurmProtocol:
    return Slurm(cluster)


def setup_logging() -> None:
    logger.remove()  # remove the default stderr logger
    logger.add('slurm_viewer.log', level='TRACE', mode='w',
               format='{time:%Y-%m-%d_%H:%M:%S.%f} | {level.icon} | {message} | {name}:{file}:{function}[{line}]')
    # logger.add('slurm_viewer.jsonl', mode='w', serialize=True, level='TRACE')

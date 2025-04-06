import sys

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Optional

from hive.common import ArgumentParser
from hive.messaging import (
    Channel,
    Connection,
    blocking_connection,
    publisher_connection,
)


@dataclass
class Service(ABC):
    argument_parser: Optional[ArgumentParser] = None
    on_channel_open: Optional[Callable[[Channel], None]] = None
    unparsed_arguments: Optional[list[str]] = None

    def make_argument_parser(self) -> ArgumentParser:
        parser = ArgumentParser()
        return parser

    def __post_init__(self):
        if not self.argument_parser:
            self.argument_parser = self.make_argument_parser()

        in_pytest = self.argument_parser.prog == "pytest"
        if self.unparsed_arguments is None:
            if in_pytest:
                self.unparsed_arguments = []
            else:
                self.unparsed_arguments = sys.argv[1:]
        self.args = self.argument_parser.parse_args(self.unparsed_arguments)

    @classmethod
    def main(cls, **kwargs):
        service = cls(**kwargs)
        return service.run()

    @abstractmethod
    def run(self):
        raise NotImplementedError

    def blocking_connection(self, **kwargs) -> Connection:
        return self._connect(blocking_connection, kwargs)

    def publisher_connection(self, **kwargs) -> Connection:
        return self._connect(publisher_connection, kwargs)

    def _connect(self, connect, kwargs) -> Connection:
        on_channel_open = kwargs.pop("on_channel_open", self.on_channel_open)
        return connect(on_channel_open=on_channel_open, **kwargs)

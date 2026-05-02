from typing import Protocol, ClassVar,

class ServerSocketProto(Protocol):
    printer: Printer

    def stats(self, eventtime): ...

class WebHooksProto(Protocol):
    printer: Printer

    def register_endpoint(self, path: str, callback: Callable[[WebRequest], None]): ...


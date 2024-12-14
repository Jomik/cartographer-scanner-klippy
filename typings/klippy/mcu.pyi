# https://github.com/Klipper3d/klipper/blob/master/klippy/mcu.py

from typing import Any, Callable, Protocol, TypedDict, TypeVar, overload

from klippy.klippy import Printer
from klippy.reactor import ReactorCompletion
from klippy.stepper import MCU_stepper

T = TypeVar("T")

class error(Exception):
    pass

class _MCUStatus(TypedDict):
    mcu_version: str

class _CommandQueue:
    pass

class MCU:
    error: type[error]

    class sentinel:
        pass

    def alloc_command_queue(self) -> _CommandQueue:
        pass
    def register_config_callback(self, callback: Callable[[], None]) -> None:
        pass
    def register_response(
        self, callback: Callable[[T], None], message: str, oid: int | None = None
    ) -> None:
        pass
    def get_constants(self) -> dict[str, object]:
        pass
    def lookup_command(
        self, msgformat: str, cq: _CommandQueue | None = None
    ) -> CommandWrapper:
        pass
    def lookup_query_command(
        self,
        msgformat: str,
        respformat: str,
        oid: int | None = None,
        cq: _CommandQueue | None = None,
        is_async: bool = False,
    ) -> CommandQueryWrapper:
        pass
    def print_time_to_clock(self, print_time: float) -> int:
        pass
    def clock_to_print_time(self, clock: int) -> float:
        pass
    def clock32_to_clock64(self, clock32: int) -> int:
        pass
    def get_printer(self) -> Printer:
        pass
    def get_status(self) -> _MCUStatus:
        pass
    def is_fileoutput(self) -> bool:
        pass

    @overload
    def get_constant(self, name: str, default: type[sentinel] | str = sentinel) -> str:
        pass
    @overload
    def get_constant(self, name: str, default: None) -> str | None:
        pass

    @overload
    def get_constant_float(
        self, name: str, default: type[sentinel] | float = sentinel
    ) -> float:
        pass
    @overload
    def get_constant_float(self, name: str, default: None) -> float | None:
        pass

class MCU_trsync:
    REASON_ENDSTOP_HIT: int
    REASON_HOST_REQUEST: int
    REASON_PAST_END_TIME: int
    REASON_COMMS_TIMEOUT: int

    def get_oid(self) -> int:
        pass
    def get_mcu(self) -> MCU:
        pass
    def add_stepper(self, stepper: MCU_stepper) -> None:
        pass
    def get_steppers(self) -> list[MCU_stepper]:
        pass
    def start(
        self,
        print_time: float,
        report_offset: float,
        trigger_completion: ReactorCompletion,
        expire_timeout: float,
    ) -> None:
        pass
    def set_home_end_time(self, home_end_time: float) -> None:
        pass
    def stop(self) -> int:
        pass

class CommandWrapper:
    def send(self, data: list[int] = [], minclock: int = 0, reqclock: int = 0) -> None:
        pass

class CommandQueryWrapper[T = Any]:
    def send(self, data: list[int] = [], minclock: int = 0, reqclock: int = 0) -> T:
        pass

class MCU_endstop(Protocol):
    def get_mcu(self) -> MCU:
        pass
    def add_stepper(self, stepper: MCU_stepper) -> None:
        pass
    def get_steppers(self) -> list[MCU_stepper]:
        pass
    def home_start(
        self,
        print_time: float,
        sample_time: float,
        sample_count: int,
        rest_time: float,
        triggered: bool = True,
    ) -> ReactorCompletion:
        pass
    def home_wait(self, home_end_time: float) -> float:
        pass
    def query_endstop(self, print_time: float) -> int:
        pass

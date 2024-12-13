from typing import Callable, Protocol, Tuple, TypedDict
from klippy.configfile import ConfigWrapper
from klippy.gcode import GCodeCommand
from klippy.mcu import MCU_endstop

HINT_TIMEOUT: str

class _ProbeStatus(TypedDict):
    name: str
    last_query: bool | int
    last_z_result: float

class ProbeCommandHelper:
    def __init__(
        self,
        config: ConfigWrapper,
        probe: object,
        query_endstop: Callable[[float], int] | None = None,
    ) -> None:
        pass

    def get_status(self, eventtime: float) -> _ProbeStatus:
        pass

class ProbeOffsetsHelper:
    def __init__(self, config: ConfigWrapper) -> None:
        pass

    def get_offsets(self) -> Tuple[float, float, float]:
        pass

class _ProbeSession(Protocol):
    pass

class _ProbeParams(TypedDict):
    probe_speed: float
    lift_speed: float
    samples: int
    sample_retract_dist: float
    samples_tolerance: float
    samples_tolerance_retries: int
    samples_result: float

class ProbeSessionHelper:
    def __init__(self, config: ConfigWrapper, mcu_probe: ProbeEndstopWrapper) -> None:
        pass
    def start_probe_session(self, gcmd: GCodeCommand) -> _ProbeSession:
        pass
    def end_probe_session(self) -> None:
        pass
    def get_probe_params(self, gcmd: GCodeCommand | None = None) -> _ProbeParams:
        pass
    def run_probe(self, gcmd: GCodeCommand) -> None:
        pass
    def pull_probed_results(self) -> list[float]:
        pass

class ProbeEndstopWrapper(MCU_endstop, Protocol):
    def multi_probe_begin(self) -> None:
        pass
    def multi_probe_end(self) -> None:
        pass
    def probing_move(self, pos: list[float], speed: float) -> list[float]:
        pass
    def probe_prepare(self, hmove: float) -> None:
        pass
    def probe_finish(self, hmove: float) -> None:
        pass
    def get_position_endstop(self) -> float:
        pass

class PrinterProbe(Protocol):
    def get_probe_params(self, gcmd: GCodeCommand | None = None) -> _ProbeParams:
        pass
    def get_offsets(self) -> Tuple[float, float, float]:
        pass
    def get_status(self, eventtime: float) -> _ProbeStatus:
        pass
    def start_probe_session(self, gcmd: GCodeCommand) -> _ProbeSession:
        pass

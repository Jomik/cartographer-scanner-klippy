from __future__ import annotations

from typing import TYPE_CHECKING, final

from extras.probe import ProbeEndstopWrapper
from typing_extensions import override

from cartographer.mcu import ScannerMCUHelper

if TYPE_CHECKING:
    from klippy.configfile import ConfigWrapper
    from klippy.mcu import MCU
    from klippy.reactor import ReactorCompletion
    from klippy.stepper import MCU_stepper


@final
class ScannerEndstopWrapper(ProbeEndstopWrapper):
    def __init__(self, config: ConfigWrapper, mcu_helper: ScannerMCUHelper):
        self._mcu_helper = mcu_helper

    @override
    def get_mcu(self) -> MCU:
        return self._mcu_helper.get_mcu()

    @override
    def add_stepper(self, stepper: MCU_stepper) -> None:
        raise NotImplementedError()

    @override
    def get_steppers(self) -> list[MCU_stepper]:
        raise NotImplementedError()

    @override
    def home_start(
        self,
        print_time: float,
        sample_time: float,
        sample_count: int,
        rest_time: float,
        triggered: bool = True,
    ) -> ReactorCompletion:
        raise NotImplementedError()

    @override
    def home_wait(self, home_end_time: float) -> float:
        raise NotImplementedError()

    @override
    def query_endstop(self, print_time: float) -> int:
        raise NotImplementedError()

    @override
    def multi_probe_begin(self) -> None:
        raise NotImplementedError()

    @override
    def multi_probe_end(self) -> None:
        raise NotImplementedError()

    @override
    def probing_move(self, pos: "list[float]", speed: float) -> "list[float]":
        raise NotImplementedError()

    @override
    def probe_prepare(self, hmove: float) -> None:
        raise NotImplementedError()

    @override
    def probe_finish(self, hmove: float) -> None:
        raise NotImplementedError()

    @override
    def get_position_endstop(self) -> float:
        raise NotImplementedError()

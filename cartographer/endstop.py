from __future__ import annotations

from typing import final

from configfile import ConfigWrapper
from extras.probe import ProbeEndstopWrapper
from mcu import MCU, TriggerDispatch
from reactor import ReactorCompletion
from stepper import MCU_stepper
from typing_extensions import override

from cartographer.mcu import ScannerMCUHelper


@final
class ScannerEndstopWrapper(ProbeEndstopWrapper):
    def __init__(self, config: ConfigWrapper, mcu_helper: ScannerMCUHelper):
        self.printer = config.get_printer()
        self._mcu_helper = mcu_helper
        self._dispatch = TriggerDispatch(mcu_helper.get_mcu())
        self.printer.register_event_handler(
            "klippy:mcu_identify", self._register_steppers
        )

    def _register_steppers(self):
        toolhead = self.printer.lookup_object("toolhead")
        kin = toolhead.get_kinematics()
        for stepper in kin.get_steppers():
            if stepper.is_active_axis("z"):
                self.add_stepper(stepper)

    @override
    def get_mcu(self) -> MCU:
        return self._mcu_helper.get_mcu()

    @override
    def add_stepper(self, stepper: MCU_stepper) -> None:
        return self._dispatch.add_stepper(stepper)

    @override
    def get_steppers(self) -> list[MCU_stepper]:
        return self._dispatch.get_steppers()

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

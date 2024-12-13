from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional, final

from extras import probe

if TYPE_CHECKING:
    from klippy.configfile import ConfigWrapper
    from klippy.gcode import GCodeCommand
    from klippy.mcu import MCU
    from klippy.reactor import ReactorCompletion
    from klippy.stepper import MCU_stepper


@final
class PrinterScanner:
    def __init__(self, config: ConfigWrapper):
        printer = config.get_printer()
        endstop = ScannerEndstopWrapper(config)
        probe_interface = ScannerProbeWrapper(config, endstop)
        printer.add_object("probe", probe_interface)
        logging.info("Successfully added probe!")


@final
class ScannerEndstopWrapper(probe.ProbeEndstopWrapper):
    def __init__(self, config: ConfigWrapper):
        pass

    def get_mcu(self) -> MCU:
        raise NotImplementedError()

    def add_stepper(self, stepper: MCU_stepper) -> None:
        raise NotImplementedError()

    def get_steppers(self) -> list[MCU_stepper]:
        raise NotImplementedError()

    def home_start(
        self,
        print_time: float,
        sample_time: float,
        sample_count: int,
        rest_time: float,
        triggered: bool = True,
    ) -> ReactorCompletion:
        raise NotImplementedError()

    def home_wait(self, home_end_time: float) -> float:
        raise NotImplementedError()

    def query_endstop(self, print_time: float) -> int:
        raise NotImplementedError()

    def multi_probe_begin(self) -> None:
        raise NotImplementedError()

    def multi_probe_end(self) -> None:
        raise NotImplementedError()

    def probing_move(self, pos: "list[float]", speed: float) -> "list[float]":
        raise NotImplementedError()

    def probe_prepare(self, hmove: float) -> None:
        raise NotImplementedError()

    def probe_finish(self, hmove: float) -> None:
        raise NotImplementedError()

    def get_position_endstop(self) -> float:
        raise NotImplementedError()


@final
class ScannerProbeWrapper:
    def __init__(self, config: ConfigWrapper, endstop: ScannerEndstopWrapper):
        self.cmd_helper = probe.ProbeCommandHelper(config, self, endstop.query_endstop)
        self.probe_offsets = probe.ProbeOffsetsHelper(config)
        self.probe_session = probe.ProbeSessionHelper(config, endstop)

    def get_probe_params(self, gcmd: Optional[GCodeCommand] = None):
        return self.probe_session.get_probe_params(gcmd)

    def get_offsets(self):
        return self.probe_offsets.get_offsets()

    def get_status(self, eventtime: float):
        return self.cmd_helper.get_status(eventtime)

    def start_probe_session(self, gcmd: GCodeCommand):
        return self.probe_session.start_probe_session(gcmd)

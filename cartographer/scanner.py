from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional, final

from extras import probe
from typing_extensions import override

from cartographer.endstop import ScannerEndstopWrapper
from cartographer.mcu import ScannerMCU

if TYPE_CHECKING:
    from klippy.configfile import ConfigWrapper
    from klippy.gcode import GCodeCommand


@final
class PrinterScanner:
    def __init__(self, config: ConfigWrapper):
        printer = config.get_printer()
        endstop = ScannerEndstopWrapper(config)
        mcu = ScannerMCU(config)
        probe_interface = ScannerProbeInterface(config, endstop)
        printer.add_object("probe", probe_interface)
        logging.info("Successfully added probe!")


@final
class ScannerProbeInterface(probe.PrinterProbe):
    def __init__(self, config: ConfigWrapper, endstop: ScannerEndstopWrapper):
        self.cmd_helper = probe.ProbeCommandHelper(config, self, endstop.query_endstop)
        self.probe_offsets = probe.ProbeOffsetsHelper(config)
        self.probe_session = probe.ProbeSessionHelper(config, endstop)

    @override
    def get_probe_params(self, gcmd: Optional[GCodeCommand] = None):
        return self.probe_session.get_probe_params(gcmd)

    @override
    def get_offsets(self):
        return self.probe_offsets.get_offsets()

    @override
    def get_status(self, eventtime: float):
        return self.cmd_helper.get_status(eventtime)

    @override
    def start_probe_session(self, gcmd: GCodeCommand):
        return self.probe_session.start_probe_session(gcmd)

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional, final

from extras import probe

from .endstop import ScannerEndstopWrapper

if TYPE_CHECKING:
    from klippy.configfile import ConfigWrapper
    from klippy.gcode import GCodeCommand


@final
class PrinterScanner:
    def __init__(self, config: ConfigWrapper):
        printer = config.get_printer()
        endstop = ScannerEndstopWrapper(config)
        probe_interface = ScannerProbeWrapper(config, endstop)
        printer.add_object("probe", probe_interface)
        logging.info("Successfully added probe!")


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

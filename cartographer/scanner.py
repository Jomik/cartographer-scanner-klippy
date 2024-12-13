from typing import Optional, final

from extras import probe
from klippy import configfile, gcode


@final
class PrinterScanner:
    def __init__(self, config: configfile.ConfigWrapper):
        self.mcu_probe = ScannerEndstopWrapper(config)
        probe_interface = PrinterProbeInterface(config, self)
        config.get_printer().add_object("probe", probe_interface)


@final
class ScannerEndstopWrapper:
    def __init__(self, config: configfile.ConfigWrapper):
        pass

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
class PrinterProbeInterface:
    def __init__(self, config: configfile.ConfigWrapper, scanner: PrinterScanner):
        pass
        self.cmd_helper = probe.ProbeCommandHelper(config, self, self._query_endstop)
        self.probe_offsets = probe.ProbeOffsetsHelper(config)
        self.probe_session = probe.ProbeSessionHelper(config, scanner.mcu_probe)

    def _query_endstop(self, _eventtime: float) -> bool:
        raise NotImplementedError()

    def get_probe_params(self, gcmd: Optional[gcode.GCodeCommand] = None):
        return self.probe_session.get_probe_params(gcmd)

    def get_offsets(self):
        return self.probe_offsets.get_offsets()

    def get_status(self, eventtime: float):
        return self.cmd_helper.get_status(eventtime)

    def start_probe_session(self, gcmd: gcode.GCodeCommand):
        return self.probe_session.start_probe_session(gcmd)

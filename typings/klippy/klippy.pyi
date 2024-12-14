# https://github.com/Klipper3d/klipper/blob/master/klippy/klippy.py
from typing import Callable, Literal, TypeVar, overload

import configfile
from extras.bed_mesh import BedMesh
from extras.heaters import PrinterHeaters
from extras.homing import PrinterHoming
from extras.probe import PrinterProbe
from klippy.configfile import ConfigWrapper, PrinterConfig, sentinel
from klippy.gcode import CommandError, GCodeDispatch
from klippy.pins import PrinterPins
from klippy.reactor import Reactor
from klippy.stepper import PrinterRail
from klippy.toolhead import ToolHead

from cartographer.scanner import PrinterScanner

T = TypeVar("T")

class Printer:
    config_error: type[configfile.error]
    command_error: type[CommandError]
    def add_object(self, name: Literal["probe"], obj: PrinterProbe) -> None:
        pass
    @overload
    def load_object(
        self,
        config: ConfigWrapper,
        section: Literal["bed_mesh"],
    ) -> BedMesh:
        pass
    @overload
    def load_object(
        self,
        config: ConfigWrapper,
        section: Literal["heaters"],
    ) -> PrinterHeaters:
        pass
    @overload
    def load_object(
        self,
        config: ConfigWrapper,
        section: str,
        default: T | type[sentinel] = sentinel,
    ) -> T:
        pass

    def is_shutdown(self) -> bool:
        pass
    def invoke_shutdown(self, msg: str) -> None:
        pass
    def get_reactor(self) -> Reactor:
        pass
    @overload
    def register_event_handler(
        self, event: Literal["klippy:connect"], callback: Callable[[], None]
    ) -> None:
        pass
    @overload
    def register_event_handler(
        self, event: Literal["klippy:disconnect"], callback: Callable[[], None]
    ) -> None:
        pass
    @overload
    def register_event_handler(
        self, event: Literal["klippy:mcu_identify"], callback: Callable[[], None]
    ) -> None:
        pass
    @overload
    def register_event_handler(
        self,
        event: Literal["homing:home_rails_begin"],
        callback: Callable[[PrinterHoming, list[PrinterRail]], None],
    ) -> None:
        pass
    @overload
    def register_event_handler(
        self,
        event: Literal["homing:home_rails_end"],
        callback: Callable[[PrinterHoming, list[PrinterRail]], None],
    ) -> None:
        pass

    @overload
    def lookup_object(self, name: Literal["configfile"]) -> PrinterConfig:
        pass
    @overload
    def lookup_object(self, name: Literal["gcode"]) -> GCodeDispatch:
        pass
    @overload
    def lookup_object(self, name: Literal["homing"]) -> PrinterHoming:
        pass
    @overload
    def lookup_object(self, name: Literal["pins"]) -> PrinterPins:
        pass
    @overload
    def lookup_object(self, name: Literal["scanner"]) -> PrinterScanner:
        pass
    @overload
    def lookup_object(self, name: Literal["toolhead"]) -> ToolHead:
        pass
    @overload
    def lookup_object(self, name: str, default: T | type[sentinel] = sentinel) -> T:
        pass

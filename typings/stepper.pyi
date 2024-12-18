# https://github.com/Klipper3d/klipper/blob/master/klippy/stepper.py
from typing import Literal, Tuple

from mcu import MCU, MCU_endstop

type _Pos = list[float]

class MCU_stepper:
    def get_mcu(self) -> MCU: ...
    def get_name(self, short: bool = False) -> str: ...
    def get_commanded_position(self) -> _Pos: ...
    def is_active_axis(self, axis: Literal["x", "y", "z", "e"]) -> bool: ...

class PrinterRail:
    def get_steppers(self) -> list[MCU_stepper]: ...
    def get_endstops(self) -> list[Tuple[MCU_endstop, str]]: ...
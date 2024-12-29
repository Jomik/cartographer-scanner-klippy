# Helper script to determine a Z height
from typing import Callable
from gcode import GCodeCommand
from klippy import Printer

type _Pos = list[float]

class ManualProbeHelper:
    def __init__(
        self,
        printer: Printer,
        gcmd: GCodeCommand,
        finalize_callback: Callable[[_Pos], None],
    ) -> None: ...
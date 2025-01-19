# https://github.com/Klipper3d/klipper/blob/master/klippy/extras/bed_mesh.py
from typing import Iterator, Literal, Optional, Tuple, TypedDict

from gcode import GCodeCommand

type _Pos = list[float]

class BedMeshError(Exception): ...

class _Params(TypedDict):
    mesh_min: Tuple[float, float]
    mesh_max: Tuple[float, float]
    x_count: int
    y_count: int
    mesh_x_pps: int
    mesh_y_pps: int
    algo: Literal["lagrange", "bicubic", "direct"]
    tension: float

class ZMesh:
    def __init__(self, params: _Params, name: str | None) -> None: ...
    def build_mesh(self, z_matrix: list[_Pos]) -> None: ...

class BedMesh:
    bmc: BedMeshCalibrate
    horizontal_move_z: float
    def set_mesh(self, mesh: Optional[ZMesh]) -> None: ...

class BedMeshCalibrate:
    mesh_config: _Params
    probe_mgr: ProbeManager
    _profile_name: str
    def update_config(self, gcmd: GCodeCommand) -> None: ...
    def probe_finalize(
        self, offsets: list[float], positions: list[list[float]]
    ) -> None: ...

class ProbeManager:
    def iter_rapid_path(self) -> Iterator[Tuple[Tuple[float, float], bool]]: ...

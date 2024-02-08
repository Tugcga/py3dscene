from enum import Enum
import sys

class CameraType(Enum):
    PERSPECTIVE = 1
    ORTHOGRAPHIC = 2

class CameraComponent:
    def __init__(self):
        self._type = CameraType.PERSPECTIVE
        self._near = 0.0
        self._far = sys.float_info.max
        # only for perspective
        self._aspect = 1.0
        self._fov = 0.7  # vertical field of view
        # for orthographic
        self._ortho_width = 1.0
        self._ortho_height = 1.0

    def set_type(self, value: CameraType):
        self._type = value
    
    def set_clipping_planes(self, near: float, far: float):
        self._near = near
        self._far = far
    
    def set_perspective_aspect(self, value: float):
        self._aspect = value
    
    def set_perspective_fov(self, value: float):
        self._fov = value
    
    def set_orthographic_size(self, width: float, height: float):
        self._ortho_width = width
        self._ortho_height = height
    
    def get_type(self) -> CameraType:
        return self._type
    
    def get_clipping_near(self) -> float:
        return self._near
    
    def get_clipping_far(self) -> float:
        return self._far
    
    def get_perspective_aspect(self) -> float:
        return self._aspect

    def get_perspective_fov(self) -> float:
        return self._fov
    
    def get_orthographic_width(self) -> float:
        return self._ortho_width
    
    def get_orthographic_height(self) -> float:
        return self._ortho_height
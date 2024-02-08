from enum import Enum
import math
from py3dscene.material import RGB

class LightType(Enum):
    POINT = 1
    SPOT = 2
    DIRECTIONAL = 3

class LightComponent:
    def __init__(self) -> None:
        self._name: str = "unnamed"
        self._color: RGB = (1.0, 1.0, 1.0)
        self._strength: float = 1.0
        self._type: LightType = LightType.POINT
        self._range: float = 0.0  # by default is infinite
        # for spots only, angles in radians
        self._spot_inner_cone: float = 0.0
        self._spot_outer_cone = math.pi / 4.0
    
    def set_name(self, value: str):
        self._name = value
    
    def set_color(self, r: float, g: float, b: float):
        self._color = (r, g, b)
    
    def set_strength(self, value: float):
        self._strength = value
    
    def set_type(self, value: LightType):
        self._type = value
    
    def set_range(self, value: float):
        self._range = value
    
    def set_spot_angles(self, inner: float, outer: float):
        self._spot_inner_cone = inner
        self._spot_outer_cone = outer
    
    def get_name(self) -> str:
        return self._name
    
    def get_color(self) -> RGB:
        return self._color
    
    def get_strength(self) -> float:
        return self._strength
    
    def get_type(self) -> LightType:
        return self._type
    
    def get_range(self) -> float:
        return self._range
    
    def get_spot_inner_cone(self) -> float:
        return self._spot_inner_cone

    def get_spot_outer_cone(self) -> float:
        return self._spot_outer_cone

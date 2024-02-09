from enum import Enum
import math

class LightType(Enum):
    POINT = 1
    SPOT = 2
    DIRECTIONAL = 3

class LightComponent:
    '''Store the light in the 3d-scene
    '''
    def __init__(self) -> None:
        self._name: str = "unnamed"
        self._color: tuple[float, float, float] = (1.0, 1.0, 1.0)
        self._strength: float = 1.0
        self._type: LightType = LightType.POINT
        self._range: float = 0.0  # by default is infinite
        # for spots only, angles in radians
        self._spot_inner_cone: float = 0.0
        self._spot_outer_cone = math.pi / 4.0
    
    def set_name(self, value: str):
        '''Define the light name
        '''
        self._name = value
    
    def set_color(self, r: float, g: float, b: float):
        '''Define the light color
        '''
        self._color = (r, g, b)
    
    def set_strength(self, value: float):
        '''Define the light intensity
        '''
        self._strength = value
    
    def set_type(self, value: LightType):
        '''Define the light type (point, spot or directional)
        '''
        self._type = value
    
    def set_range(self, value: float):
        '''Define the light range
        '''
        self._range = value
    
    def set_spot_angles(self, inner: float, outer: float):
        '''Define inner and outer angles for the spot light
        '''
        self._spot_inner_cone = inner
        self._spot_outer_cone = outer
    
    def get_name(self) -> str:
        '''Return the light's name
        '''
        return self._name
    
    def get_color(self) -> tuple[float, float, float]:
        '''Return the color of the light
        '''
        return self._color
    
    def get_strength(self) -> float:
        '''Return the light's intensity
        '''
        return self._strength
    
    def get_type(self) -> LightType:
        '''Return the light's type
        '''
        return self._type
    
    def get_range(self) -> float:
        '''Return the light's range
        '''
        return self._range
    
    def get_spot_inner_cone(self) -> float:
        '''Return hte inner cone of the spot light
        '''
        return self._spot_inner_cone

    def get_spot_outer_cone(self) -> float:
        '''Return the outer cone of the spot light
        '''
        return self._spot_outer_cone

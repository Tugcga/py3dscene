from enum import Enum
from typing import Optional
import sys

class CameraType(Enum):
    PERSPECTIVE = 1
    ORTHOGRAPHIC = 2

class CameraComponent:
    '''Store the camera in the 3d-scene
    '''
    def __init__(self) -> None:
        self._type = CameraType.PERSPECTIVE
        self._near = 0.0
        self._far = sys.float_info.max
        # only for perspective
        self._aspect = 1.0
        self._fov = 0.7  # vertical field of view
        # for orthographic
        self._ortho_width = 1.0
        self._ortho_height = 1.0
    
    def set_type(self, value: CameraType) -> None:
        '''Define the camera type (perspective or orthographic)
        '''
        self._type = value
    
    def set_clipping_planes(self, near: float, far: float) -> None:
        '''Define clipping planes of the camera
        '''
        self._near = near
        self._far = far
    
    def set_perspective_aspect(self, value: float) -> None:
        '''Define aspect ratio of the perspective camera
        '''
        self._aspect = value
    
    def set_perspective_fov(self, value: float) -> None:
        '''Define vertical field of view of the perspective camera
        '''
        self._fov = value
    
    def set_orthographic_size(self, width: float, height: float) -> None:
        '''Define size of the orthographic camera
        '''
        self._ortho_width = width
        self._ortho_height = height
        
    def get_type(self) -> CameraType:
        '''Return type of the camera
        '''
        return self._type
    
    def get_clipping_near(self) -> float:
        '''Return values of the near clipping plane of the camera
        '''
        return self._near
    
    def get_clipping_far(self) -> float:
        '''Return value of the far clipping plane of the camera
        '''
        return self._far
    
    def get_perspective_aspect(self) -> float:
        '''Return aspect raton of the perspective camera
        '''
        return self._aspect

    def get_perspective_fov(self) -> float:
        '''Return vertical field of view of the perspective camera
        '''
        return self._fov
    
    def get_orthographic_width(self) -> float:
        '''Return width of the orthographic camera
        '''
        return self._ortho_width
    
    def get_orthographic_height(self) -> float:
        '''Return height of the orthographic camera
        '''
        return self._ortho_height

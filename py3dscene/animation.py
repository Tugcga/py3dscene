from typing import Optional
from enum import Enum

class AnimationCurveType(Enum):
    LINEAR = 1
    STEP = 2
    CUBICSPLINE = 3

Vector3d = tuple[float, float, float]
Quaternion4d = tuple[float, float, float, float]
Vector3dTriple = tuple[Vector3d, Vector3d, Vector3d]
Quaternion4dTriple = tuple[Quaternion4d, Quaternion4d, Quaternion4d]
ValuesVariants = Vector3d | Quaternion4d | Vector3dTriple | Quaternion4dTriple

class Animation:
    '''Store animation clip
    '''
    def __init__(self, type: AnimationCurveType, value_components: int) -> None:
        '''Create animation clip object and store the curve for one parameter
        Parameters:
            type - the type of the curve (Linear, Step or CubicSpline)
            value_components - the number of vector component for one value (3 for position, 4 for quaternion)
        '''
        self._type: AnimationCurveType = type
        self._points_count: int = 0
        self._frames: list[float] = []
        self._values: list[ValuesVariants] = []
        self._value_components = value_components
    
    def add_keyframe(self, frame: float, value: ValuesVariants) -> None:
        '''Add keyframe to the clip at specific frame and with specific value
        '''
        # check is the value have the proper format
        if self._type == AnimationCurveType.CUBICSPLINE:
            # in this case value should be the triple of tuples
            for v in value:
                if not (type(v) == tuple and len(v) == self._value_components):
                    return None
        else:
            # in this case case should be a tuple
            if len(value) != self._value_components:
                return None

        i: int = 0
        while i < len(self._frames) and self._frames[i] < frame:
            i += 1
        if i == len(self._frames):
            self._frames.append(frame)
            self._values.append(value)
        else:
            self._frames.insert(i, frame)
            self._values.insert(i, value)
        self._points_count += 1
    
    def get_type(self) -> AnimationCurveType:
        '''Return type of the animation clip (linear, step or cubic)
        '''
        return self._type
    
    def get_value_components(self) -> int:
        '''Return the number of components in one value stored in the animation
        For example, rotation stored as 4d-tuple, translation and scale as 3d-tuple
        This value does not depend on the animation curve type
        '''
        return self._value_components
    
    def get_frames(self) -> list[float]:
        '''Return the list of all key frames
        '''
        return self._frames
    
    def get_value_at_frame(self, frame: float) -> Optional[ValuesVariants]:
        '''Return value at specific key frame
        If there are no key frame in the clip, then return None
        This method does not interpolate values between different key frames
        '''
        for i, f in enumerate(self._frames):
            if abs(f - frame) < 0.0001:
                return self._values[i]
        return None
    
    def __str__(self) -> str:
        end = " empty" if self._points_count == 0 else ""
        parts: list[str] = [f"Animation {self._type}:{end}"]
        for i in range(self._points_count):
            parts.append(f"  frame {self._frames[i]}: {self._values[i]}")
        return "\n".join(parts)

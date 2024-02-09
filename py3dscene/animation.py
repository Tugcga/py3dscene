from typing import Optional
from enum import Enum

class AnimationCurveType(Enum):
    LINEAR = 1
    STEP = 2
    CUBICSPLINE = 3

Vector3d = tuple[float, float, float]
Quaternion4d = tuple[float, float, float, float]
ValuesVariants = Vector3d | Quaternion4d | tuple[Vector3d, Vector3d, Vector3d] | tuple[Quaternion4d, Quaternion4d, Quaternion4d]

class Animation:
    def __init__(self, type: AnimationCurveType) -> None:
        self._type: AnimationCurveType = type
        self._points_count: int = 0
        self._frames: list[float] = []
        self._values: list[ValuesVariants] = []
    
    def add_keyframe(self, frame: float, value: ValuesVariants):
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
        return self._type
    
    def get_frames(self) -> list[float]:
        return self._frames
    
    def get_value_at_frame(self, frame: float) -> Optional[ValuesVariants]:
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

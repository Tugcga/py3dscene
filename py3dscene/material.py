from enum import Enum
from typing import Optional

class AlphaMode(Enum):
    OPAQUE = 1
    MASK = 2
    BLEND = 3

Color = tuple[float, float, float, float]
RGB = tuple[float, float, float]

class Material:
    id_pointer: int = 0

class PBRMaterial(Material):
    def __init__(self, name: str="", id: Optional[int]=None) -> None:
        self._id: int = 0
        if id is None:
            self._id = Material.id_pointer
            Material.id_pointer += 1
        else:
            self._id = id
        
        self._name: str = name if len(name) > 0 else "unnamed"
        self._alpha_mode: AlphaMode = AlphaMode.OPAQUE
        self._alpha_cutoff: float = 0.5
        self._is_double_sided: bool = False
        self._metalness: float = 0.5
        self._roughness: float = 0.5
        self._albedo: Color = (0.8, 0.8, 0.8, 1.0)
        self._emissive: RGB = (0.0, 0.0, 0.0)
        # each texture stored as
        #   - path
        #   - uv_channel
        self._albedo_texture: Optional[tuple[str, int]] = None
        self._metallic_roughness_texture: Optional[tuple[str, int]] = None
        self._emissive_texture: Optional[tuple[str, int]] = None
        # normal and occlusion additionally have parameter
        #   - strength
        self._normal_texture: Optional[tuple[str, int, float]] = None
        self._occlusion_texture: Optional[tuple[str, int, float]] = None
    
    def set_alpha_mode(self, value: AlphaMode):
        self._alpha_mode = value
    
    def set_alpha_cutoff(self, value: float):
        self._alpha_cutoff = value
    
    def set_double_sided(self, value: bool):
        self._is_double_sided = value
    
    def set_albedo(self, r: float, g: float, b: float, a: float):
        self._albedo = (r, g, b, a)
    
    def set_metalness(self, value: float):
        self._metalness = value
    
    def set_roughness(self, value: float):
        self._roughness = value
    
    def set_emissive(self, r: float, g: float, b: float):
        self._emissive = (r, g, b)
    
    def set_albedo_texture(self, texture_path: str, uv_index: int):
        self._albedo_texture = (texture_path, uv_index)
    
    def set_metallic_roughness_texture(self, texture_path: str, uv_index: int):
        self._metallic_roughness_texture = (texture_path, uv_index)
    
    def set_emissive_texture(self, texture_path: str, uv_index: int):
        self._emissive_texture = (texture_path, uv_index)
    
    def set_normal_texture(self, texture_path: str, uv_index: int, strength: float):
        self._normal_texture = (texture_path, uv_index, strength)
    
    def set_occlusion_texture(self, texture_path: str, uv_index: int, strength: float):
        self._occlusion_texture = (texture_path, uv_index, strength)
    
    def get_id(self) -> int:
        return self._id
    
    def get_name(self) -> str:
        return self._name

    def get_alpha_mode(self) -> AlphaMode:
        return self._alpha_mode

    def get_alpha_cutoff(self) -> float:
        return self._alpha_cutoff
    
    def get_double_sided(self) -> bool:
        return self._is_double_sided
    
    def get_albedo(self) -> Color:
        return self._albedo

    def get_metalness(self) -> float:
        return self._metalness

    def get_roughness(self) -> float:
        return self._roughness

    def get_emissive(self) -> RGB:
        return self._emissive
    
    def get_albedo_texture_path(self) -> Optional[str]:
        if self._albedo_texture:
            return self._albedo_texture[0]
        else:
            return None
    
    def get_albedo_texture_uv(self) -> Optional[int]:
        if self._albedo_texture:
            return self._albedo_texture[1]
        else:
            return None

    def get_metallic_roughness_texture_path(self) -> Optional[str]:
        if self._metallic_roughness_texture:
            return self._metallic_roughness_texture[0]
        else:
            return None
    
    def get_metallic_roughness_texture_uv(self) -> Optional[int]:
        if self._metallic_roughness_texture:
            return self._metallic_roughness_texture[1]
        else:
            return None
    
    def get_emissive_texture_path(self) -> Optional[str]:
        if self._emissive_texture:
            return self._emissive_texture[0]
        else:
            return None
    
    def get_emissive_texture_uv(self) -> Optional[int]:
        if self._emissive_texture:
            return self._emissive_texture[1]
        else:
            return None
    
    def get_normal_texture_path(self) -> Optional[str]:
        if self._normal_texture:
            return self._normal_texture[0]
        else:
            return None
    
    def get_normal_texture_uv(self) -> Optional[int]:
        if self._normal_texture:
            return self._normal_texture[1]
        else:
            return None
    
    def get_normal_texture_strength(self) -> Optional[float]:
        if self._normal_texture:
            return self._normal_texture[2]
        else:
            return None
    
    def get_occlusion_texture_path(self) -> Optional[str]:
        if self._occlusion_texture:
            return self._occlusion_texture[0]
        else:
            return None
    
    def get_occlusion_texture_uv(self) -> Optional[int]:
        if self._occlusion_texture:
            return self._occlusion_texture[1]
        else:
            return None
    
    def get_occlusion_texture_strength(self) -> Optional[float]:
        if self._occlusion_texture:
            return self._occlusion_texture[2]
        else:
            return None
    
    def __str__(self) -> str:
        return f"{self._name}"

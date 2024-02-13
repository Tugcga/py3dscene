from __future__ import annotations  # remove for Python 3.11
from typing import Optional
from py3dscene.transform import Transform
from py3dscene.transform import get_identity
from py3dscene.transform import tfm_to_translation
from py3dscene.transform import tfm_to_rotation
from py3dscene.transform import tfm_to_scale
from py3dscene.transform import get_srt_matrix
from py3dscene.transform import get_scale_matrix
from py3dscene.transform import multiply
from py3dscene.camera import CameraComponent
from py3dscene.light import LightComponent
from py3dscene.mesh import MeshComponent
from py3dscene.animation import Animation

class Object:
    '''Class for store object inside a 3d-scene
    '''
    id_pointer: int = 0

    def __init__(self, name: str="", id: Optional[int]=None) -> None:
        self._name: str = name if len(name) > 0 else "unnamed"
        self._children: list[Object] = []
        self._id: int = 0
        if id is None:
            self._id = Object.id_pointer
            Object.id_pointer += 1
        else:
            self._id = id
        # for each object store transform as matrix
        self._transform: Transform = get_identity()
        # and also as separate translation, rotation quaternion and scale
        self._translation: tuple[float, float, float] = (0.0, 0.0, 0.0)
        # quaternion stored in format (x, y, z, w) = w + i * x + j * y + k * z
        self._rotation: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)
        self._scale: tuple[float, float, float] = (1.0, 1.0, 1.0)

        # each object can store several components
        self._camera: Optional[CameraComponent] = None
        self._light: Optional[LightComponent] = None
        # object can contains several mesh components
        self._meshes: list[MeshComponent] = []

        # animations
        self._translation_animation: Optional[Animation] = None
        self._rotation_animation: Optional[Animation] = None
        self._scale_animation: Optional[Animation] = None
    
    def create_subobject(self, name: str="", id: Optional[int]=None) -> Object:
        '''Create and return a new object. Parent it to the current object
        It's possible to define custom id for the new object
        If id is not defines, then use the global counter
        It's does not recommended to mix custom and automatic ids: use either only custom id's for all object all automatic ones
        '''
        new_object: Object = Object(name, id)
        self._children.append(new_object)
        return new_object
    
    def set_local_tfm(self, tfm: Transform):
        '''Define matrix of the local transformation of the object
        '''
        self._transform = tfm
        # also extract translation, rotation and scale from this matrix
        self._translation = tfm_to_translation(tfm)
        self._scale = tfm_to_scale(tfm)
        # for rotation we should previously rescale transform 
        inv_scale_tfm = get_scale_matrix(1.0 / self._scale[0], 1.0 / self._scale[1], 1.0 / self._scale[2])
        rescale_tfm = multiply(tfm, inv_scale_tfm)
        # extract rotation from scaled matrix
        self._rotation = tfm_to_rotation(rescale_tfm)
    
    def set_local_translation(self, x: float, y: float, z: float):
        '''Define position of the object
        '''
        self._translation = (x, y, z)
        self._transform = get_srt_matrix(self._translation, self._rotation, self._scale)

    def set_local_rotation(self, x: float, y: float, z: float, w: float):
        '''Define rotation of the object
        '''
        self._rotation = (x, y, z, w)
        self._transform = get_srt_matrix(self._translation, self._rotation, self._scale)

    def set_local_scale(self, x: float, y: float, z: float):
        '''Define scale of the object
        '''
        self._scale = (x, y, z)
        self._transform = get_srt_matrix(self._translation, self._rotation, self._scale)
    
    def set_camera_component(self, camera: CameraComponent):
        '''Add camera component to the object
        '''
        self._camera = camera
    
    def set_light_component(self, light: LightComponent):
        '''Add light component to the object
        '''
        self._light = light
    
    def set_translation_animation(self, animation: Animation):
        '''Define translation animation of the object
        '''
        self._translation_animation = animation
    
    def set_rotation_animation(self, animation: Animation):
        '''Define rotation animation of the object
        '''
        self._rotation_animation = animation
    
    def set_scale_animation(self, animation: Animation):
        '''Define scale animation of the object
        '''
        self._scale_animation = animation
    
    def add_mesh_component(self, mesh: MeshComponent):
        '''Add mesh component to the object
        Each object can contains several mesh components
        '''
        self._meshes.append(mesh)

    def get_id(self) -> int:
        '''Return id of the object
        '''
        return self._id
    
    def get_name(self) -> str:
        '''Return name of the object
        '''
        return self._name
    
    def get_transform(self) -> Transform:
        '''Return transformation matrix of the object
        '''
        return self._transform

    def get_translation(self) -> tuple[float, float, float]:
        '''Return translation of the object
        '''
        return self._translation
    
    def get_rotation(self) -> tuple[float, float, float, float]:
        '''Return rotation of the object
        '''
        return self._rotation
    
    def get_scale(self) -> tuple[float, float, float]:
        '''Return scale of the object
        '''
        return self._scale

    def is_camera(self) -> bool:
        '''Return True if the object contains camera component, False otherwise
        '''
        return self._camera is not None
    
    def get_camera(self) -> Optional[CameraComponent]:
        '''Return camera component of the object
        If it does not assigned, then return None
        '''
        return self._camera
    
    def is_light(self) -> bool:
        '''Return True if the object contains light component, False otherwise
        '''
        return self._light is not None
    
    def get_light(self) -> Optional[LightComponent]:
        '''Return light component of the object
        If it does not assigned, then return None
        '''
        return self._light
    
    def is_mesh(self) -> bool:
        '''Return True if the object contains at least one mesh component, False otherwise
        '''
        return len(self._meshes) > 0
    
    def get_mesh_components(self) -> list[MeshComponent]:
        '''Return the full list of all mesh components of the object
        '''
        return self._meshes

    def get_mesh_components_count(self) -> int:
        '''Return the number of mesh components (i.e. clusters or submeshes) of the object
        '''
        return len(self._meshes)
    
    def get_mesh_component(self, index: int) -> Optional[MeshComponent]:
        '''Return mesh component of the object with specific index
        If the index is invalid, then return None
        '''
        if index < len(self._meshes):
            return self._meshes[index]
        else:
            return None
    
    def get_translation_animation(self) -> Optional[Animation]:
        '''Return translation animation of the object
        If it does node defined, then return None
        '''
        return self._translation_animation
    
    def get_rotation_animation(self) -> Optional[Animation]:
        '''Return rotation animation of the object
        If it does node defined, then return None
        '''
        return self._rotation_animation
    
    def get_scale_animation(self) -> Optional[Animation]:
        '''Return scale animation of the object
        If it does node defined, then return None
        '''
        return self._scale_animation
    
    def get_object_by_id(self, id: int) -> Optional[Object]:
        '''Find and return the object with a given id
        Search in the collection of this object and children sub-objects
        '''
        if self._id == id:
            return self
        for sub_obj in self._children:
            v: Optional[Object] = sub_obj.get_object_by_id(id)
            if v:
                return v
        return None
    
    def get_subobjects_count(self) -> int:
        return len(self._children)
    
    def get_children(self) -> list[Object]:
        return self._children

    def __str__(self) -> str:
        children_list: list[str] = []
        for child in self._children:
            child_str = str(child)
            child_list = child_str.split("\n")
            for i in range(len(child_list)):
                child_list[i] = "  " + child_list[i]
            children_list.extend(child_list)
        children_list = list(filter(lambda s: len(s) > 0, children_list))
        return "\n".join([f"{self._name}({self._id})"] + children_list)

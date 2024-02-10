from typing import Optional
from py3dscene.material import PBRMaterial
from py3dscene.object import Object

class Scene:
    '''Main class for store 3d-scene data
    '''
    def __init__(self) -> None:
        self._materials: list[PBRMaterial] = []
        self._objects: list[Object] = []

    def create_material(self, name: str="", id: Optional[int]=None) -> PBRMaterial:
        '''Create and return material
        It's recommended to create materials by this method
        It automatically add material to the list in the scene object
        '''
        material: PBRMaterial = PBRMaterial(name, id)
        self._materials.append(material)
        return material
    
    def get_material(self, id: int) -> PBRMaterial:
        '''Return material with a given id
        '''
        return self._materials[id]
    
    def create_object(self, name: str="", id: Optional[int]=None) -> Object:
        '''Create and return new object. This object parented to the root of the scene
        It's possible to define the custom id for the new object
        '''
        new_object = Object(name, id)
        self._objects.append(new_object)
        return new_object
    
    def get_object_by_id(self, id: int) -> Optional[Object]:
        '''Return object with a given id
        If there are no such object return None
        '''
        for obj in self._objects:
            v: Optional[Object] = obj.get_object_by_id(id)
            if v:
                return v
        return None
    
    def get_objects_count(self) -> int:
        '''Return the number of objects in the root level of the scene
        '''
        return len(self._objects)
    
    def get_root_objects(self) -> list[Object]:
        '''Return the list with objects in the root level of the scene
        '''
        return self._objects
    
    def __str__(self) -> str:
        objects_list: list[str] = []
        for obj in self._objects:
            obj_str = str(obj)
            obj_list = obj_str.split("\n")
            for i in range(len(obj_list)):
                obj_list[i] = "  " + obj_list[i]
            objects_list.extend(obj_list)
        objects_list = list(filter(lambda s: len(s) > 0, objects_list))

        materials_list: list[str] = []
        for mat in self._materials:
            materials_list.append(f"  {str(mat)}({mat.get_id()})")
        return "\n".join(["Objects:"] + objects_list + ["Materials:"] + materials_list)

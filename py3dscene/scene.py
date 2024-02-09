from typing import Optional
from py3dscene.material import PBRMaterial
from py3dscene.object import Object

class Scene:
    def __init__(self) -> None:
        self._materials: list[PBRMaterial] = []
        self._objects: list[Object] = []

    def add_material(self, material: PBRMaterial):
        self._materials.append(material)
    
    def get_material(self, id: int) -> PBRMaterial:
        return self._materials[id]
    
    def create_object(self, name: str="", id: Optional[int]=None) -> Object:
        new_object = Object(name, id)
        self._objects.append(new_object)
        return new_object
    
    def get_object_by_id(self, id: int) -> Optional[Object]:
        for obj in self._objects:
            v: Optional[Object] = obj.get_object_by_id(id)
            if v:
                return v
        return None
    
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

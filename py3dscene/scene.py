from typing import Optional
from py3dscene.material import PBRMaterial
from py3dscene.object import Object

class Scene:
    def __init__(self) -> None:
        self._materials: dict[int, PBRMaterial] = {}
        self._objects: list[Object] = []

    def add_material(self, material: PBRMaterial, id: int):
        self._materials[id] = material
    
    def get_material(self, id: int) -> PBRMaterial:
        return self._materials[id]
    
    def create_object(self, name: str="", id: Optional[int]=None) -> Object:
        new_object = Object(name, id)
        self._objects.append(new_object)
        return new_object
    
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
        for id, mat in self._materials.items():
            materials_list.append(f"  {str(mat)}({id})")
        return "\n".join(["Objects:"] + objects_list + ["Materials:"] + materials_list)

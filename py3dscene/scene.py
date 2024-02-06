from py3dscene.material import PBRMaterial
from py3dscene.object import Object

class Scene:
    def __init__(self) -> None:
        self._materials: dict[int, PBRMaterial] = {}

    def add_material(self, material: PBRMaterial, id: int):
        self._materials[id] = material
    
    def get_material(self, id: int) -> PBRMaterial:
        return self._materials[id]
    
    def create_object(self, name: str="") -> Object:
        print("create object", name)
        return Object()

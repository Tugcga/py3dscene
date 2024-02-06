from py3dscene.material import Material
from py3dscene.object import Object

class Scene:
    def __init__(self):
        pass

    def add_material(self, material: Material):
        print("add material to the scene")
    
    def create_object(self, name: str="") -> Object:
        print("create object", name)
        return Object()

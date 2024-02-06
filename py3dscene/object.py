from __future__ import annotations  # remove for Python 3.11
from typing import Optional
from py3dscene.transform import Transform
from py3dscene.transform import get_identity

class Object:
    id_pointer: int = 0

    def __init__(self, name: str="", id: Optional[int]=None) -> None:
        self._name: str = name if len(name) > 0 else "unnamed"
        self._children: list[Object] = []
        if id is None:
            self._id: int = Object.id_pointer
            Object.id_pointer += 1
        else:
            self._id = id
        self._transform: Transform = get_identity()
    
    def create_subobject(self, name: str="", id: Optional[int]=None) -> Object:
        new_object: Object = Object(name, id)
        self._children.append(new_object)
        return new_object
    
    def assign_local_tfm(self, tfm: Transform):
        self._transform = tfm

    def get_id(self) -> int:
        return self._id
    
    def get_name(self) -> str:
        return self._name

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

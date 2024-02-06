from __future__ import annotations  # remove for Python 3.11
from py3dscene.transform import Transform

class Object:
    def __init__(self) -> None:
        pass
    
    def create_subobject(self, name: str="") -> Object:
        return Object()
    
    def assign_local_tfm(self, tfm: Transform):
        pass

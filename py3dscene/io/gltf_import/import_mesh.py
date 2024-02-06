from py3dscene.bin.tiny_gltf import Model as GLTFModel  # type: ignore
from py3dscene.bin.tiny_gltf import Mesh as GLTFMesh  # type: ignore
from py3dscene.object import Object
from py3dscene.material import PBRMaterial

def import_object_mesh(gltf_model: GLTFModel,
                       gltf_mesh: GLTFMesh,
                       object: Object,
                       materials_map: dict[int, PBRMaterial],
                       envelop_map: dict[int, list[float]]):
    pass
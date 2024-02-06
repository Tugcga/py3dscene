from py3dscene.bin.tiny_gltf import Model as GLTFModel  # type: ignore
from py3dscene.object import Object

def import_object_skin(gltf_model: GLTFModel,
                       object: Object,
                       skin_index: int,
                       envelope_data: dict[int, list[float]],
                       nodes_map: dict[int, Object]):
    print("import skin", skin_index)

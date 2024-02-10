from py3dscene.bin.tiny_gltf import Model as GLTFModel  # type: ignore
from py3dscene.object import Object

def export_skin(gltf_model: GLTFModel,
                skin_index: int,
                object: Object,
                object_to_node: dict[int, int]):
    pass
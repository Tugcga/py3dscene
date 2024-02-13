from py3dscene.bin import tiny_gltf
from py3dscene.object import Object

def export_skin(gltf_model_skins: list[tiny_gltf.Skin],
                skin_index: int,
                object: Object,
                object_to_node: dict[int, int]):
    pass
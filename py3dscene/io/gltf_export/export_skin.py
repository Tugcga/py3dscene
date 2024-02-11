from py3dscene.bin.tiny_gltf import Skin as GLTFSkin  # type: ignore
from py3dscene.object import Object

def export_skin(gltf_model_skins: list[GLTFSkin],
                skin_index: int,
                object: Object,
                object_to_node: dict[int, int]):
    pass
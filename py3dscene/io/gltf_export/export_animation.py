from py3dscene.bin.tiny_gltf import Sampler as GLTFSampler  # type: ignore
from py3dscene.bin.tiny_gltf import Animation as GLTFAnimation  # type: ignore

def export_animation(gltf_model_animations: list[GLTFAnimation],
                     gltf_model_samplers: list[GLTFSampler],
                     object_to_node: dict[int, int]):
    pass

from py3dscene.bin.tiny_gltf import Node as GLTFNode  # type: ignore
from py3dscene.transform import Transform

def export_transform(gltf_node: GLTFNode,
                     tfm: Transform,
                     translation: tuple[float, float, float],
                     rotation: tuple[float, float, float, float],
                     scale: tuple[float, float, float]):
    # we use separate SRT from transform matrix
    # Warning: if we would like to use matrix, then we should transpose it
    # because glTF format use row-oriented matrix (instead of column-oriented in our case)
    gltf_node.translation = list(translation)
    gltf_node.rotation = list(rotation)
    gltf_node.scale = list(scale)

from py3dscene.bin import tiny_gltf
from py3dscene.transform import Transform

def export_transform(gltf_node: tiny_gltf.Node,
                     tfm: Transform,
                     translation: tuple[float, float, float],
                     rotation: tuple[float, float, float, float],
                     scale: tuple[float, float, float]) -> None:
    # we use separate SRT from transform matrix
    # Warning: if we would like to use matrix, then we should transpose it
    # because glTF format use row-oriented matrix (instead of column-oriented in our case)
    gltf_node.translation = list(translation)
    gltf_node.rotation = list(rotation)
    gltf_node.scale = list(scale)

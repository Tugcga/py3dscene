from py3dscene.bin.tiny_gltf import Node as GLTFNode  # type: ignore
from py3dscene.transform import Transform 

def import_transform(gltf_node: GLTFNode) -> Transform:
    return ((1.0, 0.0, 0.0, 0.0),
            (0.0, 1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0, 0.0),
            (0.0, 0.0, 0.0, 1.0))

from py3dscene.bin.tiny_gltf import Node as GLTFNode  # type: ignore
from py3dscene.transform import Transform
from py3dscene.transform import get_srt_matrix

'''GLTF use matrix for transforms where the last column is (0.0, 0.0, 0.0, 1.0)
It means that to apply the transform we should multiply the row with coordinates (x, y, z) ito matrix
in the form: (x, y, z) * T
So, each row of T is a vector with coordinates of the axis after transformation

More often transformation matrix used when coordinates places into columns
In this case we should multiply is as T * (x, y, z)^t
Also the last row is zero (0.0, 0.0, 0.0, 1.0), and the last column contains position of the origin after transform

We will be use the second approach
'''

def import_transform(gltf_node: GLTFNode) -> Transform:
    gltf_mat = gltf_node.matrix
    if len(gltf_mat) == 0:
        gltf_translation: list[float] = gltf_node.translation
        gltf_rotation: list[float] = gltf_node.rotation
        gltf_scale: list[float] = gltf_node.scale
        return get_srt_matrix((gltf_translation[0], gltf_translation[1], gltf_translation[2]) if len(gltf_translation) > 0 else (0.0, 0.0, 0.0),
                              (gltf_rotation[0], gltf_rotation[1], gltf_rotation[2], gltf_rotation[3]) if len(gltf_rotation) > 0 else (0.0, 0.0, 0.0, 1.0),
                              (gltf_scale[0], gltf_scale[1], gltf_scale[2]) if len(gltf_scale) > 0 else (1.0, 1.0, 1.0))
    else:
        return ((gltf_mat[0], gltf_mat[4], gltf_mat[8], gltf_mat[12]),
                (gltf_mat[1], gltf_mat[5], gltf_mat[9], gltf_mat[13]),
                (gltf_mat[2], gltf_mat[6], gltf_mat[10], gltf_mat[14]),
                (gltf_mat[3], gltf_mat[7], gltf_mat[11], gltf_mat[15]))

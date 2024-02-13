from py3dscene.bin import tiny_gltf
from py3dscene.object import Object

def import_object_skin(gltf_model: tiny_gltf.Model,
                       object: Object,
                       skin_index: int,
                       envelope_data: dict[int, list[float]],
                       nodes_map: dict[int, Object]) -> None:
    # TODO: implement skin import
    pass

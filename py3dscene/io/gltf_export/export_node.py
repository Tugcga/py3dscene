from typing import Optional
from py3dscene.bin.tiny_gltf import Node as GLTFNode  # type: ignore
from py3dscene.io.gltf_export.export_transform import export_transform
from py3dscene.io.gltf_export.export_mesh import export_mesh
from py3dscene.object import Object

def export_node(object: Object,
                materials_map: dict[int, int],
	            textures_map: dict[int, int],
	            envelope_meshes: list[Object]) -> Optional[GLTFNode]:
    new_node: GLTFNode = GLTFNode()
    new_node.name = object.get_name()

    # TODO: skip export transform for skinned mesh object
    export_transform(new_node,
                     object.get_transform(),
                     object.get_translation(),
                     object.get_rotation(),
                     object.get_scale())
    
    if object.get_mesh_components_count() > 0:
        export_mesh(new_node, object, materials_map, textures_map, envelope_meshes)

    return new_node
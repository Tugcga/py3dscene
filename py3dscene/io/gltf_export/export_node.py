from typing import Optional
from py3dscene.bin import tiny_gltf
from py3dscene.io.gltf_export.export_transform import export_transform
from py3dscene.io.gltf_export.export_mesh import export_mesh
from py3dscene.object import Object

def export_node(object: Object,
                gltf_model_buffers_data: list[int],
                gltf_model_buffer_views: list[tiny_gltf.BufferView],
                gltf_model_accessors: list[tiny_gltf.Accessor],
                gltf_model_meshes: list[tiny_gltf.Mesh],
                materials_map: dict[int, int],
	            envelope_meshes: list[Object],
                optimize_mesh_nodes: bool) -> Optional[tiny_gltf.Node]:
    new_node = tiny_gltf.Node()
    new_node.name = object.get_name()

    # TODO: skip export transform for skinned mesh object
    export_transform(new_node,
                     object.get_transform(),
                     object.get_translation(),
                     object.get_rotation(),
                     object.get_scale())
    
    if object.get_mesh_components_count() > 0:
        export_mesh(gltf_model_buffers_data,
                    gltf_model_buffer_views,
                    gltf_model_accessors,
                    gltf_model_meshes,
                    new_node,
                    object,
                    materials_map,
                    envelope_meshes,
                    optimize_mesh_nodes)

    return new_node
from typing import Optional
from py3dscene.bin.tiny_gltf import Node as GLTFNode  # type: ignore
from py3dscene.bin.tiny_gltf import Mesh as GLTFMesh  # type: ignore
from py3dscene.bin.tiny_gltf import BufferView as GLTFBufferView  # type: ignore
from py3dscene.bin.tiny_gltf import Accessor as GLTFAccessor  # type: ignore
from py3dscene.io.gltf_export.export_transform import export_transform
from py3dscene.io.gltf_export.export_mesh import export_mesh
from py3dscene.object import Object

def export_node(object: Object,
                gltf_model_buffers_data: list[int],
                gltf_model_buffer_views: list[GLTFBufferView],
                gltf_model_accessors: list[GLTFAccessor],
                gltf_model_meshes: list[GLTFMesh],
                materials_map: dict[int, int],
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
        export_mesh(gltf_model_buffers_data,
                    gltf_model_buffer_views,
                    gltf_model_accessors,
                    gltf_model_meshes,
                    new_node,
                    object,
                    materials_map,
                    envelope_meshes)

    return new_node
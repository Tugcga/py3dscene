from typing import Optional
from py3dscene.bin import tiny_gltf
from py3dscene.io.gltf_export.export_camera import export_camera
from py3dscene.io.gltf_export.export_light import export_light
from py3dscene.io.gltf_export.export_node import export_node
from py3dscene.object import Object

def export_iterate(gltf_model_buffers_data: list[int],
                   gltf_model_buffer_views: list[tiny_gltf.BufferView],
                   gltf_model_accessors: list[tiny_gltf.Accessor],
                   gltf_model_nodes: list[tiny_gltf.Node],
                   gltf_model_cameras: list[tiny_gltf.Camera],
                   gltf_model_lights: list[tiny_gltf.Light],
                   gltf_model_meshes: list[tiny_gltf.Mesh],
                   object: Object,
                   exported_objects: set[int],
	               materials_map: dict[int, int],
	               envelope_meshes: list[Object],
	               object_to_node: dict[int, int],
                   optimize_mesh_nodes: bool) -> int:
    node_index: int = -1
    gltf_node: Optional[tiny_gltf.Node] = None
    object_id: int = object.get_id()
    if object_id in exported_objects:
        return -1

    if object.is_camera():
        camera = object.get_camera()
        if camera:
            gltf_node = export_camera(camera, object, gltf_model_cameras)
    elif object.is_light():
        light = object.get_light()
        if light:
            gltf_node = export_light(light, object, gltf_model_lights)
    else:
        gltf_node = export_node(object,
                                gltf_model_buffers_data,
                                gltf_model_buffer_views,
                                gltf_model_accessors,
                                gltf_model_meshes,
                                materials_map,
                                envelope_meshes,
                                optimize_mesh_nodes)

    if gltf_node:
        exported_objects.add(object_id)
        node_index = len(gltf_model_nodes)
        gltf_model_nodes.append(gltf_node)
        object_to_node[object_id] = node_index

        gltf_node_children: list[int] = []
        for child in object.get_children():
            child_index = export_iterate(gltf_model_buffers_data,
                                         gltf_model_buffer_views,
                                         gltf_model_accessors,
                                         gltf_model_nodes,
                                         gltf_model_cameras,
                                         gltf_model_lights,
                                         gltf_model_meshes,
                                         child,
                                         exported_objects,
                                         materials_map,
                                         envelope_meshes,
                                         object_to_node,
                                         optimize_mesh_nodes)
            if child_index >= 0:
                gltf_node_children.append(child_index)
        
            gltf_node.children = gltf_node_children
    return node_index
from typing import Optional
from py3dscene.bin.tiny_gltf import Model as GLTFModel  # type: ignore
from py3dscene.bin.tiny_gltf import Node as GLTFNode  # type: ignore
from py3dscene.bin.tiny_gltf import Mesh as GLTFMesh  # type: ignore
from py3dscene.bin.tiny_gltf import Camera as GLTFCamera  # type: ignore
from py3dscene.bin.tiny_gltf import Light as GLTFLight  # type: ignore
from py3dscene.scene import Scene
from py3dscene.object import Object
from py3dscene.material import PBRMaterial

from py3dscene.io.gltf_import.import_transform import import_transform
from py3dscene.io.gltf_import.import_mesh import import_object_mesh
from py3dscene.io.gltf_import.import_camera import import_object_camera
from py3dscene.io.gltf_import.import_light import import_object_light

def process_node(gltf_model: GLTFModel,
                 gltf_node: GLTFNode,
                 model_buffers_data: list[list[int]],
                 gltf_node_index: int,
                 scene: Scene,
                 parent: Optional[Object],
                 materials_map: dict[int, PBRMaterial],
                 nodes_map: dict[int, Object],
                 envelopes: list[tuple[int, Object, dict[int, list[float]]]]):
    local_tfm = import_transform(gltf_node)
    object_name = gltf_node.name
    # create new object
    if parent is None:
        object = scene.create_object(object_name, gltf_node_index)
    else:
        object = parent.create_subobject(object_name, gltf_node_index)
    
    # assign local transform
    object.set_local_tfm(local_tfm)
    
    if gltf_node.mesh >= 0 and gltf_node.mesh < len(gltf_model.meshes):
        # current node contains a mesh component
        gltf_mesh: GLTFMesh = gltf_model.meshes[gltf_node.mesh]
        envelop_map: dict[int, list[float]] = {}
        import_object_mesh(gltf_model, gltf_mesh, model_buffers_data, object, materials_map, envelop_map)

        if gltf_node.skin > 0 and len(envelop_map.keys()) > 0:
            envelopes.append((gltf_node.skin, object, envelop_map))
    elif gltf_node.camera >= 0 and gltf_node.camera < len(gltf_model.cameras):
        # current node is a camera
        gltf_camera: GLTFCamera = gltf_model.cameras[gltf_node.camera]
        import_object_camera(gltf_camera, object)
    elif gltf_node.light >= 0 and gltf_node.light < len(gltf_model.lights):
        # current node is a light
        gltf_light: GLTFLight = gltf_model.lights[gltf_node.light]
        import_object_light(gltf_light, object)
    
    nodes_map[gltf_node_index] = object

    for i in range(len(gltf_node.children)):
        process_node(gltf_model,
                     gltf_model.nodes[gltf_node.children[i]],
                     model_buffers_data,
                     gltf_node.children[i],
                     scene,
                     object,
                     materials_map,
                     nodes_map,
                     envelopes)

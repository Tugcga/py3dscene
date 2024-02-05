from typing import Optional
from py3dscene.scene import Scene
from py3dscene.transform import Transform  # type: ignore
from py3dscene.material import Material  # type: ignore
from py3dscene.object import Object  # type: ignore
from py3dscene.bin.tiny_gltf import load_gltf  # type: ignore
from py3dscene.bin.tiny_gltf import Scene as GLTFScene
from py3dscene.bin.tiny_gltf import Model as GLTFModel
from py3dscene.bin.tiny_gltf import Material as GLTFMaterial
from py3dscene.bin.tiny_gltf import Node as GLTFNode
from py3dscene.bin.tiny_gltf import Mesh as GLTFMesh
from py3dscene.bin.tiny_gltf import Camera as GLTFCamera
from py3dscene.bin.tiny_gltf import Light as GLTFLight

def import_images(gltf_model: GLTFModel,
                  gltf_scene: GLTFScene,
                  file_path: str) -> dict[int, str]:
    '''Read images from gltf container and store it in a separate folder
    The folder to store images is located near input file_path and named 'textures'
    Return the dictionary with key - image index in gltf, value - path to the corresponding image file
    '''
    print("import images")
    return {}

def import_material(gltf_model: GLTFModel,
                    gltf_material: GLTFMaterial,
                    material_index: int,
                    images_map: dict[int, str]) -> Material:
    '''Read and return one material with index material_index from gltf
    '''
    print("import material")
    return Material()

def import_transform(gltf_node: GLTFNode) -> Transform:
    return ((1.0, 0.0, 0.0, 0.0),
            (0.0, 1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0, 0.0),
            (0.0, 0.0, 0.0, 1.0))

def import_mesh(gltf_model: GLTFModel,
                gltf_mesh: GLTFMesh,
                object: Object,
                materials_map,
                envelop_map: dict[int, list[float]]):
    pass

def import_camera(gltf_model: GLTFModel,
                  gltf_camera: GLTFCamera,
                  object: Object):
    pass

def import_light(gltf_model: GLTFModel,
                 gltf_light: GLTFLight,
                 object: Object):
    pass

def process_node(gltf_model: GLTFModel,
                 gltf_node: GLTFNode,
                 gltf_node_index: int,
                 scene: Scene,
                 parent: Optional[Object],
                 materials_map: dict[int, Material],
                 nodes_map: dict[int, Object],
                 envelopes: list[tuple[int, Object, dict[int, list[float]]]]):
    print("import node", gltf_node_index)
    local_tfm = import_transform(gltf_node)
    object_name = gltf_node.name
    # create new object
    if parent is None:
        object = scene.create_object(object_name)
    else:
        object = parent.create_subobject(object_name)
    
    # assign local transform
    object.assign_local_tfm(local_tfm)

    if gltf_node.mesh >= 0 and gltf_node.mesh < len(gltf_model.meshes):
        # current node contains a mesh component
        gltf_mesh: GLTFMesh = gltf_model.meshes[gltf_node.mesh]
        envelop_map: dict[int, list[float]] = {}
        import_mesh(gltf_model, gltf_mesh, object, materials_map, envelop_map)

        if gltf_node.skin > 0 and len(envelop_map.keys()) > 0:
            envelopes.append((gltf_node.skin, object, envelop_map))
    elif gltf_node.camera >= 0 and gltf_node.camera < len(gltf_model.cameras):
        # current node is a camera
        gltf_camera: GLTFCamera = gltf_model.cameras[gltf_node.camera]
        import_camera(gltf_model, gltf_camera, object)
    elif gltf_node.light >= 0 and gltf_node.light < len(gltf_model.lights):
        # current node is a light
        gltf_light: GLTFLight = gltf_model.lights[gltf_node.light]
        import_light(gltf_model, gltf_light, object)
    
    nodes_map[gltf_node_index] = object

    for i in range(len(gltf_node.children)):
        process_node(gltf_model, gltf_model.nodes[gltf_node.children[i]], gltf_node.children[i], scene, object, materials_map, nodes_map, envelopes)

def import_skin(gltf_model: GLTFModel,
                object: Object,
                skin_index: int,
                envelope_data: dict[int, list[float]],
                nodes_map: dict[int, Object]):
    print("import skin", skin_index)

def import_animation(gltf_model: GLTFModel,
                     nodes_map: dict[int, Object]):
    pass

def from_gltf(file_path: str) -> Scene:
    '''Create and return Scene object, which contains default scene from input gltf/glb file
    '''
    gltf_model: GLTFModel = load_gltf(file_path)
    gltf_scene: GLTFScene = gltf_model.scenes[gltf_model.default_scene if gltf_model.default_scene > -1 else 0]

    scene: Scene = Scene()

    # at first import images
    images_map: dict[int, str] = import_images(gltf_model, gltf_scene, file_path)

    # next materials
    materials_map: dict[int, Material] = {}
    for material_index in range(len(gltf_model.materials)):
        gltf_material: GLTFMaterial = gltf_model.materials[material_index]
        material = import_material(gltf_model, gltf_material, material_index, images_map)
        materials_map[material_index] = material
        # add material to the scene
        scene.add_material(material)
    
    # next read scene nodes
    nodes_map: dict[int, Object] = {}
    envelopes: list[tuple[int, Object, dict[int, list[float]]]] = []
    for i in range(len(gltf_scene.nodes)):
        process_node(gltf_model, gltf_model.nodes[gltf_scene.nodes[i]], gltf_scene.nodes[i], scene, None, materials_map, nodes_map, envelopes)
    
    # after nodes import skin data
    for i in range(len(envelopes)):
        envelop_data: tuple[int, Object, dict[int, list[float]]] = envelopes[i]
        import_skin(gltf_model, envelopes[1], envelop_data[0], envelop_data[2], nodes_map)
    
    # finally animations
    import_animation(gltf_model, nodes_map)

    return scene
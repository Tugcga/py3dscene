import os
from py3dscene.scene import Scene
from py3dscene.material import PBRMaterial
from py3dscene.object import Object
from py3dscene.bin.tiny_gltf import load_gltf  # type: ignore
from py3dscene.bin.tiny_gltf import save_gltf  # type: ignore
from py3dscene.bin.tiny_gltf import Scene as GLTFScene  # type: ignore
from py3dscene.bin.tiny_gltf import Model as GLTFModel  # type: ignore
from py3dscene.bin.tiny_gltf import Material as GLTFMaterial  # type: ignore
from py3dscene.bin.tiny_gltf import Buffer as GLTFBuffer  # type: ignore
from py3dscene.bin.tiny_gltf import Asset as GLTFAsset  # type: ignore
from py3dscene.bin.tiny_gltf import Node as GLTFNode  # type: ignore
from py3dscene.bin.tiny_gltf import Camera as GLTFCamera  # type: ignore
from py3dscene.bin.tiny_gltf import Light as GLTFLight  # type: ignore
from py3dscene.io.gltf_import.import_image import import_images
from py3dscene.io.gltf_import.import_material import import_material
from py3dscene.io.gltf_import.import_object import process_node
from py3dscene.io.gltf_import.import_skin import import_object_skin
from py3dscene.io.gltf_import.import_animation import import_animations
from py3dscene.io.gltf_export.export_object import export_iterate
from py3dscene.io.gltf_export.export_skin import export_skin
from py3dscene.io.gltf_export.export_animation import export_animation

def from_gltf(file_path: str, fps: float=30.0) -> Scene:
    '''Create and return Scene object, which contains default scene from input gltf/glb file
    Parameter fps is used for animations
    glTF format store animation keyframes in seconds, but more traditional way is to store it in frames
    parameter fps used to convert seconds-related values to frame-related values
    '''
    gltf_model: GLTFModel = load_gltf(file_path)
    gltf_scene: GLTFScene = gltf_model.scenes[gltf_model.default_scene if gltf_model.default_scene > -1 else 0]

    scene: Scene = Scene()

    # at first import images
    images_map: dict[int, str] = import_images(gltf_model, gltf_scene, file_path)

    # next materials
    # key is material id = index in gltf
    materials_map: dict[int, PBRMaterial] = {}
    for material_index in range(len(gltf_model.materials)):
        gltf_material: GLTFMaterial = gltf_model.materials[material_index]
        material = import_material(gltf_material, scene, material_index, images_map)
        materials_map[material.get_id()] = material
    
    # next read scene nodes
    nodes_map: dict[int, Object] = {}
    # each envelope data is a tuple:
    #   - skin index
    #   - object with this skin
    #   - dictionary with
    #       key - scene node index
    #       value - weights for the mesh
    envelopes: list[tuple[int, Object, dict[int, list[float]]]] = []
    for i in range(len(gltf_scene.nodes)):
        process_node(gltf_model, gltf_model.nodes[gltf_scene.nodes[i]], gltf_scene.nodes[i], scene, None, materials_map, nodes_map, envelopes)
    
    # after nodes import skin data
    # TODO: implement store object skinning
    for i in range(len(envelopes)):
        envelop_data: tuple[int, Object, dict[int, list[float]]] = envelopes[i]
        import_object_skin(gltf_model, envelop_data[1], envelop_data[0], envelop_data[2], nodes_map)
    
    # finally animations
    import_animations(gltf_model, nodes_map, fps)

    return scene

def to_gltf(scene: Scene,
            file_path: str,
            embed_images: bool=False,
            embed_buffers: bool=False,
            fps: float=30.0):
    # extract output extension
    ext_str: str = file_path.split(".")[-1].lower()
    if ext_str not in ["glb", "gltf"]:
        return None
    
    # extract output folder
    file_path_norm: str = file_path.replace("/", "\\")
    folder_path: str = "\\".join(file_path_norm.split("\\")[:-1])  # store without last \\

    # create output folder
    os.makedirs(folder_path, exist_ok=True)

    # extract file name without extension
    file_name: str = file_path_norm.split("\\")[-1].split(".")[0]
    
    # store here id's of exported objects
    exported_objects: set[int] = set()
    gltf_model = GLTFModel()
    gltf_scene = GLTFScene()
    
    materials_map: dict[int, int] = {}  # key - material object id, value - index in the gltf materials list
    textures_map: dict[int, int] = {}  # key - image clip id, value - index of the texture in the gltf textures list
    envelope_meshes: list[Object] = []
    object_to_node: dict[int, int] = {}  # map from scene object id to gltf node index

    data_buffer: GLTFBuffer = GLTFBuffer()
    gltf_model.buffers = [data_buffer]
    gltf_scene_nodes: list[int] = []
    gltf_model_nodes: list[GLTFNode] = []
    gltf_model_cameras: list[GLTFCamera] = []
    gltf_model_lights: list[GLTFLight] = []

    for obj in scene.get_root_objects():
        scene_node_index: int = export_iterate(gltf_model_nodes, gltf_model_cameras, gltf_model_lights, obj, exported_objects, materials_map, textures_map, envelope_meshes, object_to_node)
        if scene_node_index >= 0:
            gltf_scene_nodes.append(scene_node_index)
    gltf_scene.nodes = gltf_scene_nodes
    gltf_model.nodes = gltf_model_nodes
    gltf_model.cameras = gltf_model_cameras
    gltf_model.lights = gltf_model_lights

    for i in range(len(envelope_meshes)):
        export_skin(gltf_model, i, envelope_meshes[i], object_to_node)
    
    export_animation(gltf_model, object_to_node)

    gltf_scene.name = file_name
    gltf_model.scenes = [gltf_scene]
    gltf_model.default_scene = 0

    gltf_asset: GLTFAsset = GLTFAsset()
    gltf_asset.version = "2.0"
    gltf_asset.generator = "py3dscene"
    gltf_model.asset = gltf_asset

    save_gltf(gltf_model,
              file_path,
              embed_images,
              embed_buffers,
              True,
              ext_str == "glb")

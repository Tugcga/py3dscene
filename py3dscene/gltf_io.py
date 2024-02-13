import os
from py3dscene.bin import tiny_gltf
from py3dscene.scene import Scene
from py3dscene.material import PBRMaterial
from py3dscene.object import Object
from py3dscene.io.gltf_import.import_image import import_images
from py3dscene.io.gltf_import.import_material import import_material
from py3dscene.io.gltf_import.import_object import process_node
from py3dscene.io.gltf_import.import_skin import import_object_skin
from py3dscene.io.gltf_import.import_animation import import_animations
from py3dscene.io.gltf_export.export_object import export_iterate
from py3dscene.io.gltf_export.export_skin import export_skin
from py3dscene.io.gltf_export.export_animation import export_animation
from py3dscene.io.gltf_export.export_material import export_materials

def from_gltf(file_path: str, fps: float=30.0) -> Scene:
    '''Create and return Scene object, which contains default scene from input gltf/glb file
    Parameter fps is used for animations
    glTF format store animation keyframes in seconds, but more traditional way is to store it in frames
    parameter fps used to convert seconds-related values to frame-related values
    '''
    gltf_model = tiny_gltf.load_gltf(file_path)
    gltf_scene = gltf_model.scenes[gltf_model.default_scene if gltf_model.default_scene > -1 else 0]
    model_buffers_data: list[list[int]] = []
    model_buffers: list[tiny_gltf.Buffer] = gltf_model.buffers
    for i in range(len(model_buffers)):
        gltf_buffer = model_buffers[i]
        model_buffers_data.append(gltf_buffer.data)

    scene: Scene = Scene()

    # at first import images
    images_map: dict[int, str] = import_images(gltf_model, file_path)

    # next materials
    # key is material id = index in gltf
    materials_map: dict[int, PBRMaterial] = {}
    for material_index in range(len(gltf_model.materials)):
        gltf_material = gltf_model.materials[material_index]
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
        process_node(gltf_model,
                     gltf_model.nodes[gltf_scene.nodes[i]],
                     model_buffers_data,
                     gltf_scene.nodes[i],
                     scene,
                     None,
                     materials_map,
                     nodes_map, envelopes)
    
    # after nodes import skin data
    # TODO: implement store object skinning
    for i in range(len(envelopes)):
        envelop_data: tuple[int, Object, dict[int, list[float]]] = envelopes[i]
        import_object_skin(gltf_model, envelop_data[1], envelop_data[0], envelop_data[2], nodes_map)
    
    # finally animations
    import_animations(gltf_model, model_buffers_data, nodes_map, fps)

    return scene

def to_gltf(scene: Scene,
            file_path: str,
            optimize_mesh_nodes: bool=False,
            embed_images: bool=False,
            embed_buffers: bool=False,
            fps: float=30.0):
    '''Export scene object as gltf or glb file
    Parameters:
    file_path: full output path with extension
    optimize_mesh_nodes: if True, then in the export process the module try to reduce the number of vertices in the output meshes
        in the mesh it's possible to have one vertex and different normals in polygons incident to this vertex
        if optimization is ON, then the exporter check is polygon nodes have different attributes or not
        if at least one attribute (position, normal, uv etc) is different, then it creates the new vertex
        if all attributes the same, then use the same vertex
        but this process is long for dense mesh
        so, it's possible to deactivate this flag
        it the flag is False then the output mesh have the same vertices as it is, node attributes are override by last node
        if the mesh is imported from glTF, then it's ok, because all vertices already are splitted by difference in node attributes
    embed_images: if True then embed image data into output file and does not create separate texture files
        if False then textures are stored in the same directory as the output file
    embed_buffers: if True then hte binary buffer is embedded into output file
        if False then create the separate file *.bin
    fps: the number of frames per second for exporting animations
        in 3d-scene animations are stored by using key-frames, but in glTF it use seconds
        so, fps used for converting frames to seconds
    '''
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
    gltf_model = tiny_gltf.Model()
    gltf_scene = tiny_gltf.Scene()
    
    materials_map: dict[int, int] = {}  # key - material object id, value - index in the gltf materials list
    envelope_meshes: list[Object] = []
    object_to_node: dict[int, int] = {}  # map from scene object id to gltf node index

    gltf_scene_nodes: list[int] = []
    gltf_model_nodes: list[tiny_gltf.Node] = []
    gltf_model_cameras: list[tiny_gltf.Camera] = []
    gltf_model_lights: list[tiny_gltf.Light] = []
    gltf_model_meshes: list[tiny_gltf.Mesh] = []
    gltf_model_buffers_data: list[int] = []
    gltf_model_buffer_views: list[tiny_gltf.BufferView] = []
    gltf_model_accessors: list[tiny_gltf.Accessor] = []
    gltf_model_materials: list[tiny_gltf.Material] = []
    gltf_model_textures: list[tiny_gltf.Texture] = []
    gltf_model_images: list[tiny_gltf.FImage] = []
    gltf_model_skins: list[tiny_gltf.Skin] = []

    # at the beginning we should export materials and used textures
    export_materials(folder_path,
                     scene.get_all_materials(),
                     gltf_model_materials,
                     gltf_model_textures,
                     gltf_model_images,
                     materials_map)
    gltf_model.materials = gltf_model_materials
    gltf_model.textures = gltf_model_textures
    gltf_model.images = gltf_model_images

    for obj in scene.get_root_objects():
        scene_node_index: int = export_iterate(gltf_model_buffers_data,
                                               gltf_model_buffer_views,
                                               gltf_model_accessors,
                                               gltf_model_nodes,
                                               gltf_model_cameras,
                                               gltf_model_lights,
                                               gltf_model_meshes,
                                               obj,
                                               exported_objects,
                                               materials_map,
                                               envelope_meshes,
                                               object_to_node,
                                               optimize_mesh_nodes)
        if scene_node_index >= 0:
            gltf_scene_nodes.append(scene_node_index)

    gltf_scene.nodes = gltf_scene_nodes
    gltf_model.nodes = gltf_model_nodes
    gltf_model.cameras = gltf_model_cameras
    gltf_model.lights = gltf_model_lights
    gltf_model.meshes = gltf_model_meshes

    for i in range(len(envelope_meshes)):
        export_skin(gltf_model_skins, i, envelope_meshes[i], object_to_node)
    gltf_model.skins = gltf_model_skins
    
    gltf_model_animations: list[tiny_gltf.Animation] = export_animation(gltf_model_buffers_data,
                                                                  gltf_model_buffer_views,
                                                                  gltf_model_accessors,
                                                                  scene,
                                                                  fps,
                                                                  object_to_node)
    if len(gltf_model_animations) > 0:
        gltf_model.animations = gltf_model_animations

    gltf_model.accessors = gltf_model_accessors
    gltf_model.buffer_views = gltf_model_buffer_views

    data_buffer = tiny_gltf.Buffer()
    data_buffer.data = gltf_model_buffers_data
    gltf_model.buffers = [data_buffer]

    gltf_scene.name = file_name
    gltf_model.scenes = [gltf_scene]
    gltf_model.default_scene = 0

    gltf_asset = tiny_gltf.Asset()
    gltf_asset.version = "2.0"
    gltf_asset.generator = "py3dscene"
    gltf_model.asset = gltf_asset

    tiny_gltf.save_gltf(gltf_model,
                        file_path,
                        embed_images,
                        embed_buffers,
                        True,
                        ext_str == "glb")

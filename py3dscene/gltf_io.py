from py3dscene.scene import Scene
from py3dscene.material import PBRMaterial
from py3dscene.object import Object
from py3dscene.bin.tiny_gltf import load_gltf  # type: ignore
from py3dscene.bin.tiny_gltf import Scene as GLTFScene  # type: ignore
from py3dscene.bin.tiny_gltf import Model as GLTFModel  # type: ignore
from py3dscene.bin.tiny_gltf import Material as GLTFMaterial  # type: ignore

from py3dscene.io.gltf_import.import_image import import_images
from py3dscene.io.gltf_import.import_material import import_material
from py3dscene.io.gltf_import.import_node import process_node
from py3dscene.io.gltf_import.import_skin import import_object_skin
from py3dscene.io.gltf_import.import_animation import import_animations

def from_gltf(file_path: str) -> Scene:
    '''Create and return Scene object, which contains default scene from input gltf/glb file
    '''
    gltf_model: GLTFModel = load_gltf(file_path)
    gltf_scene: GLTFScene = gltf_model.scenes[gltf_model.default_scene if gltf_model.default_scene > -1 else 0]

    scene: Scene = Scene()

    # at first import images
    images_map: dict[int, str] = import_images(gltf_model, gltf_scene, file_path)
    print("images map", images_map)

    # next materials
    materials_map: dict[int, PBRMaterial] = {}
    for material_index in range(len(gltf_model.materials)):
        gltf_material: GLTFMaterial = gltf_model.materials[material_index]
        material = import_material(gltf_model, gltf_material, material_index, images_map)
        materials_map[material_index] = material
        # add material to the scene
        # use index as the id
        scene.add_material(material, material_index)
    
    # next read scene nodes
    nodes_map: dict[int, Object] = {}
    envelopes: list[tuple[int, Object, dict[int, list[float]]]] = []
    for i in range(len(gltf_scene.nodes)):
        process_node(gltf_model, gltf_model.nodes[gltf_scene.nodes[i]], gltf_scene.nodes[i], scene, None, materials_map, nodes_map, envelopes)
    
    # after nodes import skin data
    for i in range(len(envelopes)):
        envelop_data: tuple[int, Object, dict[int, list[float]]] = envelopes[i]
        import_object_skin(gltf_model, envelop_data[1], envelop_data[0], envelop_data[2], nodes_map)
    
    # finally animations
    import_animations(gltf_model, nodes_map)

    return scene
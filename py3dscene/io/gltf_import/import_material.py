from py3dscene.bin.tiny_gltf import Model as GLTFModel  # type: ignore
from py3dscene.bin.tiny_gltf import Material as GLTFMaterial  # type: ignore
from py3dscene.material import Material

def import_material(gltf_model: GLTFModel,
                    gltf_material: GLTFMaterial,
                    material_index: int,
                    images_map: dict[int, str]) -> Material:
    material_name = gltf_material.name
    if len(material_name) == 0:
        material_name = "Material_" + str(material_index)
    
    material = Material()
    
    return material

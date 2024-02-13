from py3dscene.bin import tiny_gltf
from py3dscene.scene import Scene
from py3dscene.material import PBRMaterial
from py3dscene.material import AlphaMode

def import_material(gltf_material: tiny_gltf.Material,
                    scene: Scene,
                    material_index: int,
                    images_map: dict[int, str]) -> PBRMaterial:
    material_name = gltf_material.name
    if len(material_name) == 0:
        material_name = "Material_" + str(material_index)
    
    # ise material index as id
    material = scene.create_material(material_name, material_index)

    alpha_mode: str = gltf_material.alpha_mode
    if alpha_mode == "MASK":
        material.set_alpha_mode(AlphaMode.MASK)
    elif alpha_mode == "BLEND":
        material.set_alpha_mode(AlphaMode.BLEND)
    else:
        material.set_alpha_mode(AlphaMode.OPAQUE)
    
    material.set_alpha_cutoff(gltf_material.alpha_cutoff)
    material.set_double_sided(gltf_material.double_sided)
    material.set_metalness(gltf_material.pbr_metallic_roughness.metallic_factor)
    material.set_roughness(gltf_material.pbr_metallic_roughness.roughness_factor)

    albedo: list[float] = gltf_material.pbr_metallic_roughness.base_color_factor
    material.set_albedo(*albedo)

    emissive: list[float] = gltf_material.emissive_factor
    material.set_emissive(*emissive)

    albedo_texture_index = gltf_material.pbr_metallic_roughness.base_color_texture.index
    metallic_texture_index = gltf_material.pbr_metallic_roughness.metallic_roughness_texture.index
    emissive_texture_index = gltf_material.emissive_texture.index
    normal_texture_index = gltf_material.normal_texture.index
    occlusion_texture_index = gltf_material.occlusion_texture.index
    
    if albedo_texture_index in images_map:
        material.set_albedo_texture(images_map[albedo_texture_index], gltf_material.pbr_metallic_roughness.base_color_texture.tex_coord)
    
    if metallic_texture_index in images_map:
        material.set_metallic_roughness_texture(images_map[metallic_texture_index], gltf_material.pbr_metallic_roughness.metallic_roughness_texture.tex_coord)
    
    if emissive_texture_index in images_map:
        material.set_emissive_texture(images_map[emissive_texture_index], gltf_material.emissive_texture.tex_coord)
    
    if normal_texture_index in images_map:
        material.set_normal_texture(images_map[normal_texture_index], gltf_material.normal_texture.tex_coord, gltf_material.normal_texture.scale)
    
    if occlusion_texture_index in images_map:
        material.set_occlusion_texture(images_map[occlusion_texture_index], gltf_material.occlusion_texture.tex_coord, gltf_material.occlusion_texture.strength)
    
    return material

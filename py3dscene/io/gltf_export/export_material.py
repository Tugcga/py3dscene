import os
from typing import Optional
from py3dscene.bin import tiny_gltf
from py3dscene.material import PBRMaterial
from py3dscene.material import AlphaMode

def export_texture(gltf_model_textures: list[tiny_gltf.Texture],
                   gltf_model_images: list[tiny_gltf.Image],
                   texture_path: str,
                   output_folder: str) -> int:
    # extract texture name
    texture_path_norm = texture_path.replace("/", "\\")
    output_folder_norm = output_folder.replace("/", "\\")
    texture_name = ".".join(texture_path_norm.split("\\")[-1].split(".")[:-1])
    image_info: list[int] = tiny_gltf.get_image_info(texture_path)
    # image_info in format: width, height, channels, os_ok (1 or 0)
    if image_info[-1] == 1:
        width: int = image_info[0]
        height: int = image_info[1]
        channels: int = image_info[2]

        gltf_image = tiny_gltf.Image()
        gltf_image.name = texture_name
        gltf_image.width = width
        gltf_image.height = height
        gltf_image.component = channels
        gltf_image.bits = 8

        pixels = tiny_gltf.load_image(texture_path)
        gltf_image.image = pixels
        gltf_image.uri = os.path.relpath(texture_path_norm, output_folder_norm)
        gltf_image.pixel_type = tiny_gltf.TINYGLTF_COMPONENT_TYPE_UNSIGNED_BYTE

        image_index: int = len(gltf_model_images)
        gltf_model_images.append(gltf_image)

        gltf_texture = tiny_gltf.Texture()
        gltf_texture.name = texture_name
        gltf_texture.source = image_index
        gltf_model_textures.append(gltf_texture)
        return len(gltf_model_textures) - 1
    else:
        return -1

def assign_texture(texture_path: str,
                   textures_map: dict[str, int],
                   gltf_model_textures: list[tiny_gltf.Texture],
                   gltf_model_images: list[tiny_gltf.Image],
                   output_folder: str,
                   uv_index: Optional[int]) -> Optional[tiny_gltf.TextureInfo]:
    texture_index: int = -1
    if texture_path in textures_map:
        texture_index = textures_map[texture_path]
    else:
        texture_index = export_texture(gltf_model_textures,
                                       gltf_model_images,
                                       texture_path,
                                       output_folder)
        textures_map[texture_path] = texture_index

    if texture_index >= 0 and uv_index is not None:
        texture_info = tiny_gltf.TextureInfo()
        texture_info.index = texture_index
        texture_info.tex_coord = uv_index
        return texture_info
    return None
        

def export_materials(output_folder: str,
                     materials: list[PBRMaterial],
                     gltf_model_materials: list[tiny_gltf.Material],
                     gltf_model_textures: list[tiny_gltf.Texture],
                     gltf_model_images: list[tiny_gltf.Image],
                     materials_map: dict[int, int]):
    # some materials can use the same textures
    # export each used texture once and then use the link
    textures_map: dict[str, int] = {}  # key - path to the texture, value - index in glTF model
    for material in materials:
        material_id: int = material.get_id()
        gltf_material = tiny_gltf.Material()
        gltf_material.name = material.get_name()
        alpha_mode: AlphaMode = material.get_alpha_mode()
        if alpha_mode == AlphaMode.MASK:
            gltf_material.alpha_mode = "MASK"
        elif alpha_mode == AlphaMode.BLEND:
            gltf_material.alpha_mode = "BLEND"
        else:
            gltf_material.alpha_mode = "OPAQUE"
        
        gltf_material.alpha_cutoff = material.get_alpha_cutoff()
        gltf_material.double_sided = material.get_double_sided()
        gltf_material.emissive_factor = material.get_emissive()

        gltf_pbr = tiny_gltf.PbrMetallicRoughness()
        gltf_pbr.base_color_factor = material.get_albedo()
        gltf_pbr.metallic_factor = material.get_metalness()
        gltf_pbr.roughness_factor = material.get_roughness()
        albedo_path: Optional[str] = material.get_albedo_texture_path()
        texture_info: Optional[tiny_gltf.TextureInfo] = None
        if albedo_path:
            texture_info = assign_texture(albedo_path,
                                          textures_map,
                                          gltf_model_textures,
                                          gltf_model_images,
                                          output_folder,
                                          material.get_albedo_texture_uv())
            if texture_info:
                gltf_pbr.base_color_texture = texture_info
        
        metallic_path: Optional[str] = material.get_metallic_roughness_texture_path()
        if metallic_path:
            texture_info = assign_texture(metallic_path,
                                          textures_map,
                                          gltf_model_textures,
                                          gltf_model_images,
                                          output_folder,
                                          material.get_metallic_roughness_texture_uv())
            if texture_info:
                gltf_pbr.metallic_roughness_texture = texture_info
        gltf_material.pbr_metallic_roughness = gltf_pbr
        
        normal_path: Optional[str] = material.get_normal_texture_path()
        if normal_path:
            texture_info = assign_texture(normal_path,
                                          textures_map,
                                          gltf_model_textures,
                                          gltf_model_images,
                                          output_folder,
                                          material.get_normal_texture_uv())
            if texture_info:
                gltf_normal = tiny_gltf.NormalTextureInfo()
                gltf_normal.index = texture_info.index
                gltf_normal.tex_coord = texture_info.tex_coord
                gltf_normal.scale = material.get_normal_texture_strength()
                gltf_material.normal_texture = gltf_normal

        occlusion_path: Optional[str] = material.get_occlusion_texture_path()
        if occlusion_path:
            texture_info = assign_texture(occlusion_path,
                                          textures_map,
                                          gltf_model_textures,
                                          gltf_model_images,
                                          output_folder,
                                          material.get_occlusion_texture_uv())
            if texture_info:
                gltf_occlusion = tiny_gltf.OcclusionTextureInfo()
                gltf_occlusion.index = texture_info.index
                gltf_occlusion.tex_coord = texture_info.tex_coord
                gltf_occlusion.strength = material.get_occlusion_texture_strength()
                gltf_material.occlusion_texture = gltf_occlusion

        emission_path: Optional[str] = material.get_emissive_texture_path()
        if emission_path:
            texture_info = assign_texture(emission_path,
                                          textures_map,
                                          gltf_model_textures,
                                          gltf_model_images,
                                          output_folder,
                                          material.get_emissive_texture_uv())
            if texture_info:
                gltf_material.emissive_texture = texture_info

        materials_map[material_id] = len(gltf_model_materials)
        gltf_model_materials.append(gltf_material)

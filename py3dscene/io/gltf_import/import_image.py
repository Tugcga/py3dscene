import os
from py3dscene.bin import tiny_gltf

def import_images(gltf_model: tiny_gltf.Model,
                  file_path: str) -> dict[int, str]:
    file_path_norm: str = file_path.replace("/", "\\")
    images_map: dict[int, str] = {}
    images_count: int = len(gltf_model.images)
    for i in range(images_count):
        gltf_image: tiny_gltf.Image = gltf_model.images[i]
        image_uri: str = gltf_image.uri
        # calculate image path
        # if uri is empty, then image is embedded
        # in other case the path already exists
        image_path: str = ""
        last_slash: int = file_path_norm.rfind("\\")
        last_point: int = file_path_norm.rfind(".")
        if len(image_uri) == 0:
            # extract the image
            image_width: int = gltf_image.width
            image_height: int = gltf_image.height
            image_components: int = gltf_image.component
            image_pixel_type: int = gltf_image.pixel_type
            image_bits: int = gltf_image.bits

            gltf_image_name: str = gltf_image.name
            gltf_image_name = gltf_image_name.replace("/", "\\").replace(".", "_")
            # the name may contains the path to the file, so, get only the last part of the path
            image_name: str = gltf_image_name.split("\\")[-1]
            if len(image_name) == 0:
                image_name = "texture_" + str(i)
            image_folder: str = file_path_norm[:last_slash] + "\\" + file_path_norm[last_slash + 1: last_point] + "_textures\\"
            # create directory if it does not exists
            os.makedirs(image_folder, exist_ok=True)
            image_path = image_folder + image_name + ".png"
            # skip if the file already exists
            if not os.path.isfile(image_path):
                is_write: bool = tiny_gltf.write_png(image_path, image_width, image_height, image_components, gltf_image.image)
                if not is_write:
                    # fail to write the texture
                    image_path = ""
        else:
            # we assume that the path is relative to the input file
            # form new relative path
            image_path = file_path_norm[:last_slash] + "\\" + image_uri

        if len(image_path) > 0:
            images_map[i] = image_path
    return images_map

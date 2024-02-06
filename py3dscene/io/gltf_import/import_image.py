import os
from py3dscene.bin.tiny_gltf import Scene as GLTFScene  # type: ignore
from py3dscene.bin.tiny_gltf import Model as GLTFModel  # type: ignore
from py3dscene.bin.tiny_gltf import Image as GLTFImage  # type: ignore
from py3dscene.bin.tiny_gltf import write_png  # type: ignore

def import_images(gltf_model: GLTFModel,
                  gltf_scene: GLTFScene,
                  file_path: str) -> dict[int, str]:
    images_map: dict[int, str] = {}
    images_count: int = len(gltf_model.images)
    for i in range(images_count):
        gltf_image = gltf_model.images[i]
        image_uri = gltf_image.uri
        # calculate image path
        # if uri is empty, then image is embedded
        # in other case the path already exists
        image_path = ""
        last_slash = file_path.rfind("/")
        last_point = file_path.rfind(".")
        if len(image_uri) == 0:
            # extract the image
            image_width: int = gltf_image.width
            image_height: int = gltf_image.height
            image_components: int = gltf_image.component
            image_pixel_type: int = gltf_image.pixel_type
            image_bits: int = gltf_image.bits

            image_name: str = gltf_image.name
            if len(image_name) == 0:
                image_name = "texture_" + str(i)
            image_folder = file_path[:last_slash] + "/" + file_path[last_slash + 1: last_point] + "_textures/"
            # create directory if it does not exists
            os.makedirs(image_folder, exist_ok=True)
            image_path = image_folder + image_name + ".png"
            # skip if the file already exists
            if not os.path.isfile(image_path):
                is_write = write_png(image_path, image_width, image_height, image_components, gltf_image.image)
                if not is_write:
                    # fail to write the texture
                    image_path = ""
        else:
            # we assume that the path is relative to the input file
            # form new relative path
            image_path = file_path[:last_slash] + "//" + image_uri

        if len(image_path) > 0:
            images_map[i] = image_path
    return images_map

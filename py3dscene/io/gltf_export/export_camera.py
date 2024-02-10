from typing import Optional
from py3dscene.bin.tiny_gltf import Node as GLTFNode  # type: ignore
from py3dscene.bin.tiny_gltf import Camera as GLTFCamera  # type: ignore
from py3dscene.camera import CameraComponent
from py3dscene.camera import CameraType

def export_camera(camera: CameraComponent,
                  gltf_model_cameras: list[GLTFCamera]) -> Optional[GLTFNode]:

    return None
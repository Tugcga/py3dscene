from typing import Optional
from py3dscene.bin.tiny_gltf import Node as GLTFNode  # type: ignore
from py3dscene.bin.tiny_gltf import Light as GLTFLight  # type: ignore
from py3dscene.light import LightComponent
from py3dscene.light import LightType

def export_light(light: LightComponent,
                  gltf_model_lights: list[GLTFLight]) -> Optional[GLTFNode]:

    return None
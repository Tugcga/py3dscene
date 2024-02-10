from py3dscene.bin.tiny_gltf import Model as GLTFModel  # type: ignore
from py3dscene.bin.tiny_gltf import Light as GLTFLight  # type: ignore
from py3dscene.object import Object
from py3dscene.light import LightComponent
from py3dscene.light import LightType

def import_object_light(gltf_light: GLTFLight,
                        object: Object):
    gltf_type = gltf_light.type
    light: LightComponent = LightComponent()
    gltf_name = gltf_light.name
    if len(gltf_name ) > 0:
        light.set_name(gltf_name)

    gltf_color = gltf_light.color
    if len(gltf_color) >= 3:
        light.set_color(gltf_color[0], gltf_color[1], gltf_color[2])

    light.set_strength(gltf_light.intensity)
    light.set_range(gltf_light.range)

    if gltf_type == "point":
        light.set_type(LightType.POINT)
    elif gltf_type == "directional":
        light.set_type(LightType.DIRECTIONAL)
    elif gltf_type == "spot":
        light.set_type(LightType.SPOT)
        light.set_spot_angles(gltf_light.spot.inner_cone_angle, gltf_light.spot.outer_cone_angle)
    object.set_light_component(light)

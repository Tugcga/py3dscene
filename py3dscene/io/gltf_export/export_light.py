from typing import Optional
from py3dscene.bin import tiny_gltf
from py3dscene.io.gltf_export.export_transform import export_transform
from py3dscene.object import Object
from py3dscene.light import LightComponent
from py3dscene.light import LightType

def export_light(light: LightComponent,
                 object: Object,
                 gltf_model_lights: list[tiny_gltf.Light]) -> Optional[tiny_gltf.Node]:
    new_node = tiny_gltf.Node()
    new_node.name = object.get_name()

    export_transform(new_node,
                     object.get_transform(),
                     object.get_translation(),
                     object.get_rotation(),
                     object.get_scale())

    gltf_light = tiny_gltf.Light()
    
    type: LightType = light.get_type()
    if type in [LightType.POINT, LightType.DIRECTIONAL, LightType.SPOT]:
        gltf_light.color = list(light.get_color())
        gltf_light.intensity = light.get_strength()
        gltf_light.range = light.get_range()

    if type == LightType.POINT:
        gltf_light.name = "point light"
        gltf_light.type = "point"
    elif type == LightType.DIRECTIONAL:
        gltf_light.name = "directional light"
        gltf_light.type = "directional"
    elif type == LightType.SPOT:
        gltf_light.name = "spot light"
        gltf_light.type = "spot"

        gltf_spot = tiny_gltf.SpotLight()
        gltf_spot.inner_cone_angle = light.get_spot_inner_cone()
        gltf_spot.outer_cone_angle = light.get_spot_outer_cone()

        gltf_light.spot = gltf_spot
    else:
        return None
    
    new_node.light = len(gltf_model_lights)
    gltf_model_lights.append(gltf_light)
    return new_node

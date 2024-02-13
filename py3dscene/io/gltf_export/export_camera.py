from typing import Optional
from py3dscene.bin import tiny_gltf
from py3dscene.io.gltf_export.export_transform import export_transform
from py3dscene.object import Object
from py3dscene.camera import CameraComponent
from py3dscene.camera import CameraType

def export_camera(camera: CameraComponent,
                  object: Object,
                  gltf_model_cameras: list[tiny_gltf.Camera]) -> Optional[tiny_gltf.Node]:
    new_node = tiny_gltf.Node()

    new_node.name = object.get_name()
    export_transform(new_node,
                        object.get_transform(),
                        object.get_translation(),
                        object.get_rotation(),
                        object.get_scale())
    gltf_camera = tiny_gltf.Camera()

    type: CameraType = camera.get_type()
    if type == CameraType.PERSPECTIVE:
        gltf_camera.type = "perspective"
        gltf_camera.name = "perspective camera"
        persp_camera = tiny_gltf.PerspectiveCamera()
        persp_camera.yfov = camera.get_perspective_fov()
        
        persp_camera.aspect_ratio = camera.get_perspective_aspect()

        persp_camera.znear = camera.get_clipping_near()
        persp_camera.zfar = camera.get_clipping_far()

        gltf_camera.perspective = persp_camera
    elif type == CameraType.ORTHOGRAPHIC:
        gltf_camera.type = "orthographic"
        gltf_camera.name = "orthographic camera"
        ortho_camera = tiny_gltf.OrthographicCamera()
        ortho_camera.ymag = camera.get_orthographic_height()
        ortho_camera.xmag = camera.get_orthographic_width()

        ortho_camera.znear = camera.get_clipping_near()
        ortho_camera.zfar = camera.get_clipping_far()

        gltf_camera.orthographic = ortho_camera
    else:
        return None

    new_node.camera = len(gltf_model_cameras)
    gltf_model_cameras.append(gltf_camera)
    return new_node
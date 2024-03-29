from py3dscene.bin import tiny_gltf
from py3dscene.object import Object
from py3dscene.camera import CameraComponent
from py3dscene.camera import CameraType

def import_object_camera(gltf_camera: tiny_gltf.Camera,
                         object: Object) -> None:
    gltf_type = gltf_camera.type
    camera: CameraComponent = CameraComponent()
    if gltf_type == "perspective":
        camera.set_type(CameraType.PERSPECTIVE)
        camera.set_perspective_fov(gltf_camera.perspective.yfov)
        camera.set_perspective_aspect(gltf_camera.perspective.aspect_ratio)
        camera.set_clipping_planes(gltf_camera.perspective.znear, gltf_camera.perspective.zfar)
    elif gltf_type == "orthographic":
        camera.set_type(CameraType.ORTHOGRAPHIC)
        camera.set_orthographic_size(gltf_camera.orthographic.xmag, gltf_camera.orthographic.ymag)
        camera.set_clipping_planes(gltf_camera.orthographic.znear, gltf_camera.orthographic.zfar)
    object.set_camera_component(camera)

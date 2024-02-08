from py3dscene.bin.tiny_gltf import Model as GLTFModel  # type: ignore
from py3dscene.bin.tiny_gltf import Camera as GLTFCamera  # type: ignore
from py3dscene.object import Object
from py3dscene.camera import CameraComponent
from py3dscene.camera import CameraType

def import_object_camera(gltf_camera: GLTFCamera,
                         object: Object):
    gltf_type = gltf_camera.type
    camera: CameraComponent = CameraComponent()
    if gltf_type == "perspective":
        camera.set_type(CameraType.PERSPECTIVE)
        camera.set_perspective_fov(gltf_camera.perspective.yfov)
        camera.set_perspective_aspect(gltf_camera.perspective.aspect_ratio)
        camera.set_clipping_planes(gltf_camera.perspective.znear, gltf_camera.perspective.zfar)
        object.set_camera_component(camera)
    elif gltf_type == "orthographic":
        camera.set_type(CameraType.ORTHOGRAPHIC)
        camera.set_orthographic_size(gltf_camera.orthographic.xmag, gltf_camera.orthographic.ymag)
        camera.set_clipping_planes(gltf_camera.perspective.znear, gltf_camera.perspective.zfar)
        object.set_camera_component(camera)

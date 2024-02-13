from typing import Optional
import sys
import struct
from py3dscene.bin.tiny_gltf import AnimationSampler as GLTFAnimationSampler  # type: ignore
from py3dscene.bin.tiny_gltf import AnimationChannel as GLTFAnimationChannel  # type: ignore
from py3dscene.bin.tiny_gltf import Animation as GLTFAnimation  # type: ignore
from py3dscene.bin.tiny_gltf import BufferView as GLTFBufferView  # type: ignore
from py3dscene.bin.tiny_gltf import Accessor as GLTFAccessor  # type: ignore
from py3dscene.bin.tiny_gltf import TINYGLTF_COMPONENT_TYPE_FLOAT
from py3dscene.bin.tiny_gltf import TINYGLTF_TYPE_SCALAR
from py3dscene.bin.tiny_gltf import TINYGLTF_TYPE_VEC3
from py3dscene.bin.tiny_gltf import TINYGLTF_TYPE_VEC4
from py3dscene.io.gltf_export.export_buffer import add_data_to_buffer
from py3dscene.scene import Scene
from py3dscene.object import Object
from py3dscene.animation import Animation
from py3dscene.animation import AnimationCurveType
from py3dscene.animation import ValuesVariants

def write_animation_clip(gltf_model_buffers_data: list[int],
                         gltf_model_buffer_views: list[GLTFBufferView],
                         gltf_model_accessors: list[GLTFAccessor],
                         gltf_animation_samplers: list[GLTFAnimationSampler],
                         gltf_animation_channels: list[GLTFAnimationChannel],
                         animation: Animation,
                         target_str: str,
                         node_index: int,
                         fps: float):
    # for the animation we should transform key frames into plane array of seconds
    # values into plane array of floats
    # and then write it to the buffer
    frames = animation.get_frames()
    curve_type: AnimationCurveType = animation.get_type()
    value_components: int = animation.get_value_components()

    times_array: list[float] = []
    values_array: list[float] = []
    for frame in frames:
        value: Optional[ValuesVariants] = animation.get_value_at_frame(frame)
        if value:
            frame_time = frame / fps
            times_array.append(frame_time)

            if curve_type == AnimationCurveType.CUBICSPLINE:
                # in this case value is a tuple of tuples
                for v in value:
                    values_array.extend(v)  # type: ignore
            else:
                # in this case value is simple tuple
                values_array.extend(value)  # type: ignore
    # calculate minimum and maximum values for coordinates
    min_values: list[float] = [sys.float_info.max] * value_components
    max_values: list[float] = [-sys.float_info.max] * value_components
    time_bytes: list[int] = []
    values_bytes: list[int] = []
    times_count = len(times_array)
    for i in range(times_count):
        time_bytes.extend(struct.pack("f", times_array[i]))
    steps: int = len(values_array) // value_components
    for i in range(steps):
        for c in range(value_components):
            v = values_array[i * value_components + c]
            values_bytes.extend(struct.pack("f", v))
            if v < min_values[c]:
                min_values[c] = v
            if v > max_values[c]:
                max_values[c] = v
    # write arrays to the buffer
    time_index: int = add_data_to_buffer(gltf_model_buffers_data,
                                         gltf_model_buffer_views,
                                         gltf_model_accessors,
                                         time_bytes,
                                         times_count,
                                         False,
                                         True,
                                         TINYGLTF_COMPONENT_TYPE_FLOAT,
                                         TINYGLTF_TYPE_SCALAR,
                                         [times_array[0]],
                                         [times_array[-1]])
    values_index: int = add_data_to_buffer(gltf_model_buffers_data,
                                           gltf_model_buffer_views,
                                           gltf_model_accessors,
                                           values_bytes,
                                           times_count * 3 if curve_type == AnimationCurveType.CUBICSPLINE else times_count,
                                           False,
                                           True,
                                           TINYGLTF_COMPONENT_TYPE_FLOAT,
                                           TINYGLTF_TYPE_VEC3 if value_components == 3 else TINYGLTF_TYPE_VEC4,
                                           min_values,
                                           max_values)
    
    # next write accessor indices to animation objects
    gltf_sampler: GLTFAnimationSampler = GLTFAnimationSampler()
    gltf_sampler.interpolation = "CUBICSPLINE" if curve_type == AnimationCurveType.CUBICSPLINE else ("STEP" if curve_type == AnimationCurveType.STEP else "LINEAR")
    gltf_sampler.input = time_index
    gltf_sampler.output = values_index

    sampler_index: int = len(gltf_animation_samplers)
    gltf_animation_samplers.append(gltf_sampler)
    channel: GLTFAnimationChannel = GLTFAnimationChannel()
    channel.sampler = sampler_index
    channel.target_node = node_index
    channel.target_path = target_str
    gltf_animation_channels.append(channel)

def export_object_animation(gltf_model_buffers_data: list[int],
                            gltf_model_buffer_views: list[GLTFBufferView],
                            gltf_model_accessors: list[GLTFAccessor],
                            gltf_model_animations: list[GLTFAnimation],
                            object_to_node: dict[int, int],
                            object: Object,
                            fps: float):
    gltf_animation_samplers: list[GLTFAnimationSampler] = []
    gltf_animation_channels: list[GLTFAnimationChannel] = []

    translation_anim: Optional[Animation] = object.get_translation_animation()
    rotation_anim: Optional[Animation] = object.get_rotation_animation()
    scale_anim: Optional[Animation] = object.get_scale_animation()

    object_id: int = object.get_id()
    if object_id not in object_to_node:
        return None
    
    node_index: int = object_to_node[object_id]

    if translation_anim:
        write_animation_clip(gltf_model_buffers_data,
                             gltf_model_buffer_views,
                             gltf_model_accessors,
                             gltf_animation_samplers,
                             gltf_animation_channels,
                             translation_anim,
                             "translation",
                             node_index,
                             fps)
    if rotation_anim:
        write_animation_clip(gltf_model_buffers_data,
                             gltf_model_buffer_views,
                             gltf_model_accessors,
                             gltf_animation_samplers,
                             gltf_animation_channels,
                             rotation_anim,
                             "rotation",
                             node_index,
                             fps)
    if scale_anim:
         write_animation_clip(gltf_model_buffers_data,
                             gltf_model_buffer_views,
                             gltf_model_accessors,
                             gltf_animation_samplers,
                             gltf_animation_channels,
                             scale_anim,
                             "scale",
                             node_index,
                             fps)

    if len(gltf_animation_samplers) > 0 and len(gltf_animation_channels) > 0:
        gltf_animation: GLTFAnimation = GLTFAnimation()
        gltf_animation.samplers = gltf_animation_samplers
        gltf_animation.channels = gltf_animation_channels
        gltf_animation.name = object.get_name()
        gltf_model_animations.append(gltf_animation)

    for obj in object.get_children():
        export_object_animation(gltf_model_buffers_data,
                                gltf_model_buffer_views,
                                gltf_model_accessors,
                                gltf_model_animations,
                                object_to_node,
                                obj,
                                fps)

def export_animation(gltf_model_buffers_data: list[int],
                     gltf_model_buffer_views: list[GLTFBufferView],
                     gltf_model_accessors: list[GLTFAccessor],
                     scene: Scene,
                     fps: float,
                     object_to_node: dict[int, int]) -> list[GLTFAnimation]:
    gltf_model_animations: list[GLTFAnimation] = []
    for obj in scene.get_root_objects():
        export_object_animation(gltf_model_buffers_data,
                                gltf_model_buffer_views,
                                gltf_model_accessors,
                                gltf_model_animations,
                                object_to_node,
                                obj,
                                fps)
    
    return gltf_model_animations

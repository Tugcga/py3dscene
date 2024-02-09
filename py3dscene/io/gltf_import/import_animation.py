from py3dscene.bin.tiny_gltf import Model as GLTFModel  # type: ignore
from py3dscene.bin.tiny_gltf import Accessor as GLTFAccessor  # type: ignore
from py3dscene.bin.tiny_gltf import Animation as GLTFAnimation  # type: ignore
from py3dscene.bin.tiny_gltf import AnimationChannel as GLTFAnimationChannel  # type: ignore
from py3dscene.bin.tiny_gltf import AnimationSampler as GLTFAnimationSampler  # type: ignore
from py3dscene.io.gltf_import.import_buffer import get_float_buffer
from py3dscene.object import Object
from py3dscene.animation import Animation
from py3dscene.animation import AnimationCurveType

def import_animations(gltf_model: GLTFModel,
                      nodes_map: dict[int, Object],
                      fps: float):
    for anim_index in range(len(gltf_model.animations)):
        animation: GLTFAnimation = gltf_model.animations[anim_index]
        for channel_index in range(len(animation.channels)):
            channel: GLTFAnimationChannel = animation.channels[channel_index]
            sampler: GLTFAnimationSampler = animation.samplers[channel.sampler]
            node_index: int = channel.target_node
            if node_index in nodes_map:
                object = nodes_map[node_index]
                target_path: str = channel.target_path
                time_accessor: GLTFAccessor = gltf_model.accessors[sampler.input]
                values_accessor: GLTFAccessor = gltf_model.accessors[sampler.output]
                curve_type: AnimationCurveType = AnimationCurveType.CUBICSPLINE if sampler.interpolation == "CUBICSPLINE" else (AnimationCurveType.STEP if sampler.interpolation == "STEP" else AnimationCurveType.LINEAR)
                times: list[float] = get_float_buffer(gltf_model, time_accessor)
                values: list[float] = get_float_buffer(gltf_model, values_accessor, True)
                if len(times) > 0 and len(values) > 0:
                    # for cubic curve each key defined by 3 values
                    # for linear and step only by 1 value
                    # for example, for translation cubic curve the number of values is x9 to the number of times
                    anim: Animation = Animation(curve_type)
                    for step, time in enumerate(times):
                        if curve_type == AnimationCurveType.CUBICSPLINE:
                            if target_path == "rotation":
                                anim.add_keyframe(time * fps, ((values[4 * step], values[4 * step + 1], values[4 * step + 2], values[4 * step + 3]),
                                                               (values[4 * step + 4], values[4 * step + 5], values[4 * step + 6], values[4 * step + 7]),
                                                               (values[4 * step + 8], values[4 * step + 9], values[4 * step + 10], values[4 * step + 11])))
                            else:
                                anim.add_keyframe(time * fps, ((values[9 * step], values[9 * step + 1], values[9 * step + 2]),
                                                               (values[9 * step + 4], values[9 * step + 5], values[9 * step + 6]),
                                                               (values[9 * step + 7], values[9 * step + 8], values[9 * step + 9])))
                        else:
                            if target_path == "rotation":
                                anim.add_keyframe(time * fps, (values[4 * step], values[4 * step + 1], values[4 * step + 2], values[4 * step + 3]))
                            else:
                                anim.add_keyframe(time * fps, (values[3 * step], values[3 * step + 1], values[3 * step + 2]))
                    if target_path == "translation":
                        object.set_translation_animation(anim)
                    elif target_path == "rotation":
                        object.set_rotation_animation(anim)
                    elif target_path == "scale":
                        object.set_scale_animation(anim)

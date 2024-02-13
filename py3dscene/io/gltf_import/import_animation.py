from py3dscene.bin import tiny_gltf
from py3dscene.io.gltf_import.import_buffer import get_float_buffer
from py3dscene.object import Object
from py3dscene.animation import Animation
from py3dscene.animation import AnimationCurveType

def import_animations(gltf_model: tiny_gltf.Model,
                      model_buffers_data: list[list[int]],
                      nodes_map: dict[int, Object],
                      fps: float) -> None:
    for anim_index in range(len(gltf_model.animations)):
        animation: tiny_gltf.Animation = gltf_model.animations[anim_index]
        for channel_index in range(len(animation.channels)):
            channel: tiny_gltf.AnimationChannel = animation.channels[channel_index]
            sampler: tiny_gltf.AnimationSampler = animation.samplers[channel.sampler]
            node_index: int = channel.target_node
            if node_index in nodes_map:
                object = nodes_map[node_index]
                target_path: str = channel.target_path
                time_accessor: tiny_gltf.Accessor = gltf_model.accessors[sampler.input]
                values_accessor: tiny_gltf.Accessor = gltf_model.accessors[sampler.output]
                curve_type: AnimationCurveType = AnimationCurveType.CUBICSPLINE if sampler.interpolation == "CUBICSPLINE" else (AnimationCurveType.STEP if sampler.interpolation == "STEP" else AnimationCurveType.LINEAR)
                times: list[float] = get_float_buffer(gltf_model, time_accessor, model_buffers_data)
                values: list[float] = get_float_buffer(gltf_model, values_accessor, model_buffers_data, True)

                if len(times) > 0 and len(values) > 0:
                    # for cubic curve each key defined by 3 values
                    # for linear and step only by 1 value
                    # for example, for translation cubic curve the number of values is x9 to the number of times
                    anim: Animation = Animation(curve_type, 4 if target_path == "rotation" else 3)
                    for step, time in enumerate(times):
                        if curve_type == AnimationCurveType.CUBICSPLINE:
                            if target_path == "rotation":
                                anim.add_keyframe(time * fps, ((values[4 * step], values[12 * step + 1], values[12 * step + 2], values[12 * step + 3]),
                                                               (values[12 * step + 4], values[12 * step + 5], values[12 * step + 6], values[12 * step + 7]),
                                                               (values[12 * step + 8], values[12 * step + 9], values[12 * step + 10], values[12 * step + 11])))
                            else:
                                anim.add_keyframe(time * fps, ((values[9 * step], values[9 * step + 1], values[9 * step + 2]),
                                                               (values[9 * step + 3], values[9 * step + 4], values[9 * step + 5]),
                                                               (values[9 * step + 6], values[9 * step + 7], values[9 * step + 8])))
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

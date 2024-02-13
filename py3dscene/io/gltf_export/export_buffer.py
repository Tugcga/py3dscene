import struct
from py3dscene.bin import tiny_gltf

def add_data_to_buffer(gltf_model_buffers_data: list[int],
                       gltf_model_buffer_views: list[tiny_gltf.BufferView],
                       gltf_model_accessors: list[tiny_gltf.Accessor],
                       byte_vector: list[int],
                       data_count: int,
                       is_indices: bool,
                       ignore_target: bool,
                       component_type: int,
                       data_type: int,
                       min_value: list[float],
                       max_value: list[float]) -> int:
    view = tiny_gltf.BufferView()
    view.buffer = 0
    view.byte_offset = len(gltf_model_buffers_data)
    view.byte_length = len(byte_vector)
    if not ignore_target:
        view.target = tiny_gltf.TINYGLTF_TARGET_ELEMENT_ARRAY_BUFFER if is_indices else tiny_gltf.TINYGLTF_TARGET_ARRAY_BUFFER

    rem: int = len(byte_vector) % 4
    byte_vector.extend([0] * rem)

    gltf_model_buffers_data.extend(byte_vector)

    accessor = tiny_gltf.Accessor()
    accessor.buffer_view = len(gltf_model_buffer_views)
    accessor.byte_offset = 0
    accessor.component_type = component_type
    accessor.count = data_count
    accessor.type = data_type
    accessor.min_values = min_value
    accessor.max_values = max_value

    gltf_model_buffer_views.append(view)
    gltf_model_accessors.append(accessor)

    return len(gltf_model_accessors) - 1

def add_triangle_indices_to_buffer(gltf_model_buffers_data: list[int],
                                   gltf_model_buffer_views: list[tiny_gltf.BufferView],
                                   gltf_model_accessors: list[tiny_gltf.Accessor],
                                   data: list[tuple[int, int, int]],
                                   component_type: int,
                                   data_type: int) -> int:
    byte_vector: list[int] = []
    for triangle in data:
        for c in triangle:
            byte_vector.extend(list(struct.pack("I", c)))
    min: int = 2147483647
    max: int = 0
    for i in range(len(data)):
        for j in range(3):
            v = data[i][j]
            if v < min:
                min = v
            if v > max:
                max = v
    min_value: list[float] = [float(min)]
    max_value: list[float] = [float(max)]

    return add_data_to_buffer(gltf_model_buffers_data,
                              gltf_model_buffer_views,
                              gltf_model_accessors,
                              byte_vector,
                              len(data) * 3,
                              True,
                              False,
                              component_type,
                              data_type,
                              min_value,
                              max_value)

def add_float_to_buffer(gltf_model_buffers_data: list[int],
                        gltf_model_buffer_views: list[tiny_gltf.BufferView],
                        gltf_model_accessors: list[tiny_gltf.Accessor],
                        data: list[float],
                        ignore_target: bool,
                        component_type: int,
                        data_type: int) -> int:
    items_count: int = len(data) // tiny_gltf.get_num_components_in_type(data_type)
    byte_vector: list[int] = []
    for v in data:
        byte_vector.extend(struct.pack("f", v))

    min_value: list[float] = []
    max_value: list[float] = []

    return add_data_to_buffer(gltf_model_buffers_data,
                              gltf_model_buffer_views,
                              gltf_model_accessors,
                              byte_vector,
                              items_count,
                              False,
                              ignore_target,
                              component_type,
                              data_type,
                              min_value,
                              max_value)

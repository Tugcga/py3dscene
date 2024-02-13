import struct
from py3dscene.bin import tiny_gltf

def component_type_to_format(type: int) -> str:
    if type == tiny_gltf.TINYGLTF_COMPONENT_TYPE_BYTE:
        return "c"
    elif type == tiny_gltf.TINYGLTF_COMPONENT_TYPE_UNSIGNED_BYTE:
        return "B"
    elif type == tiny_gltf.TINYGLTF_COMPONENT_TYPE_SHORT:
        return "h"
    elif type == tiny_gltf.TINYGLTF_COMPONENT_TYPE_UNSIGNED_SHORT:
        return "H"
    elif type == tiny_gltf.TINYGLTF_COMPONENT_TYPE_INT:
        return "i"
    elif type == tiny_gltf.TINYGLTF_COMPONENT_TYPE_UNSIGNED_INT:
        return "I"
    elif type == tiny_gltf.TINYGLTF_COMPONENT_TYPE_FLOAT:
        return "f"
    elif type == tiny_gltf.TINYGLTF_COMPONENT_TYPE_DOUBLE:
        return "d"
    return "i"

def read_float_buffer_view(buffer_view: tiny_gltf.BufferView, 
                           model_buffers_data: list[list[int]],
                           component_type: int,
                           byte_offset: int,
                           components: int,
                           count: int,
                           decode_normalized: bool) -> list[float]:
    buffer_data: list[int] = model_buffers_data[buffer_view.buffer]
    component_size: int = tiny_gltf.get_component_size_in_bytes(component_type)
    byte_stride: int = components * component_size if buffer_view.byte_stride == 0 else buffer_view.byte_stride
    index_stride: int = byte_stride // component_size

    to_return: list[float] = [0.0] * (components * count)
    for i in range(count):
        for c in range(components):
            buffer_start = buffer_view.byte_offset + byte_offset + (i * index_stride + c) * component_size
            buffer_part = buffer_data[buffer_start:buffer_start + component_size]
            value: float = float(struct.unpack(component_type_to_format(component_type), bytearray(buffer_part))[0])

            if component_type == tiny_gltf.TINYGLTF_COMPONENT_TYPE_FLOAT:
                to_return[components * i + c] = value
            elif component_type == tiny_gltf.TINYGLTF_COMPONENT_TYPE_UNSIGNED_BYTE:
                to_return[components * i + c] = value / 255.0 if decode_normalized else value
            elif component_type == tiny_gltf.TINYGLTF_COMPONENT_TYPE_UNSIGNED_SHORT:
                to_return[components * i + c] = value / 65535.0 if decode_normalized else value
            elif component_type == tiny_gltf.TINYGLTF_COMPONENT_TYPE_UNSIGNED_INT:
                to_return[components * i + c] = value
            elif component_type == tiny_gltf.TINYGLTF_COMPONENT_TYPE_BYTE:
                to_return[components * i + c] = value / 127.0 if decode_normalized else value
            elif component_type == tiny_gltf.TINYGLTF_COMPONENT_TYPE_SHORT:
                to_return[components * i + c] = value / 32767.0 if decode_normalized else value
            elif component_type == tiny_gltf.TINYGLTF_COMPONENT_TYPE_INT:
                to_return[components * i + c] = value
            elif component_type == tiny_gltf.TINYGLTF_COMPONENT_TYPE_DOUBLE:
                to_return[components * i + c] = value

    return to_return

def get_float_buffer(model: tiny_gltf.Model,
                     accessor: tiny_gltf.Accessor,
                     model_buffers_data: list[list[int]],
                     decode_normalized: bool=False) -> list[float]:
    components: int = tiny_gltf.get_num_components_in_type(accessor.type)
    component_type: int = accessor.component_type
    buffer_view: tiny_gltf.BufferView = model.buffer_views[accessor.buffer_view]

    return read_float_buffer_view(buffer_view, model_buffers_data, component_type, accessor.byte_offset, components, accessor.count, decode_normalized)

def read_integer_buffer_view(buffer_view: tiny_gltf.BufferView,
                             model_buffers_data: list[list[int]],
                             component_type: int,
                             byte_offset: int,
                             components: int,
                             count: int) -> list[int]:
    buffer_data: list[int] = model_buffers_data[buffer_view.buffer]
    component_size: int = tiny_gltf.get_component_size_in_bytes(component_type)
    byte_stride: int = components * component_size if buffer_view.byte_stride == 0 else buffer_view.byte_stride
    index_stride: int = byte_stride // component_size
    to_return: list[int] = [0] * (components * count)

    for i in range(count):
        for c in range(components):
            buffer_start: int = buffer_view.byte_offset + byte_offset + (i * index_stride + c) * component_size
            buffer_part = buffer_data[buffer_start:buffer_start + component_size]
            value: int = struct.unpack(component_type_to_format(component_type), bytearray(buffer_part))[0]
            to_return[components * i + c] = value

    return to_return

def get_integer_buffer(model: tiny_gltf.Model,
                       accessor: tiny_gltf.Accessor,
                       model_buffers_data: list[list[int]]) -> list[int]:
    components: int = tiny_gltf.get_num_components_in_type(accessor.type)
    component_type: int = accessor.component_type
    
    buffer_view: tiny_gltf.BufferView = model.buffer_views[accessor.buffer_view]
    return read_integer_buffer_view(buffer_view, model_buffers_data, component_type, accessor.byte_offset, components, accessor.count)

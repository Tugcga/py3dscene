import struct
from py3dscene.bin.tiny_gltf import Model as GLTFModel  # type: ignore
from py3dscene.bin.tiny_gltf import BufferView as GLTFBufferView  # type: ignore
from py3dscene.bin.tiny_gltf import Buffer as GLTFBuffer  # type: ignore
from py3dscene.bin.tiny_gltf import Accessor as GLTFAccessor  # type: ignore
from py3dscene.bin.tiny_gltf import get_component_size_in_bytes
from py3dscene.bin.tiny_gltf import get_num_components_in_type
from py3dscene.bin.tiny_gltf import TINYGLTF_COMPONENT_TYPE_BYTE
from py3dscene.bin.tiny_gltf import TINYGLTF_COMPONENT_TYPE_UNSIGNED_BYTE
from py3dscene.bin.tiny_gltf import TINYGLTF_COMPONENT_TYPE_SHORT
from py3dscene.bin.tiny_gltf import TINYGLTF_COMPONENT_TYPE_UNSIGNED_SHORT
from py3dscene.bin.tiny_gltf import TINYGLTF_COMPONENT_TYPE_INT
from py3dscene.bin.tiny_gltf import TINYGLTF_COMPONENT_TYPE_UNSIGNED_INT
from py3dscene.bin.tiny_gltf import TINYGLTF_COMPONENT_TYPE_FLOAT
from py3dscene.bin.tiny_gltf import TINYGLTF_COMPONENT_TYPE_DOUBLE

def component_type_to_format(type: int) -> str:
    if type == TINYGLTF_COMPONENT_TYPE_BYTE:
        return "c"
    elif type == TINYGLTF_COMPONENT_TYPE_UNSIGNED_BYTE:
        return "B"
    elif type == TINYGLTF_COMPONENT_TYPE_SHORT:
        return "h"
    elif type == TINYGLTF_COMPONENT_TYPE_UNSIGNED_SHORT:
        return "H"
    elif type == TINYGLTF_COMPONENT_TYPE_INT:
        return "i"
    elif type == TINYGLTF_COMPONENT_TYPE_UNSIGNED_INT:
        return "I"
    elif type == TINYGLTF_COMPONENT_TYPE_FLOAT:
        return "f"
    elif type == TINYGLTF_COMPONENT_TYPE_DOUBLE:
        return "d"
    return "i"

def read_float_buffer_view(model: GLTFModel,
                           buffer_view: GLTFBufferView, 
                           component_type: int,
                           byte_offset: int,
                           components: int,
                           count: int,
                           decode_normalized: bool) -> list[float]:
    buffer: GLTFBuffer = model.buffers[buffer_view.buffer]
    component_size: int = get_component_size_in_bytes(component_type)
    byte_stride: int = components * component_size if buffer_view.byte_stride == 0 else buffer_view.byte_stride
    index_stride: int = byte_stride // component_size

    to_return: list[float] = [0.0] * (components * count)
    for i in range(count):
        for c in range(components):
            buffer_start = buffer_view.byte_offset + byte_offset + (i * index_stride + c) * component_size
            buffer_part = buffer.data[buffer_start:buffer_start + component_size]
            value: float = float(struct.unpack(component_type_to_format(component_type), bytearray(buffer_part))[0])

            if component_type == TINYGLTF_COMPONENT_TYPE_FLOAT:
                to_return[components * i + c] = value
            elif component_type == TINYGLTF_COMPONENT_TYPE_UNSIGNED_BYTE:
                to_return[components * i + c] = value / 255.0 if decode_normalized else value
            elif component_type == TINYGLTF_COMPONENT_TYPE_UNSIGNED_SHORT:
                to_return[components * i + c] = value / 65535.0 if decode_normalized else value
            elif component_type == TINYGLTF_COMPONENT_TYPE_UNSIGNED_INT:
                to_return[components * i + c] = value
            elif component_type == TINYGLTF_COMPONENT_TYPE_BYTE:
                to_return[components * i + c] = value / 127.0 if decode_normalized else value
            elif component_type == TINYGLTF_COMPONENT_TYPE_SHORT:
                to_return[components * i + c] = value / 32767.0 if decode_normalized else value
            elif component_type == TINYGLTF_COMPONENT_TYPE_INT:
                to_return[components * i + c] = value
            elif component_type == TINYGLTF_COMPONENT_TYPE_DOUBLE:
                to_return[components * i + c] = value

    return to_return

def get_float_buffer(model: GLTFModel,
                     accessor: GLTFAccessor,
                     decode_normalized: bool=False) -> list[float]:
    components: int = get_num_components_in_type(accessor.type)
    component_type: int = accessor.component_type
    buffer_view: GLTFBufferView = model.buffer_views[accessor.buffer_view]

    return read_float_buffer_view(model, buffer_view, component_type, accessor.byte_offset, components, accessor.count, decode_normalized)

def read_integer_buffer_view(model: GLTFModel,
                             buffer_view: GLTFBufferView,
                             component_type: int,
                             byte_offset: int,
                             components: int,
                             count: int) -> list[int]:
    buffer: GLTFBuffer = model.buffers[buffer_view.buffer]
    component_size: int = get_component_size_in_bytes(component_type)
    byte_stride: int = components * component_size if buffer_view.byte_stride == 0 else buffer_view.byte_stride
    index_stride: int = byte_stride // component_size
    to_return: list[int] = [0] * (components * count)

    for i in range(count):
        for c in range(components):
            buffer_start: int = buffer_view.byte_offset + byte_offset + (i * index_stride + c) * component_size
            buffer_part = buffer.data[buffer_start:buffer_start + component_size]
            value: int = struct.unpack(component_type_to_format(component_type), bytearray(buffer_part))[0]
            to_return[components * i + c] = value

    return to_return

def get_integer_buffer(model: GLTFModel,
                       accessor: GLTFAccessor) -> list[int]:
    components: int = get_num_components_in_type(accessor.type)
    component_type: int = accessor.component_type
    
    buffer_view: GLTFBufferView = model.buffer_views[accessor.buffer_view]
    return read_integer_buffer_view(model, buffer_view, component_type, accessor.byte_offset, components, accessor.count)

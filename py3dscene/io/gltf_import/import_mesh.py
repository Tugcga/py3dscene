import struct
from py3dscene.bin.tiny_gltf import Model as GLTFModel  # type: ignore
from py3dscene.bin.tiny_gltf import Mesh as GLTFMesh  # type: ignore
from py3dscene.bin.tiny_gltf import Primitive as GLTFPrimitive  # type: ignore
from py3dscene.bin.tiny_gltf import Accessor as GLTFAccessor  # type: ignore
from py3dscene.bin.tiny_gltf import BufferView as GLTFBufferView  # type: ignore
from py3dscene.bin.tiny_gltf import get_component_size_in_bytes
from py3dscene.bin.tiny_gltf import get_num_components_in_type
from py3dscene.io.gltf_import.import_buffer import component_type_to_format
from py3dscene.io.gltf_import.import_buffer import get_float_buffer
from py3dscene.io.gltf_import.import_buffer import get_integer_buffer
from py3dscene.io.gltf_import.import_buffer import read_float_buffer_view
from py3dscene.io.gltf_import.import_buffer import read_integer_buffer_view
from py3dscene.object import Object
from py3dscene.material import PBRMaterial
from py3dscene.mesh import MeshComponent

def get_polygon_indices(model: GLTFModel,
                        primitive: GLTFPrimitive,
                        model_buffers_data: list[list[int]],
                        first_index: int) -> list[int]:
    if primitive.indices >= 0:
        polygon_accessor: GLTFAccessor = model.accessors[primitive.indices]
        component_type: int = polygon_accessor.component_type
        to_return: list[int] = [0] * polygon_accessor.count

        buffer_view: GLTFBufferView = model.buffer_views[polygon_accessor.buffer_view]
        buffer_data: list[int] = model_buffers_data[buffer_view.buffer]

        count: int = polygon_accessor.count

        component_size: int = get_component_size_in_bytes(component_type)
        byte_stride: int = component_size if buffer_view.byte_stride == 0 else buffer_view.byte_stride
        index_stride: int = byte_stride // component_size

        for i in range(count):
            buffer_start = buffer_view.byte_offset + polygon_accessor.byte_offset + i * index_stride * component_size
            buffer_part = buffer_data[buffer_start:buffer_start + component_size]
            to_return[i] = struct.unpack(component_type_to_format(component_type), bytearray(buffer_part))[0] + first_index
        
        return to_return
    else:
        return []

def attribute_length(name: str) -> int:
    if name == "NORMAL" or name.find("TEXCOORD") == 0:
        return 3
    elif name.find("COLOR") == 0:
        return 4
    else:
        return 0

def add_shape_target(gltf_model: GLTFModel,
                     model_buffers_data: list[list[int]],
                     gltf_shape: dict[str, int],
                     shape_name: str,
                     mesh: MeshComponent):
    if shape_name in gltf_shape:
        acc_index: int = gltf_shape[shape_name]
        shape_accessor: GLTFAccessor = gltf_model.accessors[acc_index]
        shape_values: list[float] = []
        if shape_accessor.sparse.is_sparse:
            values: list[float] = read_float_buffer_view(
                gltf_model,
                gltf_model.buffer_views[shape_accessor.sparse.values.buffer_view],
                shape_accessor.component_type,
                shape_accessor.sparse.values.byte_offset,
                get_num_components_in_type(shape_accessor.type),
                shape_accessor.sparse.count,
                False)

            indices: list[int] = read_integer_buffer_view(
                gltf_model,
                gltf_model.buffer_views[shape_accessor.sparse.indices.buffer_view],
                shape_accessor.sparse.indices.component_type,
                shape_accessor.sparse.indices.byte_offset,
                1,
                shape_accessor.sparse.count)

            shape_values = [0.0] * (3 * mesh.get_vertex_count())
            for i in range(len(indices)):
                index: int = indices[i]
                shape_values[3 * index] = values[3 * i]
                shape_values[3 * index + 1] = values[3 * i + 1]
                shape_values[3 * index + 2] = values[3 * i + 2]
        else:
            shape_values = get_float_buffer(gltf_model, shape_accessor, model_buffers_data)
        mesh.add_shape([(shape_values[3 * i], shape_values[3 * i + 1], shape_values[3 * i + 2]) for i in range(len(shape_values) // 3)])

def import_object_mesh(gltf_model: GLTFModel,
                       gltf_mesh: GLTFMesh,
                       model_buffers_data: list[list[int]],
                       object: Object,
                       materials_map: dict[int, PBRMaterial],
                       envelop_map: dict[int, list[float]]):
    for primitive_index in range(len(gltf_mesh.primitives)):
        gltf_primitive: GLTFPrimitive = gltf_mesh.primitives[primitive_index]
        position_attr_index: int = gltf_primitive.attributes["POSITION"]
        position_accessor: GLTFAccessor = gltf_model.accessors[position_attr_index]
        positions: list[float] = get_float_buffer(gltf_model, position_accessor, model_buffers_data)
        if len(positions) == 0:
            continue

        triangles: list[int] = get_polygon_indices(gltf_model, gltf_primitive, model_buffers_data, 0)
        vertex_count: int = len(positions) // 3
        triangles_count: int = len(triangles) // 3
        samples_count: int = len(triangles)
        trivial_triangles: list[int] = []
        for t in range(triangles_count):
            a: int = triangles[3 * t]
            b: int = triangles[3 * t + 1]
            c: int = triangles[3 * t + 2]
            if a == b or a == c or b == c:
                trivial_triangles.append(t)
        trivial_triangles_count: int = len(trivial_triangles)

        if len(triangles) == 0:
            continue

        if triangles_count <= trivial_triangles_count:
            continue
        
        vertices: list[tuple[float, float, float]] = []
        for v_index in range(vertex_count):
            vertices.append((positions[3 * v_index], positions[3 * v_index + 1], positions[3 * v_index + 2]))
        polygons: list[tuple[int, ...]] = []
        for t_index in range(triangles_count):
            if t_index not in trivial_triangles:
                polygons.append((triangles[3 * t_index], triangles[3 * t_index + 1], triangles[3 * t_index + 2]))
        # create the mesh
        mesh: MeshComponent = MeshComponent(vertices, polygons)

        material_index: int = gltf_primitive.material
        if material_index in materials_map:
            material: PBRMaterial = materials_map[material_index]
            mesh.set_material(material)

        skin_joints: list[int] = []
        skin_weights: list[float] = []
            
        for attribute_name, attribute_acc in gltf_primitive.attributes.items():
            accessor: GLTFAccessor = gltf_model.accessors[attribute_acc]
            if attribute_name == "POSITION":
                continue

            triangle_index: int = 0
            v: int = 0

            if attribute_name == "NORMAL":
                normals: list[float] = get_float_buffer(gltf_model, accessor, model_buffers_data)
                normals_attr: list[tuple[float, float, float]] = []
                for i in range(samples_count):
                    triangle_index = i // 3
                    if triangle_index in trivial_triangles:
                        continue

                    v = triangles[i]
                    normals_attr.append((normals[3 * v], normals[3 * v + 1], normals[3 * v + 2]))
                mesh.add_normals(normals_attr)
            elif attribute_name.find("TEXCOORD") == 0:
                uvs: list[float] = get_float_buffer(gltf_model, accessor, model_buffers_data)
                uvs_attr: list[tuple[float, float]] = []
                for i in range(samples_count):
                    triangle_index = i // 3
                    if triangle_index in trivial_triangles:
                        continue

                    v = triangles[i]
                    uvs_attr.append((uvs[2 * v], uvs[2 * v + 1]))
                mesh.add_uvs(uvs_attr)
            elif attribute_name.find("COLOR") == 0:
                colors: list[float] = get_float_buffer(gltf_model, accessor, model_buffers_data)
                colors_attr_plain: list[float] = []
                components: int = get_num_components_in_type(accessor.type)
                colors_type: int = accessor.component_type
                for i in range(samples_count):
                    triangle_index = i // 3
                    if triangle_index in trivial_triangles:
                        continue
                    v = triangles[i]
                    for c in range(components):
                        if colors_type == 5121:
                            colors_attr_plain.append(colors[components * v + c] / 255.0)
                        elif colors_type == 5123:
                            colors_attr_plain.append(colors[components * v + c] / 65535.0)
                        else:
                            colors_attr_plain.append(colors[components * v + c])
                    for c in range(components, 4):
                        colors_attr_plain.append(1.0)
                mesh.add_colors([(colors_attr_plain[4 * i], colors_attr_plain[4 * i + 1], colors_attr_plain[4 * i + 2], colors_attr_plain[4 * i + 3]) for i in range(len(colors_attr_plain) // 4)])
            elif attribute_name.find("JOINTS") == 0:
                joints: list[int] = get_integer_buffer(gltf_model, accessor, model_buffers_data)
                skin_joints.extend(joints)
            elif attribute_name.find("WEIGHTS") == 0:
                weights: list[float] = get_float_buffer(gltf_model, accessor, model_buffers_data)
                skin_weights.extend(weights)
            elif attribute_name == "TANGENT":
                tangents: list[float] = get_float_buffer(gltf_model, accessor, model_buffers_data)
                tangents_attr: list[tuple[float, float, float, float]] = []
                for i in range(samples_count):
                    triangle_index = i // 3
                    if triangle_index in trivial_triangles:
                        continue

                    v = triangles[i]
                    tangents_attr.append((tangents[4 * v], tangents[4 * v + 1], tangents[4 * v + 2], tangents[4 * v + 3]))
                mesh.add_tangents(tangents_attr)
        # finish iterate throw attributes
        # variables skin_joints and skin_weights contains data for subobject skinning
        # TODO: implement skinning import
        
        # next iterate throw shape deforms
        for shape_index in range(len(gltf_primitive.targets)):
            gltf_shape: dict[str, int] = gltf_primitive.targets[shape_index]
            add_shape_target(gltf_model, model_buffers_data, gltf_shape, "POSITION", mesh)
        
        # add mesh component to the object
        object.add_mesh_component(mesh)

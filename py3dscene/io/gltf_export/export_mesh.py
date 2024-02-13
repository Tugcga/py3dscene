import math
import struct
import sys
from py3dscene.bin import tiny_gltf
from py3dscene.io.gltf_export.export_buffer import add_triangle_indices_to_buffer
from py3dscene.io.gltf_export.export_buffer import add_data_to_buffer
from py3dscene.object import Object
from py3dscene.material import PBRMaterial

EPSILON: float = 0.001

VertexType = tuple[
                tuple[float, float, float],  # position
                list[tuple[float, float, float]],  # normals
                list[tuple[float, float]],  # uvs
                list[tuple[float, float, float, float]],  # colors
                list[tuple[float, float, float, float]],  # tangents
                list[tuple[float, float, float]],  # shape deltas
            ]
def distance2(a: tuple[float, float],
              b: tuple[float, float]) -> float:
    return math.sqrt(sum([(a[i] - b[i])**2 for i in range(2)]))

def distance3(a: tuple[float, float, float],
              b: tuple[float, float, float]) -> float:
    return math.sqrt(sum([(a[i] - b[i])**2 for i in range(3)]))

def distance4(a: tuple[float, float, float, float],
              b: tuple[float, float, float, float]) -> float:
    return math.sqrt(sum([(a[i] - b[i])**2 for i in range(4)]))

def get_index_from_vertex_array(array: list[VertexType], value: VertexType) -> int:
    for i, v in enumerate(array):
        is_next = False
        # return -1 if value is different with array element (in some place)
        # check positions
        if distance3(v[0], value[0]) > EPSILON:
            continue
        # check normals
        if len(v[1]) != len(value[1]):
            continue
        for j in range(len(v[1])):
            if distance3(v[1][j], value[1][j]) > EPSILON:
                is_next = True
                continue
        if is_next:
            continue
        # check uvs
        if len(v[2]) != len(value[2]):
            continue
        for j in range(len(v[2])):
            if distance2(v[2][j], value[2][j]) > EPSILON:
                is_next = True
                continue
        if is_next:
            continue
        # colors
        if len(v[3]) != len(value[3]):
            continue
        for j in range(len(v[3])):
            if distance4(v[3][j], value[3][j]) > EPSILON:
                is_next = False
                continue
        if is_next:
            continue
        # tangents
        if len(v[4]) != len(value[4]):
            continue
        for j in range(len(v[4])):
            if distance4(v[4][j], value[4][j]) > EPSILON:
                is_next = False
                continue
        if is_next:
            continue
        # shapes
        if len(v[5]) != len(value[5]):
            continue
        for j in range(len(v[5])):
            if distance3(v[5][j], value[5][j]) > EPSILON:
                is_next = False
                continue
        if is_next:
            continue
        # if we pass all checks then value coincide with v
        # return the index
        return i
    return -1

def export_mesh(gltf_model_buffers_data: list[int],
                gltf_model_buffer_views: list[tiny_gltf.BufferView],
                gltf_model_accessors: list[tiny_gltf.Accessor],
                gltf_model_meshes: list[tiny_gltf.Mesh],
                gltf_node: tiny_gltf.Node,
                object: Object,
	            materials_map: dict[int, int],
                # TODO: implement export skin and use envelope_meshes
	            envelope_meshes: list[Object],
                optimize_mesh_nodes: bool):
    gltf_mesh = tiny_gltf.Mesh()
    gltf_mesh_primitives: list[tiny_gltf.Primitive] = []
    for mesh in object.get_mesh_components():
        gltf_primitive = tiny_gltf.Primitive()

        material: PBRMaterial = mesh.get_material()
        material_id: int = material.get_id()
        if material_id != -1 and material_id not in materials_map:
            # id = -1 only for default material
            # if mesh component contains this material, then it is not defined
            # so, nothing to export
            pass
        mesh_vertices: list[tuple[float, float, float]] = mesh.get_vertices()
        mesh_triangles: list[tuple[int, int, int]] = mesh.get_triangulation()
        
        # store in separate list all vertices we should export
        # if node in the mesh have the same position and attributes, then it's the same vertex
        # but if at least one attribute is different, then create the new vertex
        vertices: list[VertexType] = [] if optimize_mesh_nodes else [((0.0, 0.0, 0.0),
                                                                      [], [], [], [], [])] * len(mesh_vertices)
        # here we will store actual triangles for export
        # with indices of vertices from the previous array
        triangles: list[tuple[int, int, int]] = []
        for triangle_index, triangle_vertices in enumerate(mesh_triangles):
            triangle_nodes = mesh.get_triangle_nodes(triangle_index)
            triangle_array: list[int] = []
            # for each triangle corner form new vertex
            for i in range(3):
                v_index = triangle_vertices[i]
                n_index = triangle_nodes[i]
                vertex: VertexType = (mesh_vertices[v_index],
                                      mesh.get_node_normals(n_index),
                                      mesh.get_node_uvs(n_index),
                                      mesh.get_node_colors(n_index),
                                      mesh.get_node_tangents(n_index),
                                      mesh.get_vertex_shapes(v_index))
                if optimize_mesh_nodes:
                    # check is this vertex is new
                    index: int = get_index_from_vertex_array(vertices, vertex)
                    if index == -1:
                        # this is new vertex, add it to the array
                        index = len(vertices)
                        vertices.append(vertex)
                    # now index has the proper value
                    triangle_array.append(index)
                else:
                    vertices[v_index] = vertex
                    triangle_array.append(v_index)
            triangles.append((triangle_array[0], triangle_array[1], triangle_array[2]))
        # next we should write mesh data into gltf mesh primitive
        gltf_primitive.mode = tiny_gltf.TINYGLTF_MODE_TRIANGLES
        if material_id in materials_map:
            gltf_primitive.material = materials_map[material_id]
        gltf_mesh_primitives.append(gltf_primitive)
        # write to the buffer
        # triangle indices
        indices: int = add_triangle_indices_to_buffer(gltf_model_buffers_data,
                                                      gltf_model_buffer_views,
                                                      gltf_model_accessors,
                                                      triangles,
                                                      tiny_gltf.TINYGLTF_COMPONENT_TYPE_UNSIGNED_INT,
                                                      tiny_gltf.TINYGLTF_TYPE_SCALAR)
        gltf_primitive.indices = indices
        # before write positions and other attributes
        # we should convert it to plain arrays and calculate min and max values
        # store in arrays actual bytes representations
        buffer_positions: list[int] = []
        buffer_normals: list[list[int]] = [[] for _ in range(mesh.get_normals_count())]  # the number of arrays in the number of different normal attributes
        buffer_uvs: list[list[int]] = [[] for _ in range(mesh.get_uvs_count())]
        buffer_colors: list[list[int]] = [[] for _ in range(mesh.get_colors_count())]
        buffer_tangents: list[list[int]] = [[] for _ in range(mesh.get_tangents_count())]
        buffer_shapes: list[list[int]] = [[] for _ in range(mesh.get_shapes_count())]
        flt_max: float = sys.float_info.max
        flt_min: float = -sys.float_info.max
        min_positions: list[float] = [flt_max] * 3
        max_positions: list[float] = [flt_min] * 3
        # in these arrays we store min/max values for all attributes of the same type
        # first three values - for the first attribute and so on
        min_normals: list[float] = [flt_max] * 3 * mesh.get_normals_count()
        max_normals: list[float] = [flt_min] * 3 * mesh.get_normals_count()
        min_uvs: list[float] = [flt_max] * 2 * mesh.get_uvs_count()
        max_uvs: list[float] = [flt_min] * 2 * mesh.get_uvs_count()
        min_colors: list[float] = [flt_max] * 4 * mesh.get_colors_count()
        max_colors: list[float] = [flt_min] * 4 * mesh.get_colors_count()
        min_tangents: list[float] = [flt_max] * 4 * mesh.get_tangents_count()
        max_tangents: list[float] = [flt_min] * 4 * mesh.get_tangents_count()
        min_shapes: list[float] = [flt_max] * 3 * mesh.get_shapes_count()
        max_shapes: list[float] = [flt_min] * 3 * mesh.get_shapes_count()
        # iterate throw output vertices
        for vertex in vertices:
            # copy positions
            for i in range(3):
                v_coord: float = vertex[0][i]
                if v_coord < min_positions[i]:
                    min_positions[i] = v_coord
                if v_coord > max_positions[i]:
                    max_positions[i] = v_coord
                buffer_positions.extend(struct.pack("f", v_coord))
            # normals
            for i, n in enumerate(vertex[1]):
                for j in range(3):
                    n_coord: float = n[j]
                    if n_coord < min_normals[3 * i + j]:
                        min_normals[3 * i + j] = n_coord
                    if n_coord > max_normals[3 * i + j]:
                        max_normals[3 * i + j] = n_coord
                    buffer_normals[i].extend(struct.pack("f", n_coord))
            # uvs
            for i, uv in enumerate(vertex[2]):
                for j in range(2):
                    uv_coord: float = uv[j]
                    if uv_coord < min_uvs[2 * i + j]:
                        min_uvs[2 * i + j] = uv_coord
                    if uv_coord > max_uvs[2 * i + j]:
                        max_uvs[2 * i + j] = uv_coord
                    buffer_uvs[i].extend(struct.pack("f", uv_coord))
            # colors
            for i, c in enumerate(vertex[3]):
                for j in range(4):
                    c_coord: float = c[j]
                    if c_coord < min_colors[4 * i + j]:
                        min_colors[4 * i + j] = c_coord
                    if c_coord > max_colors[4 * i + j]:
                        max_colors[4 * i + j] = c_coord
                    buffer_colors[i].extend(struct.pack("f", c_coord))
            # tangents
            for i, t in enumerate(vertex[4]):
                for j in range(4):
                    t_coord: float = t[j]
                    if t_coord < min_tangents[4 * i + j]:
                        min_tangents[4 * i + j] = t_coord
                    if t_coord > max_tangents[4 * i + j]:
                        max_tangents[4 * i + j] = t_coord
                    buffer_tangents[i].extend(struct.pack("f", t_coord))
            # shapes
            for i, s in enumerate(vertex[5]):
                for j in range(3):
                    s_coord: float = s[j]
                    if s_coord < min_shapes[3 * i + j]:
                        min_shapes[3 * i + j] = s_coord
                    if s_coord > max_shapes[3 * i + j]:
                        max_shapes[3 * i + j] = s_coord
                    buffer_shapes[i].extend(struct.pack("f", s_coord))
        # now we are ready to write data to the buffer
        gltf_primitive_attributes: dict[str, int] = {}
        gltf_primitive_attributes["POSITION"] = add_data_to_buffer(gltf_model_buffers_data,
                                                                   gltf_model_buffer_views,
                                                                   gltf_model_accessors,
                                                                   buffer_positions,
                                                                   len(vertices),
                                                                   False,
                                                                   False,
                                                                   tiny_gltf.TINYGLTF_COMPONENT_TYPE_FLOAT,
                                                                   tiny_gltf.TINYGLTF_TYPE_VEC3,
                                                                   min_positions,
                                                                   max_positions)
        # glTF supports only one normals attribute
        if mesh.get_normals_count() > 0:
            gltf_primitive_attributes["NORMAL"] = add_data_to_buffer(gltf_model_buffers_data,
                                                                     gltf_model_buffer_views,
                                                                     gltf_model_accessors,
                                                                     buffer_normals[0],
                                                                     len(vertices),
                                                                     False,
                                                                     False,
                                                                     tiny_gltf.TINYGLTF_COMPONENT_TYPE_FLOAT,
                                                                     tiny_gltf.TINYGLTF_TYPE_VEC3,
                                                                     [min_normals[0], min_normals[1], min_normals[2]],
                                                                     [max_normals[0], max_normals[1], max_normals[2]])
        for uv_index in range(mesh.get_uvs_count()):
            gltf_primitive_attributes["TEXCOORD_" + str(uv_index)] = add_data_to_buffer(gltf_model_buffers_data,
                                                                     gltf_model_buffer_views,
                                                                     gltf_model_accessors,
                                                                     buffer_uvs[uv_index],
                                                                     len(vertices),
                                                                     False,
                                                                     False,
                                                                     tiny_gltf.TINYGLTF_COMPONENT_TYPE_FLOAT,
                                                                     tiny_gltf.TINYGLTF_TYPE_VEC2,
                                                                     [min_uvs[2 * uv_index], min_uvs[2 * uv_index + 1]],
                                                                     [max_uvs[2 * uv_index], max_uvs[2 * uv_index + 1]])
        for color_index in range(mesh.get_colors_count()):
            gltf_primitive_attributes["COLOR_" + str(color_index)] = add_data_to_buffer(gltf_model_buffers_data,
                                                                     gltf_model_buffer_views,
                                                                     gltf_model_accessors,
                                                                     buffer_colors[color_index],
                                                                     len(vertices),
                                                                     False,
                                                                     False,
                                                                     tiny_gltf.TINYGLTF_COMPONENT_TYPE_FLOAT,
                                                                     tiny_gltf.TINYGLTF_TYPE_VEC4,
                                                                     [min_colors[4 * color_index], min_colors[4 * color_index + 1], min_colors[4 * color_index + 2], min_colors[4 * color_index + 3]],
                                                                     [max_colors[4 * color_index], max_colors[4 * color_index + 1], max_colors[4 * color_index + 2], max_colors[4 * color_index + 3]])
        # only one tangent attribute
        if mesh.get_tangents_count() > 0:
            gltf_primitive_attributes["TANGENT"] = add_data_to_buffer(gltf_model_buffers_data,
                                                                     gltf_model_buffer_views,
                                                                     gltf_model_accessors,
                                                                     buffer_tangents[0],
                                                                     len(vertices),
                                                                     False,
                                                                     False,
                                                                     tiny_gltf.TINYGLTF_COMPONENT_TYPE_FLOAT,
                                                                     tiny_gltf.TINYGLTF_TYPE_VEC4,
                                                                     [min_tangents[0], min_tangents[1], min_tangents[2], min_tangents[3]],
                                                                     [max_tangents[0], max_tangents[1], max_tangents[2], max_tangents[3]])
        # finally, shapes
        # but shapes should be stored on vector of targets dictionary
        gltf_primitive_targets: list[dict[str, int]] = [{} for _ in range(mesh.get_shapes_count())]
        for shape_index in range(mesh.get_shapes_count()):
            gltf_primitive_targets[shape_index]["POSITION"] = add_data_to_buffer(gltf_model_buffers_data,
                                                                     gltf_model_buffer_views,
                                                                     gltf_model_accessors,
                                                                     buffer_shapes[shape_index],
                                                                     len(vertices),
                                                                     False,
                                                                     False,
                                                                     tiny_gltf.TINYGLTF_COMPONENT_TYPE_FLOAT,
                                                                     tiny_gltf.TINYGLTF_TYPE_VEC3,
                                                                     [min_shapes[shape_index * 3], min_shapes[shape_index * 3 + 1], min_shapes[shape_index * 3 + 2]],
                                                                     [max_shapes[shape_index * 3], max_shapes[shape_index * 3 + 1], max_shapes[shape_index * 3 + 2]])
        
        gltf_primitive.attributes = gltf_primitive_attributes
        gltf_primitive.targets = gltf_primitive_targets
        
    gltf_mesh.primitives = gltf_mesh_primitives
    gltf_node.mesh = len(gltf_model_meshes)
    gltf_model_meshes.append(gltf_mesh)

from typing import Optional
from py3dscene.material import PBRMaterial
from py3dscene.material import get_default_material

class MeshComponent:
    '''Class for store mesh data of 3d-scene objects
    '''
    def __init__(self,
                 vertices: list[tuple[float, float, float]],
                 polygons: list[tuple[int, ...]]) -> None:
        self._vertices: list[tuple[float, float, float]] = [v for v in vertices]
        self._vertex_count = len(self._vertices)
        self._polygons: list[tuple[int, ...]] = [tuple(p) for p in polygons]
        self._polygons_sizes = [len(p) for p in self._polygons]
        self._polygons_count = len(self._polygons)

        self._material = get_default_material()
        # nodes are corners of polygons
        # the total number of nodes is the sum of polygon lengths
        self._nodes_count: int = sum(self._polygons_sizes)

        # each attribute we store as a list with values for each node
        # first list element is array of attribute values for the first node and so on
        # each node can contains several values for some attribute (uv, for example)
        self._normals_count: int = 0
        self._uvs_count: int = 0
        self._colors_count: int = 0
        self._tangent_count: int = 0
        self._shapes_count: int = 0
        self._normals: list[list[tuple[float, float, float]]] = [[] for _ in range(self._nodes_count)]
        self._uvs: list[list[tuple[float, float]]] = [[] for _ in range(self._nodes_count)]
        self._colors: list[list[tuple[float, float, float, float]]] = [[] for _ in range(self._nodes_count)]
        self._tangents: list[list[tuple[float, float, float, float]]] = [[] for _ in range(self._nodes_count)]

        # as shape we store deltas for point positions
        # mesh can store several shapes, so, for each vertex we store a list with values for different shapes
        self._shapes: list[list[tuple[float, float, float]]] = [[] for _ in range(self._vertex_count)]
        # TODO: store also displacements for normals, tangents, uvs and colors
        # how many values these shapes should contains? the same as node count?

        # for exports we need mesh triangulation
        # we should not only to split polygons into triangles, but also create the map from triangle to polygon node
        # this will allow to obtain valid node attributes
        # in _triangles array we store vertex indices for each triangle
        self._triangles: list[tuple[int, int, int]] = []
        # _triangles_to_node array contains node indices for each triangle
        self._triangles_to_node: list[tuple[int, int, int]] = []
        size_accum: int = 0
        for polygon in self._polygons:
            # for each polygon (a, b, c, d ,...)
            # we create several triangles (a, b, c), (a, c, d), ...
            size: int = len(polygon)
            for i in range(2, size):
                self._triangles.append((polygon[0], polygon[i - 1], polygon[i]))
                self._triangles_to_node.append((size_accum, size_accum + i - 1, size_accum + i))
            size_accum += size
    
    def set_material(self, material: PBRMaterial):
        '''Define material fo the mesh component
        '''
        self._material = material
    
    def add_normals(self, normals: list[tuple[float, float, float]]):
        '''Add normals attribute to the mesh component
        '''
        for n in range(min(len(normals), self._nodes_count)):
            self._normals[n].append(normals[n])
        for non_n in range(len(normals), self._nodes_count):
            self._normals[non_n].append((0.0, 0.0, 0.0))
        self._normals_count += 1

    def add_uvs(self, uvs: list[tuple[float, float]]):
        '''Add uvs attributes to the mesh components
        '''
        for n in range(min(len(uvs), self._nodes_count)):
            self._uvs[n].append(uvs[n])
        for non_n in range(len(uvs), self._nodes_count):
            self._uvs[non_n].append((0.0, 0.0))
        self._uvs_count += 1

    def add_colors(self, colors: list[tuple[float, float, float, float]]):
        '''Add vertex colors attribute to the mesh component
        '''
        for n in range(min(len(colors), self._nodes_count)):
            self._colors[n].append(colors[n])
        for non_n in range(len(colors), self._nodes_count):
            self._colors[non_n].append((0.0, 0.0, 0.0, 0.0))
        self._colors_count += 1

    def add_tangents(self, tangents: list[tuple[float, float, float, float]]):
        '''Add tangents attribute to the mesh component
        '''
        for n in range(min(len(tangents), self._nodes_count)):
            self._tangents[n].append(tangents[n])
        for non_n in range(len(tangents), self._nodes_count):
            self._tangents[non_n].append((0.0, 0.0, 0.0, 0.0))
        self._tangent_count += 1

    def add_shape(self, values: list[tuple[float, float, float]]):
        '''Add shape deform attribute to the mesh component
        This deformation define displacement of the mesh vertices
        Input array store delta vectors of the displacement
        '''
        for v in range(min(len(values), self._vertex_count)):
            self._shapes[v].append(values[v])
        for non_v in range(len(values), self._vertex_count):
            self._shapes[non_v].append((0.0, 0.0, 0.0))
        self._shapes_count += 1

    def get_vertex_count(self) -> int:
        '''Return the number of vertices of the mesh
        '''
        return self._vertex_count
    
    def get_vertices(self) -> list[tuple[float, float, float]]:
        '''Return the list with vertex positions
        '''
        return self._vertices
    
    def get_polygons(self) -> list[tuple[int, ...]]:
        '''Return the list with polygon indices
        '''
        return self._polygons
    
    def get_polygons_sizes(self) -> list[int]:
        '''Return the list with polygon sizes
        '''
        return self._polygons_sizes
    
    def get_polygon_size(self, index: int) -> int:
        '''Return the size of the polygon with specific index
        If the index is invalid, then return 0
        '''
        if index < self._polygons_count:
            return self._polygons_sizes[index]
        else:
            return 0

    def get_material(self) -> PBRMaterial:
        '''Return assigned material of the mesh component
        If material was not assigned, then return default material
        '''
        return self._material
    
    def get_normals_count(self) -> int:
        '''Return the number of normals attributes in the mesh component
        '''
        return self._normals_count

    def get_normals(self, index: int=0) -> Optional[list[tuple[float, float, float]]]:
        '''Return array with normals attributes with specific index
        Each mesh can contains several normals attributes
        '''
        if len(self._normals[0]) > index:
            return [v[index] for v in self._normals]
        else:
            return None
    
    def get_uvs_count(self) -> int:
        '''Return the number of uvs attributes in the mesh component
        '''
        return self._uvs_count
    
    def get_uvs(self, index: int=0) -> Optional[list[tuple[float, float]]]:
        '''Return array with uvs attributes with specific index
        Each mesh can contains several uvs attributes
        '''
        if len(self._uvs[0]) > index:
            return [v[index] for v in self._uvs]
        else:
            return None
    
    def get_colors_count(self) -> int:
        '''Return the number of colors attributes in the mesh component
        '''
        return self._colors_count
    
    def get_colors(self, index: int=0) -> Optional[list[tuple[float, float, float, float]]]:
        '''Return array with vertex colors  attributes with specific index
        Each mesh can contains several vertex colors attributes
        '''
        if len(self._colors[0]) > index:
            return [v[index] for v in self._colors]
        else:
            return None
    
    def get_tangents_count(self) -> int:
        '''Return the number of tangents attributes in the mesh component
        '''
        return self._tangent_count
    
    def get_tangents(self, index: int=0) -> Optional[list[tuple[float, float, float, float]]]:
        '''Return array with tangents attributes with specific index
        Each mesh can contains several tangents attributes
        '''
        if len(self._tangents[0]) > index:
            return [v[index] for v in self._tangents]
        else:
            return None
    
    def get_shapes_count(self) -> int:
        return self._shapes_count
    
    def get_triangulation(self) -> list[tuple[int, int, int]]:
        '''Return array of 3-tuples with vertex indices for triangles
        '''
        return self._triangles
    
    def get_triangle_nodes(self, index: int) -> tuple[int, int, int]:
        '''Return node indices for a given triangle (with input index)
        '''
        return self._triangles_to_node[index]
    
    def get_node_normals(self, node_index: int) -> list[tuple[float, float, float]]:
        '''Return all normals for a given node
        '''
        return self._normals[node_index]
    
    def get_node_uvs(self, node_index: int) -> list[tuple[float, float]]:
        '''Return all uvs for a given node
        '''
        return self._uvs[node_index]
    
    def get_node_colors(self, node_index: int) -> list[tuple[float, float, float, float]]:
        '''Return all colors for a given node
        '''
        return self._colors[node_index]
    
    def get_node_tangents(self, node_index: int) -> list[tuple[float, float, float, float]]:
        '''Return all tangents for a given node
        '''
        return self._tangents[node_index]
    
    def get_vertex_shapes(self, index: int) -> list[tuple[float, float, float]]:
        '''Return array with shape deform deltas for a given vertex
        '''
        return self._shapes[index]
    
    def __str__(self) -> str:
        return f"Mesh {self._vertex_count} vertices, {self._polygons_count} polygons, material {self._material}"

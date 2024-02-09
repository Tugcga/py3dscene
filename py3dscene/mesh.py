from typing import Optional
from py3dscene.material import PBRMaterial
from py3dscene.material import get_default_material

class MeshComponent:
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
        self._normals: list[list[tuple[float, float, float]]] = [[] for _ in range(self._nodes_count)]
        self._uvs: list[list[tuple[float, float]]] = [[] for _ in range(self._nodes_count)]
        self._colors: list[list[tuple[float, float, float, float]]] = [[] for _ in range(self._nodes_count)]
        self._tangents: list[list[tuple[float, float, float, float]]] = [[] for _ in range(self._nodes_count)]

        # as shape we store deltas for point positions
        # mesh can store several shapes, so, for each vertex we store a list with values for different shapes
        self._shapes: list[list[tuple[float, float, float]]] = [[] for _ in range(self._vertex_count)]
        # TODO: store also displacements for normals, tangents, uvs and colors
        # how many values these shapes should contains? the same as node count?
    
    def set_material(self, material: PBRMaterial):
        self._material = material
    
    def add_normals(self, normals: list[tuple[float, float, float]]):
        for n in range(min(len(normals), self._nodes_count)):
            self._normals[n].append(normals[n])
        for non_n in range(len(normals), self._nodes_count):
            self._normals[non_n].append((0.0, 0.0, 0.0))

    def add_uvs(self, uvs: list[tuple[float, float]]):
        for n in range(min(len(uvs), self._nodes_count)):
            self._uvs[n].append(uvs[n])
        for non_n in range(len(uvs), self._nodes_count):
            self._uvs[non_n].append((0.0, 0.0))

    def add_colors(self, colors: list[tuple[float, float, float, float]]):
        for n in range(min(len(colors), self._nodes_count)):
            self._colors[n].append(colors[n])
        for non_n in range(len(colors), self._nodes_count):
            self._colors[non_n].append((0.0, 0.0, 0.0, 0.0))

    def add_tangents(self, tangents: list[tuple[float, float, float, float]]):
        for n in range(min(len(tangents), self._nodes_count)):
            self._tangents[n].append(tangents[n])
        for non_n in range(len(tangents), self._nodes_count):
            self._tangents[non_n].append((0.0, 0.0, 0.0, 0.0))

    def add_shape(self, values: list[tuple[float, float, float]]):
        for v in range(min(len(values), self._vertex_count)):
            self._shapes[v].append(values[v])
        for non_v in range(len(values), self._vertex_count):
            self._shapes[non_v].append((0.0, 0.0, 0.0))

    def get_vertex_count(self) -> int:
        return self._vertex_count
    
    def get_vertices(self) -> list[tuple[float, float, float]]:
        return self._vertices
    
    def get_polygons(self) -> list[tuple[int, ...]]:
        return self._polygons
    
    def get_polygons_sizes(self) -> list[int]:
        return self._polygons_sizes
    
    def get_polygon_size(self, index: int) -> int:
        if index < self._polygons_count:
            return self._polygons_sizes[index]
        else:
            return 0

    def get_material(self) -> PBRMaterial:
        return self._material

    def get_normals(self, index: int=0) -> Optional[list[tuple[float, float, float]]]:
        if len(self._normals[0]) > index:
            return [v[index] for v in self._normals]
        else:
            return None
    
    def get_uvs(self, index: int=0) -> Optional[list[tuple[float, float]]]:
        if len(self._uvs[0]) > index:
            return [v[index] for v in self._uvs]
        else:
            return None
    
    def get_colors(self, index: int=0) -> Optional[list[tuple[float, float, float, float]]]:
        if len(self._colors[0]) > index:
            return [v[index] for v in self._colors]
        else:
            return None
    
    def get_tangents(self, index: int=0) -> Optional[list[tuple[float, float, float, float]]]:
        if len(self._tangents[0]) > index:
            return [v[index] for v in self._tangents]
        else:
            return None
    
    def __str__(self) -> str:
        return f"Mesh {self._vertex_count} vertices, {self._polygons_count} polygons, material {self._material}"

## py3dscene

The main goal of this module is to implement high level interface for geometric data in glTF files. This module can be used to load/export geometry data from/to glTF file. All low-level actions (like decoding buffers) are hidden in methods ```to_gltf``` and ```from_gltf```. Now it's sufficient to setup the scene, define objects and assign components (light, camera or mesh) to these objects.

## TinyGLTF binaries

The module require compiled bindings for [TinyGLTF](https://github.com/syoyo/tinygltf) module. Sources for these bindings contained in ```bin_src/FormatIO/``` It require ```pybind11```. Compile into the```py3dscene/bin/``` folder. So, this folder should contain the file ```tiny_gltf.pyd```

The module contains loader for pre-build binaries for Windows x64 Python 3.6 - 3.12. All these binaries placed in [release](https://github.com/Tugcga/py3dscene/releases/tag/1.0) page. The module search required binaries and if there are no ones, then it try to download proper version from this page.

## Supported geometric data

* Objects hierarchy
* Objects transformations
* Animations of transformations parameters
* Camera (perspective and orthographic)
* Three types of lights (point, spot and directional)
* Polygonal mesh with any number of the following attributes:
    * Normals
    * UVs
    * Vertex colors
    * Tangents
    * Vertex displacements for morph shapes
* Simple pbr-material

## How to use

#### Load scene from glTF

```python
from py3dscene.gltf_io import from_gltf

scene = from_gltf(file_path)
```

Obtain scene objects
```python
objects = scene.get_root_objects()
```

Get object transforms
```python
translation = object.get_translation()
rotation = object.get_rotation()
scale = object.get_scale()

matrix = object.get_transform()
```

Get object components
```python
meshes = object.get_mesh_components()
mesh = meshes[0]

camera = object.get_camera()

light = object.get_light()
```

Get mesh attributes
```python
positions = mesh.get_vertices()
normals = mesh.get_normals()
```

#### Export scene to glTF

Create the scene
```python
scene = Scene()
```

Define scene objects
```
obj = scene.create_object()
```

Define object position
```python
obj.set_local_translation(1.0, 2.0, 3.0)
```

Add mesh component to the object
```python
mesh = MeshComponent([(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 0.0, 1.0), (0.0, 0.0, 1.0)], [(0, 1, 2, 3)])

obj.add_mesh_component(mesh)
```

Export scene to glTF
```python
from py3dscene.gltf_io import to_gltf
to_gltf(scene, file_path)
```

## API

## Animation Objects

```python
class Animation()
```

Store animation clip


#### \_\_init\_\_

```python
def __init__(type: AnimationCurveType, value_components: int) -> None
```

Create animation clip object and store the curve for one parameter
Parameters:
* type - the type of the curve (Linear, Step or CubicSpline)
* value_components - the number of vector component for one value (3 for position, 4 for quaternion)


#### add\_keyframe

```python
def add_keyframe(frame: float, value: ValuesVariants) -> None
```

Add keyframe to the clip at specific frame and with specific value


#### get\_type

```python
def get_type() -> AnimationCurveType
```

Return type of the animation clip (linear, step or cubic)


#### get\_value\_components

```python
def get_value_components() -> int
```

Return the number of components in one value stored in the animation
For example, rotation stored as 4d-tuple, translation and scale as 3d-tuple
This value does not depend on the animation curve type


#### get\_frames

```python
def get_frames() -> list[float]
```

Return the list of all key frames


#### get\_value\_at\_frame

```python
def get_value_at_frame(frame: float) -> Optional[ValuesVariants]
```

Return value at specific key frame
If there are no key frame in the clip, then return None
This method does not interpolate values between different key frames


## CameraComponent Objects

```python
class CameraComponent()
```

Store the camera in the 3d-scene


#### \_\_init\_\_

```python
def __init__() -> None
```

Create camera object. No parameters required


#### set\_type

```python
def set_type(value: CameraType) -> None
```

Define the camera type (perspective or orthographic)


#### set\_clipping\_planes

```python
def set_clipping_planes(near: float, far: float) -> None
```

Define clipping planes of the camera


#### set\_perspective\_aspect

```python
def set_perspective_aspect(value: float) -> None
```

Define aspect ratio of the perspective camera


#### set\_perspective\_fov

```python
def set_perspective_fov(value: float) -> None
```

Define vertical field of view of the perspective camera


#### set\_orthographic\_size

```python
def set_orthographic_size(width: float, height: float) -> None
```

Define size of the orthographic camera


#### get\_type

```python
def get_type() -> CameraType
```

Return type of the camera


#### get\_clipping\_near

```python
def get_clipping_near() -> float
```

Return values of the near clipping plane of the camera


#### get\_clipping\_far

```python
def get_clipping_far() -> float
```

Return value of the far clipping plane of the camera


#### get\_perspective\_aspect

```python
def get_perspective_aspect() -> float
```

Return aspect raton of the perspective camera


#### get\_perspective\_fov

```python
def get_perspective_fov() -> float
```

Return vertical field of view of the perspective camera


#### get\_orthographic\_width

```python
def get_orthographic_width() -> float
```

Return width of the orthographic camera


#### get\_orthographic\_height

```python
def get_orthographic_height() -> float
```

Return height of the orthographic camera


## gltf_io

#### from\_gltf

```python
def from_gltf(file_path: str, fps: float = 30.0) -> Scene
```

Create and return Scene object, which contains default scene from input gltf/glb file
Parameter fps is used for animations
glTF format store animation keyframes in seconds, but more traditional way is to store it in frames
parameter fps used to convert seconds-related values to frame-related values


#### to\_gltf

```python
def to_gltf(scene: Scene,
            file_path: str,
            optimize_mesh_nodes: bool = False,
            embed_images: bool = False,
            embed_buffers: bool = False,
            fps: float = 30.0) -> None
```

Export scene object as gltf or glb file
Parameters:
* file_path: full output path with extension
* optimize_mesh_nodes: if True, then in the export process the module try to reduce the number of vertices in the output meshes.   In the mesh it's possible to have one vertex and different normals in polygons incident to this vertex. If optimization is ON, then the exporter check is polygon nodes have different attributes or not. If at least one attribute (position, normal, uv etc) is different, then it creates the new vertex. If all attributes the same, then use the same vertex. But this process is long for dense mesh. So, it's possible to deactivate this flag. If the flag is False then the output mesh have the same vertices as it is, node attributes are override by last node. If the mesh is imported from glTF, then it's ok, because all vertices already are splitted by difference in node attributes
* embed_images: if True then embed image data into output file and does not create separate texture files. If False then textures are stored in the same directory as the output file
* embed_buffers: if True then hte binary buffer is embedded into output file. If False then create the separate file *.bin
* fps: the number of frames per second for exporting animations. In 3d-scene animations are stored by using key-frames, but in glTF it use seconds. So, fps used for converting frames to seconds


## LightComponent Objects

```python
class LightComponent()
```

Store the light in the 3d-scene


#### \_\_init\_\_

```python
def __init__() -> None
```

Create light object. No parameters required


#### set\_name

```python
def set_name(value: str) -> None
```

Define the light name


#### set\_color

```python
def set_color(r: float, g: float, b: float) -> None
```

Define the light color


#### set\_strength

```python
def set_strength(value: float) -> None
```

Define the light intensity


#### set\_type

```python
def set_type(value: LightType) -> None
```

Define the light type (point, spot or directional)


#### set\_range

```python
def set_range(value: float) -> None
```

Define the light range


#### set\_spot\_angles

```python
def set_spot_angles(inner: float, outer: float) -> None
```

Define inner and outer angles for the spot light


#### get\_name

```python
def get_name() -> str
```

Return the light's name


#### get\_color

```python
def get_color() -> tuple[float, float, float]
```

Return the color of the light


#### get\_strength

```python
def get_strength() -> float
```

Return the light's intensity


#### get\_type

```python
def get_type() -> LightType
```

Return the light's type


#### get\_range

```python
def get_range() -> float
```

Return the light's range


#### get\_spot\_inner\_cone

```python
def get_spot_inner_cone() -> float
```

Return hte inner cone of the spot light


#### get\_spot\_outer\_cone

```python
def get_spot_outer_cone() -> float
```

Return the outer cone of the spot light


## Material Objects

```python
class PBRMaterial(Material)
```

Class to store parameters of the simple pbr-material


#### \_\_init\_\_

```python
def __init__(name: str = "", id: Optional[int] = None) -> None
```

Create material object. It's recommended to create materials by using scene method

Parameters:
    name - the name of the material
    id - preferred id value


#### set\_alpha\_mode

```python
def set_alpha_mode(value: AlphaMode) -> None
```

Define alpha mode of the material


#### set\_alpha\_cutoff

```python
def set_alpha_cutoff(value: float) -> None
```

Define cut-off level for the alpha of the material


#### set\_double\_sided

```python
def set_double_sided(value: bool) -> None
```

Set material double-sided (or not)


#### set\_albedo

```python
def set_albedo(r: float, g: float, b: float, a: float) -> None
```

Define albedo color of the material


#### set\_metalness

```python
def set_metalness(value: float) -> None
```

Define metalness value of the material


#### set\_roughness

```python
def set_roughness(value: float) -> None
```

Define roughness value of the material


#### set\_emissive

```python
def set_emissive(r: float, g: float, b: float) -> None
```

Define emissive value of the material


#### set\_albedo\_texture

```python
def set_albedo_texture(texture_path: str, uv_index: int) -> None
```

Define albedo texture of the material


#### set\_metallic\_roughness\_texture

```python
def set_metallic_roughness_texture(texture_path: str, uv_index: int) -> None
```

Define one texture for metallic and roughness of the material


#### set\_emissive\_texture

```python
def set_emissive_texture(texture_path: str, uv_index: int) -> None
```

Define emissive texture of the material


#### set\_normal\_texture

```python
def set_normal_texture(texture_path: str, uv_index: int,
                       strength: float) -> None
```

Define normal texture of the material


#### set\_occlusion\_texture

```python
def set_occlusion_texture(texture_path: str, uv_index: int,
                          strength: float) -> None
```

Define ambient occlusion texture of the material


#### get\_id

```python
def get_id() -> int
```

Return id of the material


#### get\_name

```python
def get_name() -> str
```

Return name of the material


#### get\_alpha\_mode

```python
def get_alpha_mode() -> AlphaMode
```

Return alpha mode of the material


#### get\_alpha\_cutoff

```python
def get_alpha_cutoff() -> float
```

Return cut-off value for the alpha of the material


#### get\_double\_sided

```python
def get_double_sided() -> bool
```

Return is the material is double-sided or not


#### get\_albedo

```python
def get_albedo() -> Color
```

Return albedo color of the material


#### get\_metalness

```python
def get_metalness() -> float
```

Return metalness value of the material


#### get\_roughness

```python
def get_roughness() -> float
```

Return roughness value of the material


#### get\_emissive

```python
def get_emissive() -> tuple[float, float, float]
```

Return emissive value of the material


#### get\_albedo\_texture\_path

```python
def get_albedo_texture_path() -> Optional[str]
```

Return path to the albedo texture of the material


#### get\_albedo\_texture\_uv

```python
def get_albedo_texture_uv() -> Optional[int]
```

Return uv index for the albedo texture


#### get\_metallic\_roughness\_texture\_path

```python
def get_metallic_roughness_texture_path() -> Optional[str]
```

Return path to the metallic and roughness texture of the material


#### get\_metallic\_roughness\_texture\_uv

```python
def get_metallic_roughness_texture_uv() -> Optional[int]
```

Return uv index for the metallic and roughness texture


#### get\_emissive\_texture\_path

```python
def get_emissive_texture_path() -> Optional[str]
```

Return path to the emissive texture of the material


#### get\_emissive\_texture\_uv

```python
def get_emissive_texture_uv() -> Optional[int]
```

Return uv index for the emissive texture


#### get\_normal\_texture\_path

```python
def get_normal_texture_path() -> Optional[str]
```

Return path to the normal texture of the material


#### get\_normal\_texture\_uv

```python
def get_normal_texture_uv() -> Optional[int]
```

Return uv index for the normal texture


#### get\_normal\_texture\_strength

```python
def get_normal_texture_strength() -> Optional[float]
```

Return the normal strength of the material


#### get\_occlusion\_texture\_path

```python
def get_occlusion_texture_path() -> Optional[str]
```

Return path to the ambient occlusion texture of the material


#### get\_occlusion\_texture\_uv

```python
def get_occlusion_texture_uv() -> Optional[int]
```

Return uv index for the ambient occlusion texture


#### get\_occlusion\_texture\_strength

```python
def get_occlusion_texture_strength() -> Optional[float]
```

Return the ambient occlusion strength of the material



```python
def __str__() -> str
```


#### default\_material



```python
def get_default_material() -> PBRMaterial
```

Return the global default material








## MeshComponent Objects

```python
class MeshComponent()
```

Class for store mesh data of 3d-scene objects


#### \_\_init\_\_

```python
def __init__(vertices: list[tuple[float, float, float]],
             polygons: list[tuple[int, ...]]) -> None
```

Create mesh object

Parameters:
    vertices - the list with coordinates of vertex positions
    polygons - list with tuples which describe polygons


#### set\_material

```python
def set_material(material: PBRMaterial) -> None
```

Define material fo the mesh component


#### add\_normals

```python
def add_normals(normals: list[tuple[float, float, float]]) -> None
```

Add normals attribute to the mesh component


#### add\_uvs

```python
def add_uvs(uvs: list[tuple[float, float]]) -> None
```

Add uvs attributes to the mesh components


#### add\_colors

```python
def add_colors(colors: list[tuple[float, float, float, float]]) -> None
```

Add vertex colors attribute to the mesh component


#### add\_tangents

```python
def add_tangents(tangents: list[tuple[float, float, float, float]]) -> None
```

Add tangents attribute to the mesh component


#### add\_shape

```python
def add_shape(values: list[tuple[float, float, float]]) -> None
```

Add shape deform attribute to the mesh component
This deformation define displacement of the mesh vertices
Input array store delta vectors of the displacement


#### get\_vertex\_count

```python
def get_vertex_count() -> int
```

Return the number of vertices of the mesh


#### get\_vertices

```python
def get_vertices() -> list[tuple[float, float, float]]
```

Return the list with vertex positions


#### get\_polygons

```python
def get_polygons() -> list[tuple[int, ...]]
```

Return the list with polygon indices


#### get\_polygons\_sizes

```python
def get_polygons_sizes() -> list[int]
```

Return the list with polygon sizes


#### get\_polygon\_size

```python
def get_polygon_size(index: int) -> int
```

Return the size of the polygon with specific index
If the index is invalid, then return 0


#### get\_material

```python
def get_material() -> PBRMaterial
```

Return assigned material of the mesh component
If material was not assigned, then return default material


#### get\_normals\_count

```python
def get_normals_count() -> int
```

Return the number of normals attributes in the mesh component


#### get\_normals

```python
def get_normals(index: int = 0) -> Optional[list[tuple[float, float, float]]]
```

Return array with normals attributes with specific index
Each mesh can contains several normals attributes


#### get\_uvs\_count

```python
def get_uvs_count() -> int
```

Return the number of uvs attributes in the mesh component


#### get\_uvs

```python
def get_uvs(index: int = 0) -> Optional[list[tuple[float, float]]]
```

Return array with uvs attributes with specific index
Each mesh can contains several uvs attributes


#### get\_colors\_count

```python
def get_colors_count() -> int
```

Return the number of colors attributes in the mesh component


#### get\_colors

```python
def get_colors(
        index: int = 0) -> Optional[list[tuple[float, float, float, float]]]
```

Return array with vertex colors  attributes with specific index
Each mesh can contains several vertex colors attributes


#### get\_tangents\_count

```python
def get_tangents_count() -> int
```

Return the number of tangents attributes in the mesh component


#### get\_tangents

```python
def get_tangents(
        index: int = 0) -> Optional[list[tuple[float, float, float, float]]]
```

Return array with tangents attributes with specific index
Each mesh can contains several tangents attributes


#### get\_shapes\_count

```python
def get_shapes_count() -> int
```


#### get\_triangulation

```python
def get_triangulation() -> list[tuple[int, int, int]]
```

Return array of 3-tuples with vertex indices for triangles


#### get\_triangle\_nodes

```python
def get_triangle_nodes(index: int) -> tuple[int, int, int]
```

Return node indices for a given triangle (with input index)


#### get\_node\_normals

```python
def get_node_normals(node_index: int) -> list[tuple[float, float, float]]
```

Return all normals for a given node


#### get\_node\_uvs

```python
def get_node_uvs(node_index: int) -> list[tuple[float, float]]
```

Return all uvs for a given node


#### get\_node\_colors

```python
def get_node_colors(
        node_index: int) -> list[tuple[float, float, float, float]]
```

Return all colors for a given node


#### get\_node\_tangents

```python
def get_node_tangents(
        node_index: int) -> list[tuple[float, float, float, float]]
```

Return all tangents for a given node


#### get\_vertex\_shapes

```python
def get_vertex_shapes(index: int) -> list[tuple[float, float, float]]
```

Return array with shape deform deltas for a given vertex



```python
def __str__() -> str
```

## Object Objects

```python
class Object()
```

Class for store object inside a 3d-scene

#### \_\_init\_\_

```python
def __init__(name: str = "", id: Optional[int] = None) -> None
```

Create object. It does not recommended to create objects manually, instead it's better to use the scene object method

Parameters:
    name - the name of the objects
    id - preferred id of the object


#### create\_subobject

```python
def create_subobject(name: str = "", id: Optional[int] = None) -> Object
```

Create and return a new object. Parent it to the current object
It's possible to define custom id for the new object
If id is not defines, then use the global counter
It's does not recommended to mix custom and automatic ids: use either only custom id's for all object all automatic ones


#### set\_local\_tfm

```python
def set_local_tfm(tfm: Transform) -> None
```

Define matrix of the local transformation of the object


#### set\_local\_translation

```python
def set_local_translation(x: float, y: float, z: float) -> None
```

Define position of the object


#### set\_local\_rotation

```python
def set_local_rotation(x: float, y: float, z: float, w: float) -> None
```

Define rotation of the object


#### set\_local\_scale

```python
def set_local_scale(x: float, y: float, z: float) -> None
```

Define scale of the object


#### set\_camera\_component

```python
def set_camera_component(camera: CameraComponent) -> None
```

Add camera component to the object


#### set\_light\_component

```python
def set_light_component(light: LightComponent) -> None
```

Add light component to the object


#### set\_translation\_animation

```python
def set_translation_animation(animation: Animation) -> None
```

Define translation animation of the object


#### set\_rotation\_animation

```python
def set_rotation_animation(animation: Animation) -> None
```

Define rotation animation of the object


#### set\_scale\_animation

```python
def set_scale_animation(animation: Animation) -> None
```

Define scale animation of the object


#### add\_mesh\_component

```python
def add_mesh_component(mesh: MeshComponent) -> None
```

Add mesh component to the object
Each object can contains several mesh components


#### get\_id

```python
def get_id() -> int
```

Return id of the object


#### get\_name

```python
def get_name() -> str
```

Return name of the object


#### get\_transform

```python
def get_transform() -> Transform
```

Return transformation matrix of the object


#### get\_translation

```python
def get_translation() -> tuple[float, float, float]
```

Return translation of the object


#### get\_rotation

```python
def get_rotation() -> tuple[float, float, float, float]
```

Return rotation of the object


#### get\_scale

```python
def get_scale() -> tuple[float, float, float]
```

Return scale of the object


#### is\_camera

```python
def is_camera() -> bool
```

Return True if the object contains camera component, False otherwise


#### get\_camera

```python
def get_camera() -> Optional[CameraComponent]
```

Return camera component of the object
If it does not assigned, then return None


#### is\_light

```python
def is_light() -> bool
```

Return True if the object contains light component, False otherwise


#### get\_light

```python
def get_light() -> Optional[LightComponent]
```

Return light component of the object
If it does not assigned, then return None


#### is\_mesh

```python
def is_mesh() -> bool
```

Return True if the object contains at least one mesh component, False otherwise


#### get\_mesh\_components

```python
def get_mesh_components() -> list[MeshComponent]
```

Return the full list of all mesh components of the object


#### get\_mesh\_components\_count

```python
def get_mesh_components_count() -> int
```

Return the number of mesh components (i.e. clusters or submeshes) of the object


#### get\_mesh\_component

```python
def get_mesh_component(index: int) -> Optional[MeshComponent]
```

Return mesh component of the object with specific index
If the index is invalid, then return None


#### get\_translation\_animation

```python
def get_translation_animation() -> Optional[Animation]
```

Return translation animation of the object
If it does node defined, then return None


#### get\_rotation\_animation

```python
def get_rotation_animation() -> Optional[Animation]
```

Return rotation animation of the object
If it does node defined, then return None


#### get\_scale\_animation

```python
def get_scale_animation() -> Optional[Animation]
```

Return scale animation of the object
If it does node defined, then return None


#### get\_object\_by\_id

```python
def get_object_by_id(id: int) -> Optional[Object]
```

Find and return the object with a given id
Search in the collection of this object and children sub-objects


#### get\_subobjects\_count

```python
def get_subobjects_count() -> int
```


#### get\_children

```python
def get_children() -> list[Object]
```



```python
def __str__() -> str
```

## Scene Objects

```python
class Scene()
```

Main class for store 3d-scene data


#### \_\_init\_\_

```python
def __init__() -> None
```

Create the scene object. No parameters required


#### create\_material

```python
def create_material(name: str = "", id: Optional[int] = None) -> PBRMaterial
```

Create and return material
It's recommended to create materials by this method
It automatically add material to the list in the scene object


#### get\_all\_materials

```python
def get_all_materials() -> list[PBRMaterial]
```

Return the full list of all materials in the scene


#### get\_material

```python
def get_material(id: int) -> PBRMaterial
```

Return material with a given id


#### create\_object

```python
def create_object(name: str = "", id: Optional[int] = None) -> Object
```

Create and return new object. This object parented to the root of the scene
It's possible to define the custom id for the new object


#### get\_object\_by\_id

```python
def get_object_by_id(id: int) -> Optional[Object]
```

Return object with a given id
If there are no such object return None


#### get\_objects\_count

```python
def get_objects_count() -> int
```

Return the number of objects in the root level of the scene


#### get\_root\_objects

```python
def get_root_objects() -> list[Object]
```

Return the list with objects in the root level of the scene



#### Transform

Transform matrix stored in column form
It means that the first column contains coordinates of the first transformed axis,
the second column - the second axis, the third column - the third axis and the last column - position of the origin
Last row is always (0.0, 0.0, 0.0, 1.0)

In this form transformed coordinates of the point (x, y, z) can be found:
(x_new, y_new, z_new)^t = T * (x, y, z)^t
Coordinates are columns


#### length

```python
def length(x: float, y: float, z: float) -> float
```

Return the length of the vector (x, y, z)


#### get\_identity

```python
def get_identity() -> Transform
```

Return matrix of the identity transform
1.0 0.0 0.0 0.0
0.0 1.0 0.0 0.0
0.0 0.0 1.0 0.0
0.0 0.0 0.0 1.0


#### get\_translation\_matrix

```python
def get_translation_matrix(x: float, y: float, z: float) -> Transform
```

Return matrix for the translation (x, y, z)


#### get\_rotation\_matrix

```python
def get_rotation_matrix(x: float, y: float, z: float, w: float) -> Transform
```

Return matrix for the rotation q = w + x * i 9 y * j + z * k


#### get\_scale\_matrix

```python
def get_scale_matrix(x: float, y: float, z: float) -> Transform
```

Return matrix for the scale transformation


#### get\_srt\_matrix

```python
def get_srt_matrix(translation: tuple[float, float, float],
                   rotation: tuple[float, float, float, float],
                   scale: tuple[float, float, float]) -> Transform
```

Return matrix for the transformation with given translation, rotation and scale
Calculate it in the order T * R * S (from right to left)


#### multiply

```python
def multiply(a: Transform, b: Transform) -> Transform
```

Return A * B


#### tfm\_to\_translation

```python
def tfm_to_translation(tfm: Transform) -> tuple[float, float, float]
```

Extract translation from transform matrix


#### tfm\_to\_rotation

```python
def tfm_to_rotation(tfm: Transform) -> tuple[float, float, float, float]
```

Extract rotation quaternion from transform matrix


#### tfm\_to\_scale

```python
def tfm_to_scale(tfm: Transform) -> tuple[float, float, float]
```

Extract scale from transform matrix
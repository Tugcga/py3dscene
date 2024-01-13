#define TINYGLTF_IMPLEMENTATION
#define STB_IMAGE_IMPLEMENTATION
#define STB_IMAGE_WRITE_IMPLEMENTATION

#include "tinygltf/tiny_gltf.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

tinygltf::Model load_gltf(const std::string filename) {
    tinygltf::Model model;
    tinygltf::TinyGLTF loader;
    std::string err;
    std::string warn;

    std::string::size_type point_pos = filename.rfind('.');
    bool is_binary = true;
    if (point_pos != std::string::npos) {
        std::string ext = filename.substr(point_pos + 1);
        if (ext == "gltf" || ext == "GLTF") {
            is_binary = false;
        }
    }

    if (is_binary) {
        bool is_ok = loader.LoadBinaryFromFile(&model, &err, &warn, filename);
    }
    else {
        bool is_ok = loader.LoadASCIIFromFile(&model, &err, &warn, filename);
    }
    
    return model;
}

bool save_gltf(const tinygltf::Model model, const std::string filename, bool embed_images, bool embed_buffers, bool pretty_print, bool write_binary) {
    tinygltf::TinyGLTF loader;

    return loader.WriteGltfSceneToFile(&model, filename, embed_images, embed_buffers, pretty_print, write_binary);
}

PYBIND11_MODULE(tiny_gltf, py_module) {
    py_module.doc() = "Bindings for tinygltf library";

    pybind11::class_<tinygltf::AnimationChannel>(py_module, "AnimationChannel")
        .def(pybind11::init<>())
        .def_readwrite("sampler", &tinygltf::AnimationChannel::sampler)
        .def_readwrite("target_node", &tinygltf::AnimationChannel::target_node)
        .def_readwrite("target_path", &tinygltf::AnimationChannel::target_path)
        .def_readwrite("extras_json_string", &tinygltf::AnimationChannel::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::AnimationChannel::extensions_json_string)
        .def_readwrite("target_extras_json_string", &tinygltf::AnimationChannel::target_extras_json_string)
        .def_readwrite("target_extensions_json_string", &tinygltf::AnimationChannel::target_extensions_json_string);

    pybind11::class_<tinygltf::AnimationSampler>(py_module, "AnimationSampler")
        .def(pybind11::init<>())
        .def_readwrite("input", &tinygltf::AnimationSampler::input)
        .def_readwrite("output", &tinygltf::AnimationSampler::output)
        .def_readwrite("interpolation", &tinygltf::AnimationSampler::interpolation)
        .def_readwrite("extras_json_string", &tinygltf::AnimationSampler::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::AnimationSampler::extensions_json_string);

    pybind11::class_<tinygltf::Animation>(py_module, "Animation")
        .def(pybind11::init<>())
        .def_readwrite("name", &tinygltf::Animation::name)
        .def_readwrite("channels", &tinygltf::Animation::channels)
        .def_readwrite("samplers", &tinygltf::Animation::samplers)
        .def_readwrite("extras_json_string", &tinygltf::Animation::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Animation::extensions_json_string);

    pybind11::class_<tinygltf::Skin>(py_module, "Skin")
        .def(pybind11::init<>())
        .def_readwrite("name", &tinygltf::Skin::name)
        .def_readwrite("inverse_bind_matrices", &tinygltf::Skin::inverseBindMatrices)
        .def_readwrite("skeleton", &tinygltf::Skin::skeleton)
        .def_readwrite("joints", &tinygltf::Skin::joints)
        .def_readwrite("extras_json_string", &tinygltf::Skin::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Skin::extensions_json_string);

    pybind11::class_<tinygltf::Sampler>(py_module, "Sampler")
        .def(pybind11::init<>())
        .def_readwrite("name", &tinygltf::Sampler::name)
        .def_readwrite("min_filter", &tinygltf::Sampler::minFilter)
        .def_readwrite("mag_filter", &tinygltf::Sampler::magFilter)
        .def_readwrite("wrap_s", &tinygltf::Sampler::wrapS)
        .def_readwrite("wrap_t", &tinygltf::Sampler::wrapT)
        .def_readwrite("extras_json_string", &tinygltf::Sampler::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Sampler::extensions_json_string);

    pybind11::class_<tinygltf::Image>(py_module, "Image")
        .def(pybind11::init<>())
        .def_readwrite("name", &tinygltf::Image::name)
        .def_readwrite("width", &tinygltf::Image::width)
        .def_readwrite("height", &tinygltf::Image::height)
        .def_readwrite("component", &tinygltf::Image::component)
        .def_readwrite("bits", &tinygltf::Image::bits)
        .def_readwrite("pixel_type", &tinygltf::Image::pixel_type)
        .def_readwrite("image", &tinygltf::Image::image)
        .def_readwrite("buffer_view", &tinygltf::Image::bufferView)
        .def_readwrite("mime_type", &tinygltf::Image::mimeType)
        .def_readwrite("uri", &tinygltf::Image::uri)
        .def_readwrite("extras_json_string", &tinygltf::Image::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Image::extensions_json_string)
        .def_readwrite("as_is", &tinygltf::Image::as_is);

    pybind11::class_<tinygltf::Texture>(py_module, "Texture")
        .def(pybind11::init<>())
        .def_readwrite("name", &tinygltf::Texture::name)
        .def_readwrite("sampler", &tinygltf::Texture::sampler)
        .def_readwrite("source", &tinygltf::Texture::source)
        .def_readwrite("extras_json_string", &tinygltf::Texture::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Texture::extensions_json_string);

    pybind11::class_<tinygltf::TextureInfo>(py_module, "TextureInfo")
        .def(pybind11::init<>())
        .def_readwrite("index", &tinygltf::TextureInfo::index)
        .def_readwrite("tex_coord", &tinygltf::TextureInfo::texCoord)
        .def_readwrite("extras_json_string", &tinygltf::TextureInfo::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::TextureInfo::extensions_json_string);

    pybind11::class_<tinygltf::NormalTextureInfo>(py_module, "NormalTextureInfo")
        .def(pybind11::init<>())
        .def_readwrite("index", &tinygltf::NormalTextureInfo::index)
        .def_readwrite("tex_coord", &tinygltf::NormalTextureInfo::texCoord)
        .def_readwrite("scale", &tinygltf::NormalTextureInfo::scale)
        .def_readwrite("extras_json_string", &tinygltf::NormalTextureInfo::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::NormalTextureInfo::extensions_json_string);

    pybind11::class_<tinygltf::OcclusionTextureInfo>(py_module, "OcclusionTextureInfo")
        .def(pybind11::init<>())
        .def_readwrite("index", &tinygltf::OcclusionTextureInfo::index)
        .def_readwrite("tex_coord", &tinygltf::OcclusionTextureInfo::texCoord)
        .def_readwrite("strength", &tinygltf::OcclusionTextureInfo::strength)
        .def_readwrite("extras_json_string", &tinygltf::OcclusionTextureInfo::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::OcclusionTextureInfo::extensions_json_string);

    pybind11::class_<tinygltf::PbrMetallicRoughness>(py_module, "PbrMetallicRoughness")
        .def(pybind11::init<>())
        .def_readwrite("base_color_factor", &tinygltf::PbrMetallicRoughness::baseColorFactor)
        .def_readwrite("base_color_texture", &tinygltf::PbrMetallicRoughness::baseColorTexture)
        .def_readwrite("metallic_factor", &tinygltf::PbrMetallicRoughness::metallicFactor)
        .def_readwrite("roughness_factor", &tinygltf::PbrMetallicRoughness::roughnessFactor)
        .def_readwrite("metallic_roughness_texture", &tinygltf::PbrMetallicRoughness::metallicRoughnessTexture)
        .def_readwrite("extras_json_string", &tinygltf::PbrMetallicRoughness::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::PbrMetallicRoughness::extensions_json_string);

    pybind11::class_<tinygltf::Material>(py_module, "Material")
        .def(pybind11::init<>())
        .def_readwrite("name", &tinygltf::Material::name)
        .def_readwrite("emissive_factor", &tinygltf::Material::emissiveFactor)
        .def_readwrite("alpha_mode", &tinygltf::Material::alphaMode)
        .def_readwrite("alpha_cutoff", &tinygltf::Material::alphaCutoff)
        .def_readwrite("double_sided", &tinygltf::Material::doubleSided)
        .def_readwrite("pbr_metallic_roughness", &tinygltf::Material::pbrMetallicRoughness)
        .def_readwrite("normal_texture", &tinygltf::Material::normalTexture)
        .def_readwrite("occlusion_texture", &tinygltf::Material::occlusionTexture)
        .def_readwrite("emissive_texture", &tinygltf::Material::emissiveTexture)
        .def_readwrite("extras_json_string", &tinygltf::Material::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Material::extensions_json_string);

    pybind11::class_<tinygltf::BufferView>(py_module, "BufferView")
        .def(pybind11::init<>())
        .def_readwrite("name", &tinygltf::BufferView::name)
        .def_readwrite("buffer", &tinygltf::BufferView::buffer)
        .def_readwrite("byte_offset", &tinygltf::BufferView::byteOffset)
        .def_readwrite("byte_length", &tinygltf::BufferView::byteLength)
        .def_readwrite("byte_stride", &tinygltf::BufferView::byteStride)
        .def_readwrite("target", &tinygltf::BufferView::target)
        .def_readwrite("extras_json_string", &tinygltf::BufferView::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::BufferView::extensions_json_string)
        .def_readwrite("draco_decoded", &tinygltf::BufferView::dracoDecoded);

    pybind11::class_<tinygltf::Accessor>(py_module, "Accessor")
        .def(pybind11::init<>())
        .def_readwrite("buffer_view", &tinygltf::Accessor::bufferView)
        .def_readwrite("name", &tinygltf::Accessor::name)
        .def_readwrite("byte_offset", &tinygltf::Accessor::byteOffset)
        .def_readwrite("normalized", &tinygltf::Accessor::normalized)
        .def_readwrite("component_type", &tinygltf::Accessor::componentType)
        .def_readwrite("count", &tinygltf::Accessor::count)
        .def_readwrite("type", &tinygltf::Accessor::type)
        .def_readwrite("extras_json_string", &tinygltf::Accessor::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Accessor::extensions_json_string)
        .def_readwrite("min_values", &tinygltf::Accessor::minValues)
        .def_readwrite("max_values", &tinygltf::Accessor::maxValues);

    pybind11::class_<tinygltf::PerspectiveCamera>(py_module, "PerspectiveCamera")
        .def(pybind11::init<>())
        .def_readwrite("aspect_ratio", &tinygltf::PerspectiveCamera::aspectRatio)
        .def_readwrite("yfov", &tinygltf::PerspectiveCamera::yfov)
        .def_readwrite("zfar", &tinygltf::PerspectiveCamera::zfar)
        .def_readwrite("znear", &tinygltf::PerspectiveCamera::znear)
        .def_readwrite("extras_json_string", &tinygltf::PerspectiveCamera::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::PerspectiveCamera::extensions_json_string);

    pybind11::class_<tinygltf::OrthographicCamera>(py_module, "OrthographicCamera")
        .def(pybind11::init<>())
        .def_readwrite("xmag", &tinygltf::OrthographicCamera::xmag)
        .def_readwrite("ymag", &tinygltf::OrthographicCamera::ymag)
        .def_readwrite("zfar", &tinygltf::OrthographicCamera::zfar)
        .def_readwrite("znear", &tinygltf::OrthographicCamera::znear)
        .def_readwrite("extras_json_string", &tinygltf::OrthographicCamera::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::OrthographicCamera::extensions_json_string);

    pybind11::class_<tinygltf::Camera>(py_module, "Camera")
        .def(pybind11::init<>())
        .def_readwrite("type", &tinygltf::Camera::type)
        .def_readwrite("name", &tinygltf::Camera::name)
        .def_readwrite("perspective", &tinygltf::Camera::perspective)
        .def_readwrite("orthographic", &tinygltf::Camera::orthographic)
        .def_readwrite("extras_json_string", &tinygltf::Camera::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Camera::extensions_json_string);

    pybind11::class_<tinygltf::Primitive>(py_module, "Primitive")
        .def(pybind11::init<>())
        .def_readwrite("attributes", &tinygltf::Primitive::attributes)
        .def_readwrite("material", &tinygltf::Primitive::material)
        .def_readwrite("indices", &tinygltf::Primitive::indices)
        .def_readwrite("mode", &tinygltf::Primitive::mode)
        .def_readwrite("targets", &tinygltf::Primitive::targets)
        .def_readwrite("extras_json_string", &tinygltf::Primitive::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Primitive::extensions_json_string);

    pybind11::class_<tinygltf::Mesh>(py_module, "Mesh")
        .def(pybind11::init<>())
        .def_readwrite("name", &tinygltf::Mesh::name)
        .def_readwrite("primitives", &tinygltf::Mesh::primitives)
        .def_readwrite("weights", &tinygltf::Mesh::weights)
        .def_readwrite("extras_json_string", &tinygltf::Mesh::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Mesh::extensions_json_string);

    pybind11::class_<tinygltf::Node>(py_module, "Node")
        .def(pybind11::init<>())
        .def_readwrite("camera", &tinygltf::Node::camera)
        .def_readwrite("name", &tinygltf::Node::name)
        .def_readwrite("skin", &tinygltf::Node::skin)
        .def_readwrite("mesh", &tinygltf::Node::mesh)
        .def_readwrite("light", &tinygltf::Node::light)
        .def_readwrite("emitter", &tinygltf::Node::emitter)
        .def_readwrite("children", &tinygltf::Node::children)
        .def_readwrite("rotation", &tinygltf::Node::rotation)
        .def_readwrite("scale", &tinygltf::Node::scale)
        .def_readwrite("translation", &tinygltf::Node::translation)
        .def_readwrite("matrix", &tinygltf::Node::matrix)
        .def_readwrite("weights", &tinygltf::Node::weights)
        .def_readwrite("extras_json_string", &tinygltf::Node::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Node::extensions_json_string);

    pybind11::class_<tinygltf::Buffer>(py_module, "Buffer")
        .def(pybind11::init<>())
        .def_readwrite("name", &tinygltf::Buffer::name)
        .def_readwrite("data", &tinygltf::Buffer::data)
        .def_readwrite("uri", &tinygltf::Buffer::uri)
        .def_readwrite("extras_json_string", &tinygltf::Buffer::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Buffer::extensions_json_string);

    pybind11::class_<tinygltf::Asset>(py_module, "Asset")
        .def(pybind11::init<>())
        .def_readwrite("version", &tinygltf::Asset::version)
        .def_readwrite("generator", &tinygltf::Asset::generator)
        .def_readwrite("min_version", &tinygltf::Asset::minVersion)
        .def_readwrite("copyright", &tinygltf::Asset::copyright)
        .def_readwrite("extras_json_string", &tinygltf::Asset::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Asset::extensions_json_string);

    pybind11::class_<tinygltf::Scene>(py_module, "Scene")
        .def(pybind11::init<>())
        .def_readwrite("name", &tinygltf::Scene::name)
        .def_readwrite("nodes", &tinygltf::Scene::nodes)
        .def_readwrite("audio_emitters", &tinygltf::Scene::audioEmitters)
        .def_readwrite("extras_json_string", &tinygltf::Scene::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Scene::extensions_json_string);

    pybind11::class_<tinygltf::SpotLight>(py_module, "SpotLight")
        .def(pybind11::init<>())
        .def_readwrite("inner_cone_angle", &tinygltf::SpotLight::innerConeAngle)
        .def_readwrite("outer_cone_angle", &tinygltf::SpotLight::outerConeAngle)
        .def_readwrite("extras_json_string", &tinygltf::SpotLight::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::SpotLight::extensions_json_string);

    pybind11::class_<tinygltf::Light>(py_module, "Light")
        .def(pybind11::init<>())
        .def_readwrite("name", &tinygltf::Light::name)
        .def_readwrite("color", &tinygltf::Light::color)
        .def_readwrite("intensity", &tinygltf::Light::intensity)
        .def_readwrite("type", &tinygltf::Light::type)
        .def_readwrite("range", &tinygltf::Light::range)
        .def_readwrite("spot", &tinygltf::Light::spot)
        .def_readwrite("extras_json_string", &tinygltf::Light::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Light::extensions_json_string);

    pybind11::class_<tinygltf::PositionalEmitter>(py_module, "PositionalEmitter")
        .def(pybind11::init<>())
        .def_readwrite("cone_inner_angle", &tinygltf::PositionalEmitter::coneInnerAngle)
        .def_readwrite("cone_outer_angle", &tinygltf::PositionalEmitter::coneOuterAngle)
        .def_readwrite("cone_outer_gain", &tinygltf::PositionalEmitter::coneOuterGain)
        .def_readwrite("max_distance", &tinygltf::PositionalEmitter::maxDistance)
        .def_readwrite("ref_distance", &tinygltf::PositionalEmitter::refDistance)
        .def_readwrite("rolloff_factor", &tinygltf::PositionalEmitter::rolloffFactor)
        .def_readwrite("extras_json_string", &tinygltf::PositionalEmitter::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::PositionalEmitter::extensions_json_string);

    pybind11::class_<tinygltf::AudioEmitter>(py_module, "AudioEmitter")
        .def(pybind11::init<>())
        .def_readwrite("name", &tinygltf::AudioEmitter::name)
        .def_readwrite("gain", &tinygltf::AudioEmitter::gain)
        .def_readwrite("loop", &tinygltf::AudioEmitter::loop)
        .def_readwrite("playing", &tinygltf::AudioEmitter::playing)
        .def_readwrite("type", &tinygltf::AudioEmitter::type)
        .def_readwrite("distance_model", &tinygltf::AudioEmitter::distanceModel)
        .def_readwrite("positional", &tinygltf::AudioEmitter::positional)
        .def_readwrite("source", &tinygltf::AudioEmitter::source)
        .def_readwrite("extras_json_string", &tinygltf::AudioEmitter::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::AudioEmitter::extensions_json_string);

    pybind11::class_<tinygltf::AudioSource>(py_module, "AudioSource")
        .def(pybind11::init<>())
        .def_readwrite("name", &tinygltf::AudioSource::name)
        .def_readwrite("uri", &tinygltf::AudioSource::uri)
        .def_readwrite("buffer_view", &tinygltf::AudioSource::bufferView)
        .def_readwrite("mime_type", &tinygltf::AudioSource::mimeType)
        .def_readwrite("extras_json_string", &tinygltf::AudioSource::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::AudioSource::extensions_json_string);

    pybind11::class_<tinygltf::Model>(py_module, "Model")
        .def(pybind11::init<>())
        .def_readwrite("accessors", &tinygltf::Model::accessors)
        .def_readwrite("animations", &tinygltf::Model::animations)
        .def_readwrite("buffers", &tinygltf::Model::buffers)
        .def_readwrite("bufferViews", &tinygltf::Model::bufferViews)
        .def_readwrite("materials", &tinygltf::Model::materials)
        .def_readwrite("meshes", &tinygltf::Model::meshes)
        .def_readwrite("nodes", &tinygltf::Model::nodes)
        .def_readwrite("textures", &tinygltf::Model::textures)
        .def_readwrite("images", &tinygltf::Model::images)
        .def_readwrite("skins", &tinygltf::Model::skins)
        .def_readwrite("samplers", &tinygltf::Model::samplers)
        .def_readwrite("cameras", &tinygltf::Model::cameras)
        .def_readwrite("scenes", &tinygltf::Model::scenes)
        .def_readwrite("lights", &tinygltf::Model::lights)
        .def_readwrite("audio_emitters", &tinygltf::Model::audioEmitters)
        .def_readwrite("audio_sources", &tinygltf::Model::audioSources)
        .def_readwrite("default_scene", &tinygltf::Model::defaultScene)
        .def_readwrite("extensions_used", &tinygltf::Model::extensionsUsed)
        .def_readwrite("extensions_required", &tinygltf::Model::extensionsRequired)
        .def_readwrite("asset", &tinygltf::Model::asset)
        .def_readwrite("extras_json_string", &tinygltf::Model::extras_json_string)
        .def_readwrite("extensions_json_string", &tinygltf::Model::extensions_json_string);

    py_module.attr("TINYGLTF_MODE_POINTS") = TINYGLTF_MODE_POINTS;
    py_module.attr("TINYGLTF_MODE_LINE") = TINYGLTF_MODE_LINE;
    py_module.attr("TINYGLTF_MODE_LINE_LOOP") = TINYGLTF_MODE_LINE_LOOP;
    py_module.attr("TINYGLTF_MODE_LINE_STRIP") = TINYGLTF_MODE_LINE_STRIP;
    py_module.attr("TINYGLTF_MODE_TRIANGLES") = TINYGLTF_MODE_TRIANGLES;
    py_module.attr("TINYGLTF_MODE_TRIANGLE_STRIP") = TINYGLTF_MODE_TRIANGLE_STRIP;
    py_module.attr("TINYGLTF_MODE_TRIANGLE_FAN") = TINYGLTF_MODE_TRIANGLE_FAN;

    py_module.attr("TINYGLTF_COMPONENT_TYPE_BYTE") = TINYGLTF_COMPONENT_TYPE_BYTE;
    py_module.attr("TINYGLTF_COMPONENT_TYPE_UNSIGNED_BYTE") = TINYGLTF_COMPONENT_TYPE_UNSIGNED_BYTE;
    py_module.attr("TINYGLTF_COMPONENT_TYPE_SHORT") = TINYGLTF_COMPONENT_TYPE_SHORT;
    py_module.attr("TINYGLTF_COMPONENT_TYPE_UNSIGNED_SHORT") = TINYGLTF_COMPONENT_TYPE_UNSIGNED_SHORT;
    py_module.attr("TINYGLTF_COMPONENT_TYPE_INT") = TINYGLTF_COMPONENT_TYPE_INT;
    py_module.attr("TINYGLTF_COMPONENT_TYPE_UNSIGNED_INT") = TINYGLTF_COMPONENT_TYPE_UNSIGNED_INT;
    py_module.attr("TINYGLTF_COMPONENT_TYPE_FLOAT") = TINYGLTF_COMPONENT_TYPE_FLOAT;
    py_module.attr("TINYGLTF_COMPONENT_TYPE_DOUBLE") = TINYGLTF_COMPONENT_TYPE_DOUBLE;

    py_module.attr("TINYGLTF_TEXTURE_FILTER_NEAREST") = TINYGLTF_TEXTURE_FILTER_NEAREST;
    py_module.attr("TINYGLTF_TEXTURE_FILTER_LINEAR") = TINYGLTF_TEXTURE_FILTER_LINEAR;
    py_module.attr("TINYGLTF_TEXTURE_FILTER_NEAREST_MIPMAP_NEAREST") = TINYGLTF_TEXTURE_FILTER_NEAREST_MIPMAP_NEAREST;
    py_module.attr("TINYGLTF_TEXTURE_FILTER_LINEAR_MIPMAP_NEAREST") = TINYGLTF_TEXTURE_FILTER_LINEAR_MIPMAP_NEAREST;
    py_module.attr("TINYGLTF_TEXTURE_FILTER_NEAREST_MIPMAP_LINEAR") = TINYGLTF_TEXTURE_FILTER_NEAREST_MIPMAP_LINEAR;
    py_module.attr("TINYGLTF_TEXTURE_FILTER_LINEAR_MIPMAP_LINEAR") = TINYGLTF_TEXTURE_FILTER_LINEAR_MIPMAP_LINEAR;

    py_module.attr("TINYGLTF_TEXTURE_WRAP_REPEAT") = TINYGLTF_TEXTURE_WRAP_REPEAT;
    py_module.attr("TINYGLTF_TEXTURE_WRAP_CLAMP_TO_EDGE") = TINYGLTF_TEXTURE_WRAP_CLAMP_TO_EDGE;
    py_module.attr("TINYGLTF_TEXTURE_WRAP_MIRRORED_REPEAT") = TINYGLTF_TEXTURE_WRAP_MIRRORED_REPEAT;

    py_module.attr("TINYGLTF_TYPE_VEC2") = TINYGLTF_TYPE_VEC2;
    py_module.attr("TINYGLTF_TYPE_VEC3") = TINYGLTF_TYPE_VEC3;
    py_module.attr("TINYGLTF_TYPE_VEC4") = TINYGLTF_TYPE_VEC4;
    py_module.attr("TINYGLTF_TYPE_MAT2") = TINYGLTF_TYPE_MAT2;
    py_module.attr("TINYGLTF_TYPE_MAT3") = TINYGLTF_TYPE_MAT3;
    py_module.attr("TINYGLTF_TYPE_MAT4") = TINYGLTF_TYPE_MAT4;
    py_module.attr("TINYGLTF_TYPE_SCALAR") = TINYGLTF_TYPE_SCALAR;
    py_module.attr("TINYGLTF_TYPE_VECTOR") = TINYGLTF_TYPE_VECTOR;
    py_module.attr("TINYGLTF_TYPE_MATRIX") = TINYGLTF_TYPE_MATRIX;

    py_module.attr("TINYGLTF_IMAGE_FORMAT_JPEG") = TINYGLTF_IMAGE_FORMAT_JPEG;
    py_module.attr("TINYGLTF_IMAGE_FORMAT_PNG") = TINYGLTF_IMAGE_FORMAT_PNG;
    py_module.attr("TINYGLTF_IMAGE_FORMAT_BMP") = TINYGLTF_IMAGE_FORMAT_BMP;
    py_module.attr("TINYGLTF_IMAGE_FORMAT_GIF") = TINYGLTF_IMAGE_FORMAT_GIF;

    py_module.attr("TINYGLTF_TEXTURE_FORMAT_ALPHA") = TINYGLTF_TEXTURE_FORMAT_ALPHA;
    py_module.attr("TINYGLTF_TEXTURE_FORMAT_RGB") = TINYGLTF_TEXTURE_FORMAT_RGB;
    py_module.attr("TINYGLTF_TEXTURE_FORMAT_RGBA") = TINYGLTF_TEXTURE_FORMAT_RGBA;
    py_module.attr("TINYGLTF_TEXTURE_FORMAT_LUMINANCE") = TINYGLTF_TEXTURE_FORMAT_LUMINANCE;
    py_module.attr("TINYGLTF_TEXTURE_FORMAT_LUMINANCE_ALPHA") = TINYGLTF_TEXTURE_FORMAT_LUMINANCE_ALPHA;

    py_module.attr("TINYGLTF_TEXTURE_TARGET_TEXTURE2D") = TINYGLTF_TEXTURE_TARGET_TEXTURE2D;
    py_module.attr("TINYGLTF_TEXTURE_TYPE_UNSIGNED_BYTE") = TINYGLTF_TEXTURE_TYPE_UNSIGNED_BYTE;

    py_module.attr("TINYGLTF_TARGET_ARRAY_BUFFER") = TINYGLTF_TARGET_ARRAY_BUFFER;
    py_module.attr("TINYGLTF_TARGET_ELEMENT_ARRAY_BUFFER") = TINYGLTF_TARGET_ELEMENT_ARRAY_BUFFER;

    py_module.attr("TINYGLTF_SHADER_TYPE_VERTEX_SHADER") = TINYGLTF_SHADER_TYPE_VERTEX_SHADER;
    py_module.attr("TINYGLTF_SHADER_TYPE_FRAGMENT_SHADER") = TINYGLTF_SHADER_TYPE_FRAGMENT_SHADER;

    py_module.attr("TINYGLTF_DOUBLE_EPS") = TINYGLTF_DOUBLE_EPS;

    py_module.def("get_component_size_in_bytes", &tinygltf::GetComponentSizeInBytes);
    py_module.def("get_num_components_in_type", &tinygltf::GetNumComponentsInType);

    py_module.def("load_gltf", &load_gltf);
    py_module.def("save_gltf", &save_gltf);
}
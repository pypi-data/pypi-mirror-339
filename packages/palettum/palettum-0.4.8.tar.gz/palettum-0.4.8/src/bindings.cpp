#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "config.h"
#include "palettum.h"

namespace py = pybind11;

PYBIND11_MODULE(palettum, m)
{
    m.doc() = "Core functionality for the Palettum project.";

    m.def(
        "palettify",
        [](Image &img, Config &config) {
            palettum::palettify(img, config);
        },
        py::arg("image"), py::arg("config"));

    m.def(
        "palettify",
        [](GIF &gif, Config &config) {
            palettum::palettify(gif, config);
        },
        py::arg("gif"), py::arg("config"));

    m.def("validate", &palettum::validate, py::arg("image"), py::arg("config"));

    py::enum_<Formula>(m, "Formula")
        .value("CIE76", Formula::CIE76)
        .value("CIE94", Formula::CIE94)
        .value("CIEDE2000", Formula::CIEDE2000)
        .export_values();

    py::enum_<Architecture>(m, "Architecture")
        .value("SCALAR", Architecture::SCALAR)
        .value("NEON", Architecture::NEON)
        .value("AVX2", Architecture::AVX2)
        .export_values();

    py::enum_<Mapping>(m, "Mapping")
        .value("PALETTIZED", Mapping::PALETTIZED)
        .value("SMOOTHED", Mapping::SMOOTHED)
        .value("SMOOTHED_PALETTIZED", Mapping::SMOOTHED_PALETTIZED)
        .export_values();

    py::enum_<WeightingKernelType>(m, "WeightingKernelType")
        .value("GAUSSIAN", WeightingKernelType::GAUSSIAN)
        .value("INVERSE_DISTANCE_POWER",
               WeightingKernelType::INVERSE_DISTANCE_POWER)
        .export_values();

    py::class_<Config>(m, "Config")
        .def(py::init<>())
        .def_readwrite("palette", &Config::palette)
        .def_readwrite("transparencyThreshold", &Config::transparencyThreshold)
        .def_readwrite("formula", &Config::palettized_formula)
        .def_readwrite("architecture", &Config::architecture)
        .def_readwrite("quantLevel", &Config::quantLevel)
        .def_readwrite("mapping", &Config::mapping)
        .def_readwrite("anisotropic_kernel", &Config::anisotropic_kernel)
        .def_readwrite("anisotropic_labScales", &Config::anisotropic_labScales)
        .def_readwrite("anisotropic_shapeParameter",
                       &Config::anisotropic_shapeParameter)
        .def_readwrite("anisotropic_powerParameter",
                       &Config::anisotropic_powerParameter);

    py::class_<RGB>(m, "RGB")
        .def(py::init<uint8_t, uint8_t, uint8_t>())
        .def(py::init<std::initializer_list<uint8_t>>())
        .def_readwrite("r", &RGB::r)
        .def_readwrite("g", &RGB::g)
        .def_readwrite("b", &RGB::b)
        .def("toLab", &RGB::toLab)
        .def("__eq__", &RGB::operator==)
        .def("__ne__", &RGB::operator!=)
        .def("__repr__", [](const RGB &rgb) {
            return "RGB(" + std::to_string(rgb.r) + ", " +
                   std::to_string(rgb.g) + ", " + std::to_string(rgb.b) + ")";
        });

    py::class_<RGBA>(m, "RGBA")
        .def(py::init<uint8_t, uint8_t, uint8_t, uint8_t>(), py::arg("r") = 0,
             py::arg("g") = 0, py::arg("b") = 0, py::arg("a") = 255)
        .def_readwrite("r", &RGBA::r)
        .def_readwrite("g", &RGBA::g)
        .def_readwrite("b", &RGBA::b)
        .def_readwrite("a", &RGBA::a);

    py::class_<Lab>(m, "Lab")
        .def(py::init<lab_float_t, lab_float_t, lab_float_t>(),
             py::arg("L") = 0, py::arg("a") = 0, py::arg("b") = 0)
        .def("L", &Lab::L)
        .def("a", &Lab::a)
        .def("b", &Lab::b)
        .def("toRGB", &Lab::toRGB)
        .def("__repr__", [](const Lab &lab) {
            return "Lab(" + std::to_string((float)lab.L()) + ", " +
                   std::to_string((float)lab.a()) + ", " +
                   std::to_string((float)lab.b()) + ")";
        });

    py::class_<Image>(m, "Image")
        .def(py::init<>())
        .def(py::init<const std::string &>())
        .def(py::init<const char *>())
        .def(py::init<int, int>())
        .def(py::init<int, int, bool>())
        .def(py::init([](py::buffer buffer) {
            py::buffer_info info = buffer.request();
            if (info.ndim != 1)
            {
                throw std::runtime_error("Buffer must be 1-dimensional");
            }
            return new Image(static_cast<const unsigned char *>(info.ptr),
                             static_cast<int>(info.size));
        }))
        .def("write", py::overload_cast<>(&Image::write, py::const_))
        .def("write",
             py::overload_cast<const std::string &>(&Image::write, py::const_))
        .def("write",
             py::overload_cast<const char *>(&Image::write, py::const_))

        .def("setPalette", &Image::setPalette)

        .def("resize", &Image::resize)
        .def("get", &Image::get)
        .def("set", py::overload_cast<int, int, const RGBA &>(&Image::set))
        .def("width", &Image::width)
        .def("height", &Image::height)
        .def("channels", &Image::channels)
        .def("hasAlpha", &Image::hasAlpha)
        .def("data",
             [](const Image &img) {
                 return py::array_t<uint8_t>(
                     {img.height(), img.width(), img.channels()},  // shape
                     {img.width() * img.channels(), img.channels(),
                      1},  // strides
                     img.data(),
                     py::cast(img)  // keep parent alive
                 );
             })
        .def("__eq__", &Image::operator==)
        .def("__ne__", &Image::operator!=)
        .def("__sub__", &Image::operator-);

    py::class_<GIF>(m, "GIF")
        .def(py::init<const std::string &>())
        .def(py::init<const char *>())
        .def(py::init<int, int>())
        .def(py::init([](py::buffer buffer) {
            py::buffer_info info = buffer.request();
            if (info.ndim != 1)
            {
                throw std::runtime_error("Buffer must be 1-dimensional");
            }
            return new GIF(static_cast<const unsigned char *>(info.ptr),
                           static_cast<int>(info.size));
        }))
        .def("write",
             py::overload_cast<const std::string &>(&GIF::write, py::const_))
        .def("write", py::overload_cast<const char *>(&GIF::write, py::const_))
        .def("write", py::overload_cast<>(&GIF::write, py::const_))
        .def("resize", &GIF::resize)
        .def("frameCount", &GIF::frameCount)
        .def("width", &GIF::width)
        .def("height", &GIF::height)
        .def("addFrame", &GIF::addFrame, py::arg("image"),
             py::arg("delay_cs") = 10)
        .def("setPixel",
             py::overload_cast<size_t, int, int, const RGBA &>(&GIF::setPixel))
        .def("setPixel",
             py::overload_cast<size_t, int, int, const RGB &>(&GIF::setPixel))
        .def("setPalette", &GIF::setPalette)
        .def("getFrame", py::overload_cast<size_t>(&GIF::getFrame, py::const_));
}

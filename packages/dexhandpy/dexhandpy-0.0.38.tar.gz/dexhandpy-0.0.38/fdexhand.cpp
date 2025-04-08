#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include "./fdexhand/include/dexhand.h"
namespace py = pybind11;
using namespace FdHand;

PYBIND11_MODULE(fdexhand, m) {
    py::enum_<Ret>(m, "Ret")
        .value("SUCCESS", Ret::SUCCESS)
        .value("FAIL", Ret::FAIL)
        .value("TIMEOUT", Ret::TIMEOUT)
        .export_values();

    py::class_<DexHand>(m, "DexHand")
        .def(py::init<>())
        // .def("__del__", &DexHand::~DexHand)
        .def("init", &DexHand::init, py::arg("flg")=0)
        .def("get_ip_list", &DexHand::get_ip_list)
        .def("get_name", &DexHand::get_name)
        .def("get_type", &DexHand::get_type)
        .def("get_driver_ver", &DexHand::get_driver_ver)
        .def("get_hardware_ver", &DexHand::get_hardware_ver)
        .def("get_errorcode", &DexHand::get_errorcode)
        .def("set_pos", &DexHand::set_pos)
        .def("get_pos", &DexHand::get_pos)
        .def("clear_errorcode", &DexHand::clear_errorcode)
        .def("get_ts_matrix", &DexHand::get_ts_matrix)
        .def("fast_set_pos", &DexHand::fast_set_pos)
        .def("set_hand_config", &DexHand::set_hand_config)
        .def("get_hand_config", &DexHand::get_hand_config)
        .def("reboot", (Ret (DexHand::*)()) & DexHand::reboot)
        .def("reboot", (Ret (DexHand::*)(std::string)) & DexHand::reboot)
        .def("enable", (Ret (DexHand::*)()) & DexHand::enable)
        .def("enable", (Ret (DexHand::*)(std::string)) & DexHand::enable)
        .def("disable", (Ret (DexHand::*)()) & DexHand::disable)
        .def("disable", (Ret (DexHand::*)(std::string)) & DexHand::disable)
        .def("calibration", (Ret (DexHand::*)()) & DexHand::calibration)
        .def("calibration", (Ret (DexHand::*)(std::string)) & DexHand::calibration)
        .def("get_pvc", &DexHand::get_pvc)
        ;
}

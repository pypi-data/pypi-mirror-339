#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "heatindex.h"

namespace py = pybind11;

PYBIND11_MODULE(heatindex, m) {
    m.def("heatindex", py::vectorize(heatindex),
          "The function takes air temperature (K) and relative humidity (0-1), and returns the heat index (K).",
          py::arg("Ta"), py::arg("RH"));

    m.attr("__version__") = "0.0.1";
    
    m.doc() = R"pbdoc(
        This packages currently provides a single function, `heatindex`, which is an 
        implementation of the simpler and faster heat index introduced by Lu et al. 
        (2025). This simpler and faster implementation matches the values of the heat
        index from Steadman (1979) and Lu and Romps (2022) for air temperatures above 
        300 K (27 C, 80F) and with only minor differences at lower temperatures.
        
        The `heatindex` function takes two arguments: air temperature (`Ta`) in Kelvin 
        and relative humidity (`RH`) on a scale from 0 to 1, and returns the heat index 
        in Kelvin. Note that the relative humidity is defined with respect to saturation 
        over liquid water for air temperatures over 273.16 K and with respect to 
        saturation over ice for air temperatures lower than 273.16 K.
        
        The function is numpy vectorized: it accepts scalars and arrays as inputs, 
        and returns an output of the same shape. When both arguments are arrays, 
        they must be of identical shape. If one argument is an array and the other 
        a scalar, NumPy broadcasting applies.
        
        For specific examples, please refer to
        https://heatindex.org/docs/examples

        To cite package ‘heatindex’ in publications use:
        Lu, Y.-C. and Romps, D.M., 2025. heatindex: Tools for Calculating Heat Stress.
        Python package version 0.0.1, <https://heatindex.org>.
        
        A BibTeX entry for LaTeX users is
        @manual{,
        title = {heatindex: Tools for Calculating Heat Stress},
        author = {Yi-Chuan Lu and David M. Romps},
        year = {2025},
        note = {Python package version 0.0.1},
        url = {https://heatindex.org},
        }
    )pbdoc";
}

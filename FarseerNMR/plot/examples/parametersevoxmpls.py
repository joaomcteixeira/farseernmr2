"""
This module generates examples for Parameter Evolution Plots.

Use this module to create plots that exploit plotting templates features.
"""
# Copyright © 2017-2019 Farseer-NMR
#
# @Original Article: http://bit.ly/farseerjbnmr
# @ResearchGate https://goo.gl/z8dPJU
# @Twitter https://twitter.com/farseer_nmr
# @GitHub: http://bit.ly/farseer-nmr
# @Mailist: http://bit.ly/fs_maillist
#
# This file is part of the Farseer-NMR project.
#
# Farseer-NMR is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Farseer-NMR is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Farseer-NMR. If not, see <http://www.gnu.org/licenses/>.
#
# For full list of author contributors visit:
#    https://github.com/Farseer-NMR/FarSeer-NMR/wiki/Citing
#
# Contributors to this file:
#    - João M.C. Teixeira (https://github.com/joaomcteixeira)
import string
import itertools as it
import numpy as np

from FarseerNMR.plot import (
    parameterevolutionplot,
    )

list_of_templates = [
    parameterevolutionplot,
    ]

list_of_names = [
    "parameterevolutionplot",
    ]

ext = "pdf"

c = {
    "figure_dpi": 200,
    }


def make_data(shape):
    
    values = np.linspace(0, 0.2, shape[0] * shape[1]).reshape(shape)
    
    al = it.cycle(string.ascii_letters)
    
    suptitles = [next(al) for i in range(shape[0])]
    
    peak_status = None
    fitting = None
    fitting_info = None
        
    return (
        values,
        suptitles,
        peak_status,
        fitting,
        fitting_info,
        )


def example1(plot, name):
    
    shape = (50, 10)  # 50 residues, 10 data points
    name = f"{name}_1.{ext}"
    
    values, suptitles, peak_status, fitting, \
        fitting_info, = make_data(shape)
    
    plot(
        values,
        suptitles=suptitles,
        peak_status=peak_status,
        fitting=fitting,
        fitting_info=fitting_info,
        header="1",
        figure_path=name,
        **c
        )
    
    return


def run():
    
    for module, name in zip(list_of_templates, list_of_names):
        
        for example in list_of_examples:
            
            example(module.plot, name)
            
    return


list_of_examples = [
    example1,
    ]


if __name__ == "__main__":
    
    run()

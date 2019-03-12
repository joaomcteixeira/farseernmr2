"""
This module generates examples for Bar Plots.

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

import numpy as np

from FarseerNMR.plot import (
    barplotcompacted,
    barplotextended,
    barplotextendedvertical,
    )

list_of_templates = [
    barplotcompacted,
    barplotextended,
    barplotextendedvertical,
    ]

list_of_names = [
    "barplotcompacted",
    "barplotextended",
    "barplotextendedvertical",
    ]

ext = "png"

c = {
    "bar_width": 1.0,
    "mark_user_details_flag": True,
    "color_user_details_flag": True,
    "user_marks_dict": {
        "yell": "y"
        },
    "user_bar_colors_dict": {
        "yell": "yellow"
        },
    "figure_dpi": 200,
    }


def make_data(shape):
    
    values = np.full(shape, 0.2)
    labels = np.arange(1, shape[1] + 1).astype(str)
    details = np.full(shape, "none")
    suptitles = [c for c in "ABCDEFGHIJKLMNOPQRSTUVXYZ"[:shape[0]]]
    letter_code = None
    peak_status = None
    tag_position = np.empty(shape, dtype=str)
    #tag_position[:, 1] = "*"
    theo_pre = np.full(shape, 0.25)
        
    return (
        values,
        labels,
        suptitles,
        letter_code,
        peak_status,
        details,
        tag_position,
        theo_pre,
        )

def example1(plot, name):
    
    shape = (7, 8)
    name = f"{name}_1.{ext}"
    
    values, labels, suptitles, letter_code, \
    peak_status, details, tag_position, theo_pre = make_data(shape)
    
    for i in range(shape[0]):
        values[i,i] = 0.05 * i
        details[i, i] = "yell"
    
    plot(
        values,
        labels,
        details=details,
        header="1",
        figure_path=name,
        **c
        )
    
    return 

def example2(plot, name):
    
    shape = (3, 100)
    name = f"{name}_2.{ext}"
    
    values, labels, suptitles, letter_code, \
    peak_status, details, tag_position, theo_pre = make_data(shape)
    
    values[1, 45:56] = 0.0
    tag_position[:, 49] = "*" # residue 50!!
    
    plot(
        values,
        labels,
        details=details,
        tag_position=tag_position,
        theo_pre=theo_pre,
        header="2",
        plot_theoretical_pre=True,
        figure_path=name,
        **c)
    
    return

def example3(plot, name):
    
    shape = (3, 200)
    name = f"{name}_3.{ext}"
    
    values, labels, suptitles, letter_code, \
    peak_status, details, tag_position, theo_pre = make_data(shape)
    
    values[1, 100:200] = 0.0
    tag_position[:, 149] = "*" # residue 150 !!
    
    plot(
        values,
        labels,
        details=details,
        tag_position=tag_position,
        theo_pre=theo_pre,
        header="3",
        figure_path=name,
        plot_theoretical_pre=True,
        **c)
    
    return

def example4(plot, name):
    
    shape = (3, 1000)
    name = f"{name}_4.{ext}"
    
    values, labels, suptitles, letter_code, \
    peak_status, details, tag_position, theo_pre = make_data(shape)
    
    details[0, 100:200] = "yell"
    details[1, 200:300] = "yell"
    details[2, 600:700] = "yell"
    
    plot(
        values,
        labels,
        suptitles=suptitles,
        details=details,
        header="4",
        figure_path=name,
        **c)
    
    return

def example5(plot, name):
    
    shape = (3, 357)
    name = f"{name}_5.{ext}"
    
    values, labels, suptitles, letter_code, \
    peak_status, details, tag_position, theo_pre = make_data(shape)
    
    details[0, 0:50] = "yell"
    details[1, 99:150] = "yell"
        
    plot(
        values,
        labels,
        suptitles=suptitles,
        details=details,
        header="5",
        figure_path=name,
        **{**c, **{"bar_width": 0.5}}
        )
    
    return

def run():
    
    for module, name in zip(list_of_templates, list_of_names):
        
        for example in list_of_examples:
            
            example(module.plot, name)
            
    return

list_of_examples = [
    example1,
    example2,
    example3,
    example4,
    example5,
    ]

if __name__ == "__main__":
    
    run()

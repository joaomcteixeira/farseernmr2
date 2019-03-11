from math import ceil

from matplotlib import pyplot as plt

from FarseerNMR import logger
from FarseerNMR.core import (core, wet)

log = logger.get_log(__name__)


def hex_to_RGB(hexx):
    """    
    Converts HEX color to RGB.
    
    "#FFFFFF" -> [255,255,255]
    """
    # This function was taken from:
    # Copyright 2017 Ben Southgate
    # https://github.com/bsouthga/blog
    
    # The MIT License (MIT)
    
    # Permission is hereby granted, free of charge,
    # to any person obtaining a copy of this software and associated
    # documentation files (the "Software"), to deal in the Software
    # without restriction, including without limitation the rights to
    # use, copy, modify, merge, publish, distribute, sublicense,
    # and/or sell copies of the Software, and to permit persons to
    # whom the Software is furnished to do so, subject to the
    # following conditions:

    # The above copyright notice and this permission notice shall be
    # included in all copies or substantial portions of the Software.

    # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    # EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    # OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    # NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    # HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    # WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    # FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    # OTHER DEALINGS IN THE SOFTWARE.
    
    # IF STATEMENT not part of the original function,
    # added for the Farseer-NMR Project.
    if not(hexx.startswith("#") and len(hexx) == 7):
        msg = "The input colour is not in HEX format."
        wet = wet.generate("ERROR", msg, 27)
        log.info(wet)
        sys.exit(core.abort_message)
    # Pass 16 to the integer function for change of base
    return [int(hexx[i:i + 2], 16) for i in range(1, 6, 2)]


def RGB_to_hex(RGB):
    """
    Converts RGB color to HEX.
    
    [255,255,255] -> "#FFFFFF"
    """
    # This function was taken from:
    # Copyright 2017 Ben Southgate
    # https://github.com/bsouthga/blog
    
    # The MIT License (MIT)
    
    # Permission is hereby granted, free of charge,
    # to any person obtaining a copy of this software and associated
    # documentation files (the "Software"), to deal in the Software
    # without restriction, including without limitation the rights to
    # use, copy, modify, merge, publish, distribute, sublicense,
    # and/or sell copies of the Software, and to permit persons to
    # whom the Software is furnished to do so, subject to the
    # following conditions:

    # The above copyright notice and this permission notice shall be
    # included in all copies or substantial portions of the Software.

    # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    # EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    # OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    # NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    # HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    # WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    # FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    # OTHER DEALINGS IN THE SOFTWARE.
    
    # Components need to be integers for hex to make sense
    RGB = [int(x) for x in RGB]
    hexx = "#" + "".join(
        ["0{0:x}".format(v) if v < 16 else "{0:x}".format(v)
            for v in RGB]
        )
    return hexx


def color_dict(gradient):
    """
    Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on.
    """
    # This function was taken from:
    # Copyright 2017 Ben Southgate
    # https://github.com/bsouthga/blog
    
    # The MIT License (MIT)
    
    # Permission is hereby granted, free of charge,
    # to any person obtaining a copy of this software and associated
    # documentation files (the "Software"), to deal in the Software
    # without restriction, including without limitation the rights to
    # use, copy, modify, merge, publish, distribute, sublicense,
    # and/or sell copies of the Software, and to permit persons to
    # whom the Software is furnished to do so, subject to the
    # following conditions:

    # The above copyright notice and this permission notice shall be
    # included in all copies or substantial portions of the Software.

    # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    # EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    # OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    # NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    # HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    # WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    # FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    # OTHER DEALINGS IN THE SOFTWARE.
    d = {
        "hex": [RGB_to_hex(RGB) for RGB in gradient],
        "r": [RGB[0] for RGB in gradient],
        "g": [RGB[1] for RGB in gradient],
        "b": [RGB[2] for RGB in gradient]
        }
    
    return d


def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
    """
    Returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF")
    
    Parameters
    ----------
    start_hex : :obj:`str`
        The starting HEX color color.
    
    finish_hex : :obj:`str`
        The ending HEX color color.
        Defaults to #FFFFFF.
    
    n : :obj:`int`
        The number of steps.
        Defaults to 10.
    """
    # Starting and ending colors in RGB form
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    # Initilize a list of the output colors with the starting color
    RGB_list = [s]
    # Calcuate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [
            int(s[j] + (float(t) / (n - 1)) * (f[j] - s[j]))
            for j in range(3)
            ]
        # Add it to our list of output colors
        RGB_list.append(curr_vector)
    
    return color_dict(RGB_list)


def calc_num_rows(num_subplots, cols_page):
    """
    Calculates the total number of rows.
    
    Calculates the number of subplot rows to be drawn in the figure
    based on the total number of subplots to be drawn
    and the number os columns per page.
    
    Parameters
    ----------
    num_subplots : :obj:`int`
        The total number of subplots
    
    cols_page : :obj:`int`
        The desired number os subplot columns per figure's page.
    
    Returns
    -------
    float
        The calculated number.
    """
    
    return ceil(num_subplots / cols_page) + 1


def calc_real_fig_height(rows_page, numrows, fig_hgt):
    """
    Calculates real figure height based on the height per page and
    total number of subplots rows.
    
    Paramers
    --------
    rows_page : :obj:`int`
        Desired number of rows per page.
        
    numrows : :obj:`int`
        Total number of subplot rows based on number of columns.
        Can be calculated from .calc_num_rows()
        
    fig_hgt : :obj:`float`
        Height of figure's page.
    
    Returns
    -------
    float
        Value in Inches of the final figure height.
    """
    
    return (fig_hgt / rows_page) * numrows


def draw_figure(
        num_subplots,
        rows_page,
        cols_page,
        fig_height,
        fig_width,
        ):
    """
    Draws the matplotlib figure architecture.
    
    Defines subplot grid distrubitions based on the data to plot,
    desired rows and columns per page, figure height and width.
    
    Parameters
    ----------
    num_subplots : :obj:`int`
        The total number of subplots
    
    rows_page: :obj:`int`
        The desired number os subplot rows per figure's page.
    
    cols_page : :obj:`int`
        The desired number os subplot columns per figure's page.
    
    fig_height : :obj:`float`
        Height of the figure's page.
    
    fig_width : :obj:`float`
        Width of the figure's page.
    
    Returns
    -------
    tuple
        (Figure, Axes) matplotlib.pyplot.figure and
        matplotlib.pyplot.axes objects.
    """
    
    numrows = calc_num_rows(
        num_subplots,
        cols_page,
        )
    
    real_fig_height = calc_real_fig_height(
        rows_page,
        numrows,
        fig_height,
        )
    
    # http://stackoverflow.com/questions/17210646/python-subplot-within-a-loop-first-panel-appears-in-wrong-position
    figure, axs = plt.subplots(
        nrows=numrows,
        ncols=cols_page,
        figsize=(fig_width, real_fig_height),
        )
    
    axs = axs.ravel()
    
    plt.tight_layout(
        rect=[0.01, 0.01, 0.995, 0.995]
        )
    
    log.debug("Figure drawn: OKAY")
    
    return figure, axs


def adjust_subplots(figure, hspace, wspace):
    """
    Ajudst subplots.
    
    Adjusts subplots according to matplotlib.pyplot.subplots_adjust
    
    Parameters
    ----------
    figure : :obj:`matplotlib.pyplot.figure`
    
    hspace : :obj:`float`
        from matplotlib, the amount of height reserved for space
            between subplots, expressed as a fraction of the average
            axis height
    
    wspace : :obj:`float`
        from matplotlib, the amount of width reserved for space
            between subplots, expressed as a fraction of the average
            axis width
    """
    
    figure.subplots_adjust(
        hspace=hspace,
        wspace=wspace,
        )
    
    return


def clean_subplots(axes, num_subplots):
    """
    Removes unsed subplots from figure.
    
    <axes> length is compared to <num_subplots> and elements
    in <axes> that have not been used are removed from figure.
    
    Parameters
    ----------
    axes : :obj:`matplotlib.axes.Axes`
    
    num_subplots : :obj:`int`
        The number of subplots that have been draw in the Figure.
    """
    
    len_axs = len(axes)
    
    log.debug(f"Length Axes: {len_axs}")
    
    for i in range(num_subplots, len_axs):
        axes[i].remove()
    
    return


def save_figure(
        figure,
        file_path,
        header="",
        header_fs=5,
        dpi=300,
        ):
    """
    Saves figure to path.
    
    Parameters
    ----------
    figure : :obj:`matplotlib.pyplot.figure`
    
    file_path : :obj:`str`
        File name path of the output file.
        
        For example:
        /home/user/where/ever/i/want/figure.pdf
        
        file extensions can be such as accepted by fname in:
        
        https://matplotlib.org/api/_as_gen/matplotlib.pyplot.savefig.html
    
    header : :obj:`str`
        Multi-line string with additional human-readable notes.
        Header will be written in the output figure file in a dedicated
        blank space.
    
    header_fs : :obj:`int`
        The header fontsize.
    
    dpi : :obj:`int`
        The resolution in dots per inch.
        
        The Figure resolution in dpi. Deppends on the file extension.
        
        Additional help:
        https://matplotlib.org/api/_as_gen/matplotlib.pyplot.savefig.html
    """
    
    figure.text(
        0.01,
        0.01,
        header,
        fontsize=header_fs,
        )
    
    figure.savefig(file_path, dpi=dpi)
    
    log.info(f"**Saved plot figure** {file_path}\n")
    
    return

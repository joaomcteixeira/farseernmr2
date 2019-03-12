"""
Parameter Evolution Plot.

The Parameter Evolution Plot consists of a grid of subplots where,
in each subplot is represented the evolution of a given parameter
along the titration series for a specific residue.

The final figure contains one subplot per residue identified in the
input data.

Style configurations can be tweaked using the specific parameters
in .plot() function.

The configuration dictionary provided with this module can be used
to tweak the plotting style and details - see :func:`~get_config`.

.. note::

    The implementation of plot style ``kwargs`` as a dictionary apart from
    the :func:`~plot` parameters is part of the conscious design of the
    Farseer-NMR plotting modules.
"""
import numpy as np
import json

from matplotlib import pyplot as plt

from FarseerNMR import logger
from FarseerNMR.plot.base import (
    plottingbase,
    plotvalidators,
    )
from FarseerNMR.plot.examples import parametersevoxmpls

log = logger.get_log(__name__)

_default_config = {
        
    "cols_page": 5,
    "rows_page": 8,
    
    "y_lims": (0, 0.3),
    "hspace": 0.5,
    "wspace": 0.5,
    
    "subtitle_fn": "Arial",
    "subtitle_fs": 8,
    "subtitle_pad": 0.98,
    "subtitle_weight": "normal",
    
    "x_label_fn": "Arial",
    "x_label_fs": 6,
    "x_label_pad": 2,
    "x_label_weight": "normal",
    "x_label": "ligand ratio",
    
    "y_label_fn": "Arial",
    "y_label_fs": 6,
    "y_label_pad": 2,
    "y_label_weight": "normal",
    "y_label": "CSPs",
    
    "set_x_values": False,
    "titration_x_values": [],
    "x_ticks_fn": "Arial",
    "x_ticks_fs": 5,
    "x_ticks_pad": 1,
    "x_ticks_weight": "normal",
    "x_ticks_rot": 30,
    "x_ticks_len": 2,
    "x_ticks_nbins": 5,
    
    "y_ticks_fn": "Arial",
    "y_ticks_fs": 5,
    "y_ticks_pad": 1,
    "y_ticks_weight": "normal",
    "y_ticks_rot": 0,
    "y_ticks_len": 2,
    "y_ticks_nbins": 8,
    
    "line_style": "-",
    "line_width": 1,
    "line_color": "red",
    
    "marker_style": "o",
    "marker_color": "darkred",
    "marker_size": 3,
    
    "fill_between": True,
    "fill_color": "pink",
    "fill_alpha": 0.5,
    
    "perform_resevo_fitting": False,
    "fit_line_color": "black",
    "fit_line_width": 1,
    "fit_line_style": "-",
    
    "figure_path": "plot_parameter_evolution.pdf",
    "figure_dpi": 300,
    "fig_height": 11.69,
    "fig_width": 8.69,
    
    }


def get_config():
    """
    Returns the module's default config dictionary.
    """
    return _default_config


def print_config(indent=4, sort_keys=True):
    """
    Nicely prints module's default config.
    
    Parameters
    ----------
    indent : int, optional
        Indentation for sublevels. Defaults to 4.
    
    sort_keys : bool, optional
        Sorts config keys. Default to True.
    """
    
    if not(isinstance(indent, int)):
        raise ValueError("indent should be int type")
    
    if not(isinstance(sort_keys, bool)):
        raise ValueError("sort_keys should be bool type")
    
    print(json.dumps(_default_config, indent=indent, sort_keys=sort_keys))
    
    return


def plot(
        values,
        header="",
        suptitles=None,
        peak_status=None,
        fitting=None,
        fitting_info=None,
        **kwargs,
        ):
    """
    Plots Parameter Evolution plot.
    
    Parameters
    ----------
    values : np.ndarray, shape=(Y, X), dtype=float
        Values of the parameter to plot.
        
        Where X (axis=1) represents the evolution of the parameter
        to plot for an individual residues along the titration series,
        
        and Y (axis=0) represents the different residues sequentially
        ordered according to the protein sequence.
    
        The plot X axis data (xticks) is given by the
        "titration_x_values" key of the configuration dictionary
        (see Plot Configuration Parameters bellow).
        
        "titration_x_values" should be a list of the values to represent
        in the subplots X axis ticks. Optional parameter.
        
        If not provided (default) assumes an integer range: 1, 2, 3...
        
        If "titration_x_values" can be converted to int or floats it
        will be used as such and X ticks separation will be according
        to those values.
        
        Otherwise it will be used as string labels in evenly separated
        ticks.
    
    suptitles : list of lenght Y (values.shape[0]), dtype=str, optional
        Suptitles for each subplot. Generally are the residue names:
            "1M", "2A", ...
        
        If None provided, range(values.shape[0]) is used.
    
    peak_status : np.ndarray shape (y, x), dtype=str, optional
        Peak status information according to core.utils.peak_status
        dictionary.
        
        If provided, "unnassigned" peaks will be displayed as an
        empty and identified subplot inside the subplots grid.
    
    fitting : np.ndarray shape (y, N), dtype=float, optional
        Fitting of values to an equation to plot a fitting line.
        N should be in range of <exp_values> parameter, in order for
        the fit to match the plot.
        
    fitting_info : np.array shape (y,), dtype=str, optional
        Information strings that accompany fitting values.
        Where Y is as defined for values.
        This information will be plot on the top left corner of each
        subplot.
    
    **kwargs :
        Plot details (colors, shapes, fonts, ...) can be highly
        configured through additional named parameters.
        
        The available options for named parameters are stored in a
        default configuration dictionary that can be obtained through
        the module's :func:`~get_config` (see also :func:`~prin_config`).
        
        The configuration dictionary can be modified and passed
        enterilly to the
        function call, do not forget the unpacking operator (``**``),
        or, instead if individual arguments are passed, those will
        update the default configuration.
        
        If no ``**kwargs`` are provided, the default configuration
        dictionary is used.
        
        Example:
        
        >>> my_config_dict = {"figure_path": "super_plot.pdf"}
        >>> plot(some_values, some_labels, **my_config_dict)
        
        or
        
        >>> plot(some_values, some_labels, figure_path="super_plot.pdf")
    """
    
    log.debug("* Starting Parameter Evolution Plot")
    
    if suptitles is None:
        suptitles = [str(i) for i in range(values.shape[0])]
    
    plotvalidators.validate_subplot_per_residue(
        values,
        header,
        suptitles,
        peak_status,
        fitting,
        fitting_info,
        )
    
    # # # # # validates type of positional arguments
    # # # # args2validate = [
        # # # # ("values", values, np.ndarray),
        # # # # ]
    
    # # # # [validate.validate_types(t) for t in args2validate]
    
    # # # # # validates type of named optional arguments
    # # # # args2validate = [
        # # # # ("header", header, str),
        # # # # ("suptitles", suptitles, list),
        # # # # ("peak_status", peak_status, np.ndarray),
        # # # # ("fitting", fitting, np.ndarray),
        # # # # ("fitting_info", fitting_info, np.ndarray),
        # # # # ]
    
    # # # # [validate.validate_types(t)
        # # # # for t in args2validate if t[1] is not None]
    
    # # # # # validates shapes and lenghts
    # # # # args2validate = [
        # # # # ("peak_status", peak_status),
        # # # # ]
    
    # # # # [plotvalidators.validate_shapes(values, t)
        # # # # for t in args2validate if t[1] is not None]
    
    # # # # args2validate = [
        # # # # ("suptitles", suptitles),
        # # # # ("fitting", fitting),
        # # # # ("fitting_info", fitting_info)
        # # # # ]
    
    # # # # [plotvalidators.validate_len(values[:, 0], t)
        # # # # for t in args2validate if t[1] is not None]
    
    # args2validate = [
        #
        # ]
    
    # [plotvalidators.validate_len(values[0, :], t)
        # for t in args2validate if t[1] is not None]
    
    # assigned and validates config
    config = {**_default_config, **kwargs}
    
    plotvalidators.validate_config(
        _default_config,
        config,
        name="Parameter Evolution Plot",
        )
    
    """Runs all operations to plot."""
    num_subplots = values.shape[0]
    
    if not(config["titration_x_values"]):
        
        config["titration_x_values"] = list(range(values.shape[1]))
    
    else:
    
        try:
            config["titration_x_values"] = \
                [float(i) for i in config["titration_x_values"]]
        
        except ValueError:
            config["is_float"] = False
        
        else:
            config["is_float"] = True
    
    figure, axs = plottingbase.draw_figure(
        num_subplots,
        config["rows_page"],
        config["cols_page"],
        config["fig_height"],
        config["fig_width"],
        )
    
    for i in range(values.shape[0]):
        _subplot(
            axs[i],
            values[i],
            i,
            config,
            suptitles,
            peak_status,
            fitting,
            fitting_info,
            )
    
    plottingbase.adjust_subplots(
        figure,
        config["hspace"],
        config["wspace"],
        )
    
    plottingbase.clean_subplots(axs, num_subplots)
    
    plottingbase.save_figure(
        figure,
        config["figure_path"],
        header=header,
        header_fs=config["header_fontsize"],
        dpi=config["figure_dpi"],
        )
    
    plt.close(figure)
    
    return


def _subplot(
        ax,
        values,
        i,
        c,
        suptitles,
        peak_status,
        fitting,
        fitting_info,
        ):
    """ subplot routine."""
    
    # Draws subplot title
    ax.set_title(
        suptitles[i],
        y=c["subtitle_fs"],
        fontsize=c["subtitle_fs"],
        fontname=c["subtitle_fn"],
        fontweight=c["subtitle_weight"],
        )
    
    # Defines X Axis
    
    try:
        xticks = [float(n) for n in c["titration_x_values"]]
        is_float = True
    
    except ValueError as e:
        xticks = list(range(len(values)))
        is_float = False
    
    log.debug(f"xticks: {xticks}")
    
    ax.set_xticks(xticks)
    xmin, xmax = xticks[0], xticks[-1]
    ax.set_xlim(xmin, xmax)
    
    if is_float:
        ax.locator_params(
            axis="x",
            tight=True,
            nbins=c["x_ticks_nbins"],
            )
    
    ax.set_xticklabels(
        c["titration_x_values"],
        fontname=c["x_ticks_fn"],
        fontsize=c["x_ticks_fs"],
        fontweight=c["x_ticks_weight"],
        rotation=c["x_ticks_rot"],
        )
    
    ax.xaxis.tick_bottom()
    
    ax.tick_params(
        axis='x',
        pad=c["x_ticks_pad"],
        length=c["x_ticks_len"],
        direction='out',
        )
    
    # Defines Y axis
    ax.set_ylim(c["y_lims"][0], c["y_lims"][1])
    ax.locator_params(axis='y', tight=True, nbins=c["y_ticks_nbins"])
    ax.set_yticklabels(
        ['{:.2f}'.format(yy) for yy in ax.get_yticks()],
        fontname=c["y_ticks_fn"],
        fontsize=c["y_ticks_fs"],
        fontweight=c["y_ticks_weight"],
        rotation=c["y_ticks_rot"],
        )
    
    ax.yaxis.tick_left()
    
    ax.tick_params(
        axis='y',
        pad=c["y_ticks_pad"],
        length=c["y_ticks_len"],
        direction='out',
        )
    
    # Both Axes
    ax.spines['bottom'].set_zorder(10)
    ax.spines['top'].set_zorder(10)
    ax.spines['left'].set_zorder(10)
    ax.spines['right'].set_zorder(10)

    ax.set_xlabel(
        c["x_label"],
        fontsize=c["x_label_fs"],
        labelpad=c["x_label_pad"],
        fontname=c["x_label_fn"],
        weight=c["x_label_weight"],
        )
    
    ax.set_ylabel(
        c["y_label"],
        fontsize=c["y_label_fs"],
        labelpad=c["y_label_pad"],
        fontname=c["y_label_fn"],
        weight=c["y_label_weight"],
        )
    
    # writes unassigned in the center of the plot for unassigned peaks
    # and plots nothing
    if peak_status is not None and peak_status[i, 0] == 'unassigned':
        ax.text(
            (c["titration_x_value"][0] + c["titration_x_value"][-1]) / 2,
            (c["y_lims"][0] + c["y_lims"][1]) / 2,
            'unassigned',
            fontsize=8,
            fontname='Arial',
            va='center',
            ha='center',
            )
        
        return
    
    # do not represent the missing peaks.
    if peak_status is not None:
        measured_mask = peak_status[i, :] == "measured"
        measured_values = values[measured_mask]
        x_measured = ax.get_xticks()[measured_mask]
    
    else:
        measured_values = values
        x_measured = ax.get_xticks()
    
    # Plots data
    ax.plot(
        x_measured,
        measured_values,
        ls=c["line_style"],
        color=c["line_color"],
        marker=c["marker_style"],
        mfc=c["marker_color"],
        markersize=c["marker_size"],
        lw=c["line_width"],
        zorder=5,
        )
    
    if c["fill_between"]:
        ax.fill_between(
            x_measured,
            0,
            measured_values,
            facecolor=c["fill_color"],
            alpha=c["fill_alpha"],
            )
    
    if fitting is not None:
        ax.plot(
            np.linspace(
                c["titration_x_values"][0],
                c["titration_x_values"][-1],
                len(fitting[i, :]),
                ),
            fitting[i, :],
            ls=c["fit_line_style"],
            lw=c["fit_line_width"],
            color=c["fit_line_color"],
            zorder=6,
            )
    
    if fitting_info is not None:
        ax.text(
            xmax * 0.05,
            c["y_lims"][1] * 0.97,
            fitting_info[i],
            ha='left',
            va='top',
            fontsize=4,
            )
    
    return


if __name__ == "__main__":
    
    print("I am ResEvoPlot")

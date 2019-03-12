"""
The Compacted Bar Plot template draws square-shaped subplots
designed to fit half page with individually.

Each subplot represents an datapoint in the experimental titration,
i.e., a peaklist.

The value of the parameter is represented for each residue in the
form of bars - there is a bar for each residue.

Subplots are stacked sequentially in grid from left to right and from
top to bottom. This arrangement can be used directly as a supplementary
figure in your publications.

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
from FarseerNMR.core import validate
from FarseerNMR.plot.base import (
    plottingbase,
    experimentplotbase,
    barplotbase,
    plotvalidators,
    )

log = logger.get_log(__name__)

_default_config = {
    "cols_page": 3,
    "rows_page": 5,

    "y_lims": (0, 0.3),
    "x_label": "Residues",
    "y_label": "your labels goes here",
    
    "suptitle_fn": "Arial",
    "suptitle_fs": 8,
    "suptitle_pad": 0.99,
    "suptitle_weight": "normal",
    
    "x_label_fn": "Arial",
    "x_label_fs": 8,
    "x_label_pad": 2,
    "x_label_weight": "bold",
    "x_label_rotation": 0,
    
    "y_label_fn": "Arial",
    "y_label_fs": 8,
    "y_label_pad": 3,
    "y_label_weight": "bold",
    "y_label_rot": 90,
    
    "x_ticks_pad": 2,
    "x_ticks_len": 2,
    "x_ticks_fn": "Arial",
    "x_ticks_fs": 6,
    "x_ticks_rot": 0,
    "x_ticks_weight": "normal",
    
    "y_ticks_fn": "Arial",
    "y_ticks_fs": 6,
    "y_ticks_rot": 0,
    "y_ticks_pad": 1,
    "y_ticks_weight": "normal",
    "y_ticks_len": 2,
    "y_ticks_nbins": 8,
    
    "y_grid_flag": True,
    "y_grid_color": "lightgrey",
    "y_grid_linestyle": "-",
    "y_grid_linewidth": 0.2,
    "y_grid_alpha": 0.8,
    
    "measured_color": "black",
    "missing_color": "red",
    "unassigned_color": "lightgrey",
    
    "unassigned_shade": True,
    "unassigned_shade_alpha": 0.5,
    
    "bar_width": 0.8,
    "bar_alpha": 1,
    "bar_linewidth": 0,
    
    "mark_fontsize": 4,
    "mark_prolines_flag": False,
    "mark_prolines_symbol": "P",
    "mark_user_details_flag": False,
    "color_user_details_flag": False,
    "user_marks_dict": {
        "foo": "f",
        "bar": "b",
        "boo": "o"
        },
    "user_bar_colors_dict": {
        "foo": "green",
        "bar": "yellow",
        "boo": "magenta"
        },
    
    "threshold_flag": True,
    "threshold_color": "red",
    "threshold_linewidth": 0.5,
    "threshold_alpha": 0.8,
    "threshold_zorder": 10,
    
    "plot_theoretical_pre": False,
    "theo_pre_color": "red",
    "theo_pre_lw": 1.0,
    "tag_id": "*",
    
    "tag_cartoon_color": "black",
    "tag_cartoon_ls": "-",
    "tag_cartoon_lw": 1.0,
    
    "hspace": 0.5,
    "wspace": 0.5,
    
    "figure_header": "No header provided",
    "header_fontsize": 5,
    
    "figure_path": "bar_compacted.pdf",
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
        labels,
        header="",
        suptitles=None,
        letter_code=None,
        peak_status=None,
        details=None,
        tag_position=None,
        theo_pre=None,
        **kwargs,
        ):
    """
    Plots according to the Compacted Bar Plot Template.
    
    Parameters
    ----------
    values : np.ndarray, shape=(y,x), dtype=float
        Where X (axis=1) is the data to plot for each bar (residue),
        Y (axis=0) is the evolution of that data along the titration
        series.
        
    labels : np.ndarray, shape=(x,), dtype=str
        Bar labels which are drawn as xtick labels.
    
    header : str, optional
        Multi-line string with additional human-readable notes.
        Header will be written in the output figure file in a dedicated
        blank space.
    
    suptitles : list of str, optional
        Titles of each subplot, length must be equal to values.shape[0].
        Defaults to a range of values.shape[0], ["0", "1", "2", ...
        
    letter_code : np.ndarray, shape=(x,), dtype=str, optional
        1-letter code of the protein sequence, should have length equal
        to <labels>.
        Defaults to None.

    peak_status : np.ndarray, shape=(y,x), dtype=str, optional
        Peak status information according to core.utils.peak_status
        dictionary.
        Defaults to None.

    details : np.ndarray, shape=(y,x), dtype=str, optional
        Peaklist Details column information.
        Defaults to None.
        
    theo_pre : np.ndarray, shape=(y,x), dtype=str, optional
        Information on theoretical PRE data.
        Defaults to None.

    tag_position : np.ndarray, shape=(y,x), dtype=str, optional
        Null values where tag not present, "*" character denotes
        the position of the of the paramagnetic tag.
        If None provided, Tag tick is not drawn.
        Defaults to None.
    
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
    
    log.debug("* Starting barplotcompacted")
    
    if suptitles is None:
        suptitles = [str(i) for i in range(values.shape[0])]
    
    plotvalidators.validate_barplot_params(
        values,
        labels,
        header,
        suptitles,
        letter_code,
        peak_status,
        details,
        tag_position,
        theo_pre,
        )
    
    # suptitles = suptitles or [str(i) for i in range(values.shape[0])]
    
    # # validates type of positional arguments
    # args2validate = [
        # ("values", values, np.ndarray),
        # ("label", labels, np.ndarray),
        # ]
    
    # [validate.validate_types(t) for t in args2validate]
    
    # # validates type of optional named arguments
    # args2validate = [
        # ("header", header, str),
        # ("suptitles", suptitles, list),
        # ("letter_code", letter_code, np.ndarray),
        # ("peak_status", peak_status, np.ndarray),
        # ("details", details, np.ndarray),
        # ("tag_position", tag_position, np.ndarray),
        # ("theo_pre", theo_pre, np.ndarray),
        # ]
    
    # [validate.validate_types(t) for t in args2validate if t[1] is not None]
    
    # # validates shapes and lenghts of arguments
    # args2validate = [
        # ("peak_status", peak_status),
        # ("details", details),
        # ("tag_position", tag_position),
        # ("theo_pre", theo_pre),
        # ]
    
    # [plotvalidators.validate_shapes(values, t)
        # for t in args2validate if t[1] is not None]
    
    # args2validate = [
        # ("labels", labels),
        # ("letter_code", letter_code),
        # ]
    
    # [plotvalidators.validate_len(values[0, :], t)
        # for t in args2validate if t[1] is not None]
    
    # plotvalidators.validate_len(values[:, 0], ("suptitles", suptitles))
    
    # assigned and validates config
    config = {**_default_config, **kwargs}
    
    plotvalidators.validate_config(
        _default_config,
        config,
        name="Compacted Bar Plot",
        )
    
    """Runs all operations to plot."""
    num_subplots = experimentplotbase.calc_num_subplots(values)
    
    figure, axs = plottingbase.draw_figure(
        num_subplots,
        config["rows_page"],
        config["cols_page"],
        config["fig_height"],
        config["fig_width"],
        )
    
    for i in range(values.shape[0]):
        
        log.debug("Starting subplot no: {}".format(i))
        # other parameters are not passed because they are None by default
        # and may lead to IndexError
        _subplot(
            axs[i],
            values[i],
            labels,
            i,
            config,
            suptitles,
            letter_code,
            peak_status,
            details,
            tag_position,
            theo_pre,
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
        labels,
        i,
        c,
        suptitles,
        letter_code,
        peak_status,
        details,
        tag_position,
        theo_pre,
        ):
    """Subplot routine."""
    
    ###################
    # configures vars
    ydata = np.nan_to_num(values).astype(float)
    log.debug("ydata: {}".format(ydata))
    num_of_bars = ydata.size
    log.debug("Number of bars to represented: {}".format(num_of_bars))
    log.debug("Suptitle: {}".format(suptitles[i]))
    
    ###################
    # Plots bars
    bars = ax.bar(
        range(num_of_bars),
        ydata,
        width=c["bar_width"],
        align='center',
        alpha=c["bar_alpha"],
        linewidth=c["bar_linewidth"],
        color='black',
        zorder=4,
        )
    
    log.debug(f"Number of bars plotted: {len(bars)}")
    log.debug(
        "Number of expected bars equals num of bars: "
        f"{num_of_bars == len(bars)}"
        )
    
    ###################
    # Set subplot title
    ax.set_title(
        suptitles[i],
        y=c["suptitle_pad"],
        fontsize=c["suptitle_fs"],
        fontname=c["suptitle_fn"],
        weight=c["suptitle_weight"],
        )
    
    log.debug("Subplot title set to : {}".format(suptitles[i]))
    
    ###################
    # Configures spines
    ax.spines['bottom'].set_zorder(10)
    ax.spines['top'].set_zorder(10)
    log.debug("Spines set: OK")
    
    ###################
    # Configures X ticks and X ticks labels
    
    xticks, xticks_labels = barplotbase.compacted_bar_xticks(
        num_of_bars,
        labels,
        )
    
    # Set X ticks
    ax.set_xticks(xticks)
    
    # Set X ticks labels
    # https://github.com/matplotlib/matplotlib/issues/6266
    ax.set_xticklabels(
        xticks_labels,
        fontname=c["x_ticks_fn"],
        fontsize=c["x_ticks_fs"],
        fontweight=c["x_ticks_weight"],
        rotation=c["x_ticks_rot"],
        )
    
    # Set xticks params
    ax.tick_params(
        axis='x',
        pad=c["x_ticks_pad"],
        length=c["x_ticks_len"],
        direction='out',
        )
    log.debug("Configured X tick params: OK")
    
    # Set X axis label
    ax.set_xlabel(
        c["x_label"],
        fontname=c["x_label_fn"],
        fontsize=c["x_label_fs"],
        labelpad=c["x_label_pad"],
        weight=c["x_label_weight"],
        rotation=c["x_label_rotation"],
        )
    log.debug("Set X label: OK")
    
    ###################
    # Configures Y ticks and axis
    
    # sets axis limits
    ymin = c["y_lims"][0]
    ymax = c["y_lims"][1]
    ax.set_ylim(ymin, ymax)
    log.debug("Set y max {} and ymin {}".format(ymin, ymax))
    
    # sets number of y ticks
    ax.locator_params(axis='y', tight=True, nbins=c["y_ticks_nbins"])
    
    # sets y tick labels
    ax.set_yticklabels(
        ['{:.2f}'.format(yy) for yy in ax.get_yticks()],
        fontname=c["y_ticks_fn"],
        fontsize=c["y_ticks_fs"],
        fontweight=c["y_ticks_weight"],
        rotation=c["y_ticks_rot"],
        )
    log.debug("Set Y tick labels: OK")
    
    # sets y ticks params
    ax.tick_params(
        axis='y',
        pad=c["y_ticks_pad"],
        length=c["y_ticks_len"],
        direction='out'
        )
    log.debug("Configured Y tick params: OK")
    
    # set Y label
    ax.set_ylabel(
        c["y_label"],
        fontsize=c["y_label_fs"],
        labelpad=c["y_label_pad"],
        fontname=c["y_label_fn"],
        weight=c["y_label_weight"],
        rotation=c["y_label_rot"],
        )
    log.debug("Set Y label: OK")
    
    ###################
    # Additional configurations
    # "is not None" is used in IF statements intentionally
    
    ax.margins(x=0.01, tight=True)
    
    # defines bars colors
    if peak_status is not None:
        experimentplotbase.set_item_colors(
            bars,
            peak_status[i],
            {
                'measured': c["measured_color"],
                'missing': c["missing_color"],
                'unassigned': c["unassigned_color"]
                }
            )
        log.debug("set_item_colors: OK")
    
    ###################
    # Additional representation features
    
    # Adds grid
    if c["y_grid_flag"]:
        ax.yaxis.grid(
            color=c["y_grid_color"],
            linestyle=c["y_grid_linestyle"],
            linewidth=c["y_grid_linewidth"],
            alpha=c["y_grid_alpha"],
            zorder=0
            )
        log.debug("Configured grid: OK")
    
    # Adds red line to identify significant changes.
    if c["threshold_flag"]:
        log.debug("... Starting threshold draw")
        barplotbase.plot_threshold(
            ax,
            ydata,
            threshold_color=c["threshold_color"],
            threshold_linewidth=c["threshold_linewidth"],
            threshold_alpha=c["threshold_alpha"],
            threshold_zorder=c["threshold_zorder"],
            )
        log.debug("Threshold: OK")
    
    if letter_code is not None and c["mark_prolines_flag"]:
        log.debug("... Starting Prolines Mark")
        experimentplotbase.text_marker(
            ax,
            range(num_of_bars),
            ydata,
            letter_code,
            {'P': c["mark_prolines_symbol"]},
            fs=c["mark_fontsize"],
            )
        log.debug("Prolines Marked: OK")
    
    if details is not None and c["mark_user_details_flag"]:
        log.debug("... Starting User Details Mark")
        experimentplotbase.text_marker(
            ax,
            range(num_of_bars),
            ydata,
            details[i],
            c["user_marks_dict"],
            fs=c["mark_fontsize"],
            )
        log.debug("User marks: OK")
    
    if details is not None and c["color_user_details_flag"]:
        log.debug("... Starting User Colors Mark")
        experimentplotbase.set_item_colors(
            bars,
            details[i],
            c["user_bar_colors_dict"],
            )
        log.debug("Color user details: OK")
           
    if theo_pre is not None \
            and tag_position is not None \
            and c["plot_theoretical_pre"]:
        
        experimentplotbase.plot_theo_pre(
            ax,
            range(num_of_bars),
            theo_pre[i],
            theo_pre_color=c["theo_pre_color"],
            theo_pre_lw=c["theo_pre_lw"],
            )
        
        tag_found = experimentplotbase.finds_paramagnetic_tag(
            bars,
            tag_position[i],
            )
        
        if tag_found:
            experimentplotbase.draw_paramagnetic_tag(
                ax,
                tag_found,
                ymax,
                tag_cartoon_color=c["tag_cartoon_color"],
                tag_cartoon_ls=c["tag_cartoon_ls"],
                tag_cartoon_lw=c["tag_cartoon_lw"],
                )
    
    return


if __name__ == "__main__":
    
    c = {
        "mark_user_details_flag": True,
        "color_user_details_flag": True,
        "user_marks_dict": {
            "yell": "y"
            },
        "user_bar_colors_dict": {
            "yell": "yellow"
            },
        "figure_dpi": 300,
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
    
    # ####################################################################### 1
    #    Short data set
    
    shape = (7, 8)
    name = "compacted_1.png"
    
    values, labels, suptitles, letter_code, \
    peak_status, details, tag_position, theo_pre = make_data(shape)
    
    for i in range(shape[0]):
        values[i,i] = 0.05 * i
        details[i, i] = "yell"
    
    plot(
        values,
        labels,
        details=details,
        header=name,
        figure_path=name,
        **c)
    
    # ####################################################################### 2
    # 100 Dataset
    
    shape = (3, 100)
    name = "compacted_2.png"
    
    values, labels, suptitles, letter_code, \
    peak_status, details, tag_position, theo_pre = make_data(shape)
    
    plot(
        values,
        labels,
        details=details,
        header=name,
        figure_path=name,
        **c)
    
    # ####################################################################### 2
    # 200 Dataset
    
    shape = (3, 200)
    name = "compacted_3.png"
    
    values, labels, suptitles, letter_code, \
    peak_status, details, tag_position, theo_pre = make_data(shape)
    
    values[1, 100:200] = 0.0
    tag_position[1, 150] = "*"
    
    plot(
        values,
        labels,
        details=details,
        tag_position=tag_position,
        theo_pre=theo_pre,
        header=name,
        figure_path=name,
        plot_theoretical_pre=True,
        **c)
    
    # ####################################################################### 4
    # 1000 Dataset
    
    shape = (3, 1000)
    name = "compacted_4.png"
    
    values, labels, suptitles, letter_code, \
    peak_status, details, tag_position, theo_pre = make_data(shape)
    
    details[0, 100:200] = "yell"
    details[1, 200:300] = "yell"
    details[2, 600:700] = "yell"
    
    print(suptitles)
    
    plot(
        values,
        labels,
        suptitles=suptitles,
        details=details,
        header=name,
        figure_path=name,
        **c)

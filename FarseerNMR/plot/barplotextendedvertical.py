"""
Extended Vertical Bar Plot.

Each subplot represents an datapoint in the experimental titration,
i.e., a peaklist.

The value of the parameter is represented for each residue in the
form of bars - there is a bar for each residue.

Subplots are stacked sequentially from left to right. This arrangement
can be used directly as a supplementary figure in your publications.
Or subplots can be cropped to fit figure panels.

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
    "cols_page": 5,
    "rows_page": 2,
    
    "y_lims": (0, 0.3),
    "x_label": "Residues",
    "y_label": "your labels goes here",
    
    "suptitle_fn": "Arial",
    "suptitle_fs": 8,
    "suptitle_pad": 0.99,
    "suptitle_weight": "normal",
    
    "x_label_fn": "Arial",
    "x_label_fs": 8,
    "x_label_pad": 15,
    "x_label_weight": "bold",
    "x_label_rotation": -90,
    
    "y_label_fn": "Arial",
    "y_label_fs": 8,
    "y_label_pad": 3,
    "y_label_weight": "bold",
    "y_label_rot": 0,
    
    "x_ticks_pad": 2,
    "x_ticks_len": 2,
    "x_ticks_fn": "monospace",
    "x_ticks_fs": 4,
    "x_ticks_rot": 0,
    "x_ticks_weight": "normal",
    "x_ticks_color_flag": True,
    
    "y_ticks_fn": "Arial",
    "y_ticks_fs": 6,
    "y_ticks_rot": 45,
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
    
    "figure_path": "bar_extended_vertical.pdf",
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
    Plots Vertical Extended Bar plots.
    
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

    peak_status : np.ndarray, shape=(y,x), dtype=str, optional
        Peak status information according to core.utils.peak_status
        dictionary.

    details : np.ndarray, shape=(y,x), dtype=str, optional
        Peaklist Details column information.
    
    theo_pre : np.ndarray, shape=(y,x), dtype=str, optional
        Information on theoretical PRE data.

    tag_position : np.ndarray, shape=(y,x), dtype=str, optional
        Null values where tag not present, "*" character denotes
        the position of the of the paramagnetic tag.
        If None provided, Tag tick is not drawn.
    
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
    
    log.debug("* Starting BarPlot Extended Vertical")
    
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
    num_of_bars = ydata.shape[0]
    log.debug("Number of bars to represented: {}".format(num_of_bars))
    log.debug("Suptitle: {}".format(suptitles[i]))
    
    ###################
    # Plots bars
    bars = ax.barh(
        range(num_of_bars),
        ydata,
        height=c["bar_width"],
        align='center',
        alpha=c["bar_alpha"],
        linewidth=c["bar_linewidth"],
        color=c["measured_color"],
        zorder=4,
        )
    
    log.debug("Number of bars plotted: {}".format(len(bars)))
    log.debug(
        f"Num of expected bars equals num of bars: {num_of_bars == len(bars)}"
        )
    
    # necessary for vertical template
    ax.invert_yaxis()
    
    ###################
    # Set subplot title
    ax.set_title(
        suptitles[i],
        y=c["suptitle_pad"],
        fontsize=c["suptitle_fs"],
        fontname=c["suptitle_fn"],
        weight=c["suptitle_weight"],
        )
    log.debug("Set title: OK")
    
    ###################
    # Configures spines
    ax.spines['bottom'].set_zorder(10)
    ax.spines['top'].set_zorder(10)
    log.debug("Spines set: OK")

    # Configure XX ticks and Label
    
    # Define tick spacing
    mod_ = barplotbase._extended_bar_xticks(num_of_bars)
    
    # set xticks and xticks_labels to be represented
    yticks = np.arange(len(bars))[0::mod_]
    yticks_labels = np.array(labels)[0::mod_]
    
    log.debug("xticks represented: {}".format(yticks))
    log.debug("xticks labels represented: {}".format(yticks_labels))
    
    # Set Y ticks
    ax.set_yticks(yticks)
    
    # Set Y ticks labels
    # https://github.com/matplotlib/matplotlib/issues/6266
    ax.set_yticklabels(
        yticks_labels,
        fontname=c["x_ticks_fn"],
        fontsize=c["x_ticks_fs"],
        fontweight=c["x_ticks_weight"],
        rotation=c["x_ticks_rot"],
        )
    
    # Set xticks params
    ax.tick_params(
        axis='y',
        pad=c["x_ticks_pad"],
        length=c["x_ticks_len"],
        direction='out',
        )
    
    log.debug("Configured X tick params: OK")
    
    # Set Y axis label
    ax.set_ylabel(
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
    ax.set_xlim(ymin, ymax)
    log.debug("Set y max {} and ymin {}".format(ymin, ymax))
    
    # sets number of y ticks
    ax.locator_params(axis='x', tight=True, nbins=c["y_ticks_nbins"])
    
    # sets y tick labels
    ax.set_xticklabels(
        ['{:.2f}'.format(yy) for yy in ax.get_xticks()],
        fontname=c["y_ticks_fn"],
        fontsize=c["y_ticks_fs"],
        fontweight=c["y_ticks_weight"],
        rotation=c["y_ticks_rot"],
        )
    log.debug("Set Y tick labels: OK")
    
    # sets y ticks params
    ax.tick_params(
        axis='x',
        pad=c["y_ticks_pad"],
        length=c["y_ticks_len"],
        direction='out',
        )
    log.debug("Configured Y tick params: OK")
    
    # set X label
    ax.set_xlabel(
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
    
    ax.margins(y=0.01, tight=True)
    
    # defines bars colors
    if peak_status is not None:
        experimentplotbase.set_item_colors(
            bars,
            peak_status[i],
            {
                'measured': c["measured_color"],
                'missing': c["missing_color"],
                'unassigned': c["unassigned_color"],
                },
            )
        log.debug("set_item_colors: OK")
    
    ###################
    # Additional representation features
    
    # Adds grid
    if c["y_grid_flag"]:
        ax.xaxis.grid(
            color=c["y_grid_color"],
            linestyle=c["y_grid_linestyle"],
            linewidth=c["y_grid_linewidth"],
            alpha=c["y_grid_alpha"],
            zorder=0,
            )
        log.debug("Configured grid: OK")
    
    # defines xticks colors
    if peak_status is not None and c["x_ticks_color_flag"]:
        log.debug("Configuring for x_ticks_color_flag...")
        experimentplotbase.set_item_colors(
            ax.get_yticklabels(),
            peak_status[i, 0::mod_],
            {
                'measured': c["measured_color"],
                'missing': c["missing_color"],
                'unassigned': c["unassigned_color"],
                },
            )
        log.debug("...Done")
    
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
            orientation="vertical",
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
            orientation="vertical",
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
            orientation="vertical",
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
            plottype="v",
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
                plottype="v",
                )
    
    return


if __name__ == "__main__":
    
    name = "barplotextendedvertical"
    
    for example in barplotxmpls.list_of_examples:
        example(plot, name)


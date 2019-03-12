# -*- coding: utf-8 -*-
"""
This module contains functions that make calculations :-)
"""
import numpy as np
from math import ceil

from FarseerNMR import logger

log = logger.get_log(__name__)


def threshold_std_of_population(
        values,
        *,
        std=5,
        population=0.1,
        ):
    r"""
    Calculates the significancy threshold according to a standard
    deviation of a given population.
    
        ``\overline{pop} + {std} \ast {\sigma_{pop}}``
    
    where, ``pop`` is the ``population`` percentage with the minimum
    values in ``values``.
    
    Parameters
    ----------
    values : :obj:`np.ndarray`, dtype=float, n_dims=1
        An array with the values upon which calculate the threshold.
    
    std : :obj:`int`
        The standard deviations.
        Defaults to 5.
    
    population : :obj:`float`
        The percentage of population with minimum values
        upon which the threshold is calculated.
        Defaults to 0.1.
    
    Returns
    -------
    float
        The threshold value.
    
    Raises
    ------
    TypeError
        If values is not np.ndarray type of ndim == 1.
    """
    
    if not(isinstance(values, np.ndarray)):
        raise TypeError("values should be an ARRAY")
    
    if not(values.ndim == 1):
        raise TypeError("values should have only one dimension")
    
    sorted_values = np.copy(np.sort(np.absolute(values)))
    parsed_values = sorted_values[np.logical_not(np.isnan(sorted_values))]
    
    firstpop = parsed_values[0: ceil(0.1 * len(parsed_values))]
    log.debug(f"<firstpop>: {firstpop}")
    
    mean = np.mean(firstpop)
    log.debug(f"mean: {mean}")
    
    stdev = np.std(firstpop)
    log.debug(f"stdev {stdev}")
    
    threshold = mean + std * stdev
    
    log.debug(f"threshold: {threshold}")
    
    assert isinstance(threshold, float), "threshold MUST be float"
    return threshold


if __name__ == "__main__":
    
    t = threshold_std_of_population(np.ones(100))
    print(t)

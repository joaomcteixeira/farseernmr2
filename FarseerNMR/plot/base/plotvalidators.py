import sys
import numpy as np

from FarseerNMR import logger
from FarseerNMR.core import core, validate

log = logger.get_log(__name__)


def validate_barplot_params(
        values,
        labels,
        header,
        suptitles,
        letter_code,
        peak_status,
        details,
        tag_position,
        theo_pre,
        ):
    
    if not(values.ndim == 2):
        msg_ = (
            "* DATA ERROR * VALUES must have 2 dimensions. "
            f"{values.ndim} given."
            )
        
        log.info(msg_)
        sys.exit(core.abort_message)
    
    # validates type of positional arguments
    args2validate = [
        ("values", values, np.ndarray),
        ("label", labels, np.ndarray),
        ]
    
    [validate.validate_types(t) for t in args2validate]
    
    # validates type of optional named arguments
    args2validate = [
        ("header", header, str),
        ("suptitles", suptitles, list),
        ("letter_code", letter_code, np.ndarray),
        ("peak_status", peak_status, np.ndarray),
        ("details", details, np.ndarray),
        ("tag_position", tag_position, np.ndarray),
        ("theo_pre", theo_pre, np.ndarray),
        ]
    
    [validate.validate_types(t) for t in args2validate if t[1] is not None]
    
    # validates shapes and lenghts of arguments
    args2validate = [
        ("peak_status", peak_status),
        ("details", details),
        ("tag_position", tag_position),
        ("theo_pre", theo_pre),
        ]
    
    [validate_shapes(values, t) for t in args2validate if t[1] is not None]
    
    args2validate = [
        ("labels", labels),
        ("letter_code", letter_code),
        ]
    
    [validate_len(values[0, :], t) for t in args2validate if t[1] is not None]
    
    validate_len(values[:, 0], ("suptitles", suptitles))
    
    return


def validate_subplot_per_residue(
        values,
        header,
        suptitles,
        peak_status,
        fitting,
        fitting_info,
        ):
    
    # validates type of positional arguments
    args2validate = [
        ("values", values, np.ndarray),
        ]
    
    [validate.validate_types(t) for t in args2validate]
    
    # validates type of named optional arguments
    args2validate = [
        ("header", header, str),
        ("suptitles", suptitles, list),
        ("peak_status", peak_status, np.ndarray),
        ("fitting", fitting, np.ndarray),
        ("fitting_info", fitting_info, np.ndarray),
        ]
    
    [validate.validate_types(t)
        for t in args2validate if t[1] is not None]
    
    # validates shapes and lenghts
    args2validate = [
        ("peak_status", peak_status),
        ]
    
    [validate_shapes(values, t) for t in args2validate if t[1] is not None]
    
    args2validate = [
        ("suptitles", suptitles),
        ("fitting", fitting),
        ("fitting_info", fitting_info)
        ]
    
    [validate_len(values[:, 0], t) for t in args2validate if t[1] is not None]
    
    return

def validate_config(ref, target, name="some config"):
    """
    Validate config dictionary for DeltaPRE Heat Map Plot template.
    
    Loops over config keys and checks if values' type are the
    expected. Raises ValueError otherwise.
    
    Parameters
    ----------
    ref : dict
        The reference configuration dictionary.
    
    target : dict
        The target configuration dictionary.
    
    name : str, optional
        The name of the dict for Error identification.
    """
    
    def eval_types(key, value):
        
        a = type(target[key])
        b = type(value)
        
        if not(a == b):
            msg = (
                f"Argument '{key}' in {name} Plot is not of "
                f"correct type, is {a}, should be {b}."
                )
            log.info(msg)
            raise TypeError(msg)
    
    for key, value in ref.items():
        eval_types(key, value)
    
    msg = f"Parameters type for {name} evaluated successfully"
    log.debug(msg)
    
    return


def validate_shapes(reference, target_tuple):
    
    if target_tuple[1].shape != reference.shape:
        raise ValueError(
            f"Shape of {target_tuple[0]} ({target_tuple[1].shape}) differs "
            f"from reference shape ({reference.shape})"
            )
    

def validate_len(reference, target_tuple):
    """
    Validates len of args against len of reference.
    """
    
    if len(target_tuple[1]) != len(reference):
        raise ValueError(
            f"Length of '{target_tuple[0]}' parameter ({len(target_tuple[1])})"
            f" differs from reference length ({len(reference)})"
            )

"""
Handles Farseer-NMR logging system.

By default, generates a farseernmr.log and a farseernmr.debug files
with each run. *farseernmr.log* contains scientific information
regarding the run, and *farseernmr.debug* contains information
for developers. Also, you can send us *.debug* file if you wan to
comunicate an issue with a run.
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

import logging
import logging.config

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    
    "formatters": {
        "debug_format": {
            "format": (
                "%(levelname)s - "
                "%(name)s:%(funcName)s:%(lineno)d - "
                "%(message)s"
                )
            },
        "info_format": {
            "format": "%(message)s"}
        },
    
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "info_format",
            "stream": "ext://sys.stdout"
            },
        
        "info_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "debug_format",
            "filename": "farseernmr.log",
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
            },
        
        "debug_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "debug_format",
            "filename": "farseernmr.debug",
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
            }
        },
    
    "loggers": {},
    
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "info_file_handler", "debug_file_handler"]
        }
    }
"""
Logging configuration dictionary.
"""


def get_log(name):
    """
    Returns logger according to :const:`~log_config`.
    """
    # logging.addLevelName(15, "DEBUG")
    logging.config.dictConfig(log_config)
    return logging.getLogger(name)

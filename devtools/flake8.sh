#!/bin/bash

# W293 blank line contains whitespaces
# W503 line break before binary operator, actually favoured by PEP8
# E402 module level import not at top of file, in Farseer-NMR sometimes is necessary to import later on
# -hang-closing, allows:
#my_func(
#    var1,
#    var2,
#    )

clear
flake8 --hang-closing --ignore=W293,W503,E402 $1

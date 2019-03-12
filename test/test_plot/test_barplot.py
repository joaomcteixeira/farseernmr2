from filecmp import cmp
import os 

import numpy as np

from FarseerNMR.plot import (
    barplotcompacted,
    )

from FarseerNMR.plot.examples import (
    barplotxmpls,
    )

dir_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))


def test_barplots():
    
    list_of_nametest = [
        os.path.join(dir_path, "__test_barplotcompacted"),
        os.path.join(dir_path, "__test_barplotextended"),
        ]
    
    for module, name, nametest in zip(
            barplotxmpls.list_of_templates,
            barplotxmpls.list_of_names,
            list_of_nametest,
            ):
        
        for i, example in enumerate(barplotxmpls.list_of_examples, start=1):
            example(module.plot, nametest)
            
            assert cmp(
                f"{nametest}_{i}.{barplotxmpls.ext}",
                os.path.join(
                    dir_path,
                    "original",
                    f"{name}_{i}.{barplotxmpls.ext}"
                    ),
                shallow=False,
                )
                
    return
    

from filecmp import cmp
import os 

import numpy as np

from FarseerNMR.plot import barplotcompacted


dir_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

def test_barplotcompacted_1():
    
    values = np.full((7, 15), 0.2)
    for i in range(7):
        values[i,i] = 0.05 * i
    
    values[6, 9] = 0.033
    
    labels = np.arange(1, len(values[0]) + 1).astype(str)
    
    test_plot = os.path.join(dir_path, "test_compacted_1.png")
    
    c = {
	"figure_path": test_plot,
	"figure_dpi": 100,
	}
    
    barplotcompacted.plot(values, labels, header="12", **c)
    
    isequal = cmp(
        test_plot,
        os.path.join(dir_path, "compacted_1.png"),
        shallow=False,
        )
    
    assert isequal
    
    return

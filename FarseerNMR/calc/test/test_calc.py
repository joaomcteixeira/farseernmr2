import numpy as np

from FarseerNMR.calc import calc

def test_threshold_1():
    
    values = np.ones(100)
    
    t = calc.threshold_std_of_population(values)
    
    assert t == 1
    
    return

def test_threshold_2():
    
    values = np.arange(100)
    
    t = calc.threshold_std_of_population(values)
    
    y = np.mean(np.arange(10)) + 5 * np.std(np.arange(10))
    
    assert t == y
    return

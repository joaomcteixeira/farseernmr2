from FarseerNMR.core import wet

def test_wet_1():
    """
    WET width 70.
    """
    
    _ = """
****************************** TESTING *******************************
*   This is a testing message for Farseer-NMR WET list. It contains  *
*         several lines. Tabbed with triple quoted strings.          *
*                                                                    *
*                           Please visit:                            *
*   https://github.com/Farseer-NMR/FarSeer-NMR/wiki/WET-List#wet1    *
**********************************************************************
"""
    
    a = wet.generate(
        "TESTING",
        """
        This is a testing message for Farseer-NMR WET list.
        It contains several lines.
        Tabbed with triple quoted strings.
        """,
        1,
        )
    
    assert a == _

def test_wet_2():
    """
    WET width 80.
    """
    
    _ = """
*********************************** TESTING ************************************
*    This is a testing message for Farseer-NMR WET list. It contains several   *
*                  lines. Tabbed with triple quoted strings.                   *
*                                                                              *
*                                Please visit:                                 *
*        https://github.com/Farseer-NMR/FarSeer-NMR/wiki/WET-List#wet1         *
********************************************************************************
"""
    
    a = wet.generate(
        "TESTING",
        """
        This is a testing message for Farseer-NMR WET list.
        It contains several lines.
        Tabbed with triple quoted strings.
        """,
        1,
        width=80,
        )
    
    assert a == _

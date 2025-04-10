'''
This is a moudle for python unit calculation
Use this moudle,plese write: 
`Unit()` or other class in this moudle.
If you want to create new unit class,please use: 
```
class A(ABCUnit)
```
'''

from .units import *
from decimal import Decimal as long
from fractions import Fraction as fraction
# from . import shapes
from ..tools.dec import dint,SimpleType

__all__ = [
    "shapes", "fraction", "long", "dint", "SimpleType", "numpy", "matplotlib", 
    "Unit", "Line", "Area", "Volume", "Capacity", "Duration", "Version", "datetime", "operators"
]

try:
    import numpy, matplotlib
except (ImportError, ModuleNotFoundError):
    pass

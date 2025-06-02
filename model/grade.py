"""
    grade.py

    Contains an enumeration class for grades and associated values.
"""

from enum import Enum

class Grade(Enum):
    """
        Contains grades and associated values.
    """

    WN = 0.0
    N = 0.3
    P = 1.0
    C = 2.0
    D = 3.0
    HD = 4.0

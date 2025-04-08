# src/hyqerionmath/__init__.py
"""
HyqerionMath Package
A collection of mathematical utility functions.
"""
# Import functions from modules to make them available at the package level
from .primality import isprime

# Define what 'from hyqerionmath import *' imports
__all__ = ['isprime']

# Define the package version (can also be managed by build tools)
__version__ = "0.2.0"
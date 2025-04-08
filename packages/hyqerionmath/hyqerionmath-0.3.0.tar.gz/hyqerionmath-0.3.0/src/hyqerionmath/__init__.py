# src/hyqerionmath/__init__.py
"""
HyqerionMath Package
A collection of mathematical utility functions.
"""
# Import functions from modules to make them available at the package level
from .primality import isprime, get_nth_prime, get_primes_in_index_range, find_primes_between

# Define what 'from hyqerionmath import *' imports
__all__ = [
    'isprime',
    'get_nth_prime',
    'get_primes_in_index_range',
    'find_primes_between'
]

# Define the package version (should match pyproject.toml)
__version__ = "0.3.0" # Incremented version for new features
# src/hyqerionmath/__init__.py
"""
HyqerionMath Package
A collection of mathematical utility functions, including primality tests,
factorization, and sequence generation.
"""
# Import functions from modules to make them available at the package level
from .primality import isprime, get_nth_prime, get_primes_in_index_range, find_primes_between
from .factorization import get_factors, get_prime_factorization
from .sequences import get_nth_fibonacci, get_fibonacci_in_index_range

# Define what 'from hyqerionmath import *' imports
__all__ = [
    # Primality
    'isprime',
    'get_nth_prime',
    'get_primes_in_index_range',
    'find_primes_between',
    # Factorization
    'get_factors',
    'get_prime_factorization',
    # Sequences
    'get_nth_fibonacci',
    'get_fibonacci_in_index_range',
]

# Define the package version (should match pyproject.toml)
# Increment minor version for new features
__version__ = "0.4.0"
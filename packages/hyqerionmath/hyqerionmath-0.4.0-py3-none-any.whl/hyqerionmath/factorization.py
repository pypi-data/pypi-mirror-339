# src/hyqerionmath/factorization.py
"""
Number factorization functions for HyqerionMath.
"""
import math
from typing import List

def get_factors(number: int) -> List[int]:
    """
    Finds all positive integer factors of a given number.

    For example:
    - get_factors(10) returns [1, 2, 5, 10]
    - get_factors(12) returns [1, 2, 3, 4, 6, 12]
    - get_factors(1) returns [1]

    Args:
        number: The integer for which to find factors (must be positive).

    Returns:
        A sorted list of all positive integer factors.

    Raises:
        TypeError: If the input is not an integer.
        ValueError: If the input number is not positive (<= 0).
    """
    if not isinstance(number, int):
        raise TypeError("Input must be an integer.")
    if number <= 0:
        raise ValueError("Input number must be positive.")

    factors = set()
    limit = int(math.sqrt(number)) + 1
    for i in range(1, limit):
        if number % i == 0:
            factors.add(i)
            factors.add(number // i)

    return sorted(list(factors))

def get_prime_factorization(number: int) -> List[int]:
    """
    Finds the prime factorization of a given integer greater than 1.

    For example:
    - get_prime_factorization(10) returns [2, 5]
    - get_prime_factorization(12) returns [2, 2, 3]
    - get_prime_factorization(2025) returns [3, 3, 3, 3, 5, 5]
    - get_prime_factorization(17) returns [17]

    Args:
        number: The integer to factorize (must be greater than 1).

    Returns:
        A sorted list of prime factors (including duplicates).

    Raises:
        TypeError: If the input is not an integer.
        ValueError: If the input number is not greater than 1.
    """
    if not isinstance(number, int):
        raise TypeError("Input must be an integer.")
    if number <= 1:
        raise ValueError("Input number must be greater than 1 for prime factorization.")

    prime_factors = []
    n = number # Work with a copy

    # Handle factor 2
    while n % 2 == 0:
        prime_factors.append(2)
        n //= 2

    # Handle odd factors
    # Iterate from 3 up to sqrt(n)
    limit = int(math.sqrt(n)) + 1
    i = 3
    while i <= limit: # Use <= because limit might be the sqrt
        while n % i == 0:
            prime_factors.append(i)
            n //= i
        # Re-calculate limit if n changed significantly (optimization, optional)
        # limit = int(math.sqrt(n)) + 1 # Uncomment if dealing with very large numbers
        i += 2 # Check next odd number

    # If n is still greater than 1 after the loop,
    # it means the remaining n is a prime factor itself (larger than sqrt(original n))
    if n > 1:
        prime_factors.append(n)

    return prime_factors # The list will be naturally sorted
# src/hyqerionmath/primality.py
"""
Primality test function module for HyperionMath.
"""
import math

def isprime(number: int) -> bool:
    """
    Checks if a given integer is a prime number.

    Args:
        number: The integer to check for primality.

    Returns:
        True if the number is prime, False otherwise.

    Raises:
        TypeError: If the input is not an integer.
    """
    if not isinstance(number, int):
        raise TypeError("Input must be an integer.")
    if number <= 1:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    limit = int(math.sqrt(number)) + 1
    for i in range(3, limit, 2):
        if number % i == 0:
            return False
    return True
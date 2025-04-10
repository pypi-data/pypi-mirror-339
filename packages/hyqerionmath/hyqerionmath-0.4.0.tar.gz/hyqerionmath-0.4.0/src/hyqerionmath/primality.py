# src/hyqerionmath/primality.py
"""
Primality test and prime generation functions for HyqerionMath.
"""
import math
from typing import List

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
    # Check only odd divisors up to the square root
    limit = int(math.sqrt(number)) + 1
    for i in range(3, limit, 2):
        if number % i == 0:
            return False
    return True

def get_nth_prime(n: int) -> int:
    """
    Finds the n-th prime number (1-based index).

    For example:
    - get_nth_prime(1) returns 2 (the first prime)
    - get_nth_prime(5) returns 11 (the fifth prime)

    Args:
        n: The index (position) of the desired prime number (must be a positive integer).

    Returns:
        The n-th prime number.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is not positive (<= 0).
    """
    if not isinstance(n, int):
        raise TypeError("Index 'n' must be an integer.")
    if n <= 0:
        raise ValueError("Index 'n' must be a positive integer.")

    count = 0
    num = 1
    while count < n:
        num += 1
        if isprime(num):
            count += 1
    return num

def get_primes_in_index_range(start_index: int, end_index: int) -> List[int]:
    """
    Finds prime numbers from the start_index-th prime to the end_index-th prime (inclusive).

    Indices are 1-based.

    For example:
    - get_primes_in_index_range(3, 6) returns [5, 7, 11, 13] (3rd to 6th primes)

    Args:
        start_index: The starting index (position) of the prime sequence (must be positive).
        end_index: The ending index (position) of the prime sequence (must be positive
                   and >= start_index).

    Returns:
        A list of prime numbers in the specified index range.

    Raises:
        TypeError: If start_index or end_index are not integers.
        ValueError: If start_index or end_index are not positive, or if
                    start_index > end_index.
    """
    if not isinstance(start_index, int) or not isinstance(end_index, int):
        raise TypeError("Start and end indices must be integers.")
    if start_index <= 0 or end_index <= 0:
        raise ValueError("Start and end indices must be positive integers.")
    if start_index > end_index:
        raise ValueError("Start index cannot be greater than end index.")

    primes_list = []
    count = 0
    num = 1
    while count < end_index:
        num += 1
        if isprime(num):
            count += 1
            if count >= start_index:
                primes_list.append(num)
    return primes_list

def find_primes_between(lower_bound: int, upper_bound: int) -> List[int]:
    """
    Finds all prime numbers within a given range [lower_bound, upper_bound] (inclusive).

    For example:
    - find_primes_between(10, 30) returns [11, 13, 17, 19, 23, 29]

    Args:
        lower_bound: The inclusive lower integer boundary of the range.
        upper_bound: The inclusive upper integer boundary of the range.

    Returns:
        A list of prime numbers found within the specified range.
        Returns an empty list if upper_bound < 2 or lower_bound > upper_bound.

    Raises:
        TypeError: If lower_bound or upper_bound are not integers.
        ValueError: If lower_bound > upper_bound (optional, could also return empty list).
                    Let's choose to return an empty list for simplicity here.
    """
    if not isinstance(lower_bound, int) or not isinstance(upper_bound, int):
        raise TypeError("Lower and upper bounds must be integers.")

    # Handle cases where no primes are possible or bounds are reversed
    if upper_bound < 2 or lower_bound > upper_bound:
        return []

    primes_list = []
    # Start checking from max(2, lower_bound) as numbers < 2 cannot be prime
    start = max(2, lower_bound)

    # Optimization: Handle 2 separately if it's in range
    if start <= 2 <= upper_bound:
        primes_list.append(2)

    # Start checking odd numbers from 3 or the next odd number >= start
    check_num = max(3, start)
    if check_num % 2 == 0: # Ensure we start with an odd number
        check_num += 1

    # Iterate only over odd numbers up to the upper bound
    while check_num <= upper_bound:
        if isprime(check_num):
            primes_list.append(check_num)
        check_num += 2 # Check next odd number

    return primes_list
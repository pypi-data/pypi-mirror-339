# src/hyqerionmath/sequences.py
"""
Sequence generation functions (like Fibonacci) for HyqerionMath.
"""
from typing import List

def get_nth_fibonacci(n: int) -> int:
    """
    Calculates the n-th Fibonacci number using 1-based indexing.

    The sequence is defined as F(1)=0, F(2)=1, F(3)=1, F(4)=2, F(5)=3, ...

    Args:
        n: The index (position) of the desired Fibonacci number (must be a positive integer).

    Returns:
        The n-th Fibonacci number.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is not positive (<= 0).
    """
    if not isinstance(n, int):
        raise TypeError("Index 'n' must be an integer.")
    if n <= 0:
        raise ValueError("Index 'n' must be a positive integer.")

    if n == 1:
        return 0
    if n == 2:
        return 1

    a, b = 0, 1
    # We need n-2 iterations after handling the first two cases
    for _ in range(n - 2):
        a, b = b, a + b
    return b

def get_fibonacci_in_index_range(start_index: int, end_index: int) -> List[int]:
    """
    Returns a list of Fibonacci numbers from the start_index-th to the
    end_index-th (inclusive), using 1-based indexing.

    The sequence is defined as F(1)=0, F(2)=1, F(3)=1, F(4)=2, F(5)=3, ...
    For example:
    - get_fibonacci_in_index_range(3, 6) returns [1, 2, 3, 5] (F(3) to F(6))

    Args:
        start_index: The starting index (position) of the Fibonacci sequence (must be positive).
        end_index: The ending index (position) of the Fibonacci sequence (must be positive
                   and >= start_index).

    Returns:
        A list of Fibonacci numbers in the specified index range.

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

    fib_list = []
    a, b = 0, 1

    for i in range(1, end_index + 1):
        current_fib = -1 # Placeholder

        if i == 1:
            current_fib = a
        elif i == 2:
            current_fib = b
        else: # i > 2
            # Calculate the next fib number (which corresponds to index i)
            a, b = b, a + b
            current_fib = b

        if i >= start_index:
            fib_list.append(current_fib)

    return fib_list
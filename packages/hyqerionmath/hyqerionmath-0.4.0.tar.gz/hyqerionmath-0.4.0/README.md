# HyqerionMath

[![PyPI version](https://badge.fury.io/py/hyqerionmath.svg)](https://badge.fury.io/py/hyqerionmath) <!-- Replace 'hyqerionmath' if your PyPI name is different -->
[![Python versions](https://img.shields.io/pypi/pyversions/hyqerionmath.svg)](https://pypi.org/project/hyqerionmath/) <!-- Replace 'hyqerionmath' if your PyPI name is different -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) <!-- Link assumes MIT License -->

A Python library providing supplementary mathematical utility functions, focusing on number theory aspects like prime numbers, factorization, and sequences.

## Overview

HyqerionMath aims to offer helpful, well-tested math functions that extend Python's built-in `math` module. It's designed to be simple, efficient, and easy to use.

## Features

HyqerionMath includes:

### Primality Functions (`primality.py`)

*   **`isprime(number: int) -> bool`**: Efficiently checks if a given integer `number` is a prime number. Returns `True` if prime, `False` otherwise. Raises `TypeError` for non-integer input.
*   **`get_nth_prime(n: int) -> int`**: Finds the *n*-th prime number (1-based index). e.g., `get_nth_prime(1)` is 2, `get_nth_prime(5)` is 11. Raises `TypeError` if `n` is not an integer, `ValueError` if `n` is not positive.
*   **`get_primes_in_index_range(start_index: int, end_index: int) -> List[int]`**: Returns a list containing primes from the `start_index`-th prime to the `end_index`-th prime (inclusive, 1-based). e.g., `get_primes_in_index_range(3, 6)` returns `[5, 7, 11, 13]`. Raises `TypeError` or `ValueError` for invalid indices.
*   **`find_primes_between(lower_bound: int, upper_bound: int) -> List[int]`**: Returns a sorted list of all prime numbers `p` such that `lower_bound <= p <= upper_bound`. e.g., `find_primes_between(10, 30)` returns `[11, 13, 17, 19, 23, 29]`. Raises `TypeError` for non-integer bounds. Returns an empty list if `upper_bound < 2` or `lower_bound > upper_bound`.

### Factorization Functions (`factorization.py`)

*   **`get_factors(number: int) -> List[int]`**: Finds all positive integer factors of a given `number`. e.g., `get_factors(12)` returns `[1, 2, 3, 4, 6, 12]`. Raises `TypeError` for non-integers, `ValueError` for non-positive input.
*   **`get_prime_factorization(number: int) -> List[int]`**: Returns a sorted list of the prime factors of `number` (including duplicates). e.g., `get_prime_factorization(20)` returns `[2, 2, 5]`. Raises `TypeError` for non-integers, `ValueError` if `number <= 1`.

### Sequence Functions (`sequences.py`)

*   **`get_nth_fibonacci(n: int) -> int`**: Calculates the *n*-th Fibonacci number using 1-based indexing (F(1)=0, F(2)=1, F(3)=1, F(4)=2...). e.g., `get_nth_fibonacci(5)` returns 3. Raises `TypeError` for non-integers, `ValueError` for non-positive `n`.
*   **`get_fibonacci_in_index_range(start_index: int, end_index: int) -> List[int]`**: Returns a list of Fibonacci numbers from the `start_index`-th to the `end_index`-th (inclusive, 1-based). e.g., `get_fibonacci_in_index_range(3, 6)` returns `[1, 2, 3, 5]`. Raises `TypeError` or `ValueError` for invalid indices.

*(More features may be added in the future!)*

## Installation

You can install HyqerionMath directly from PyPI (once published):

```bash
pip install hyqerionmath
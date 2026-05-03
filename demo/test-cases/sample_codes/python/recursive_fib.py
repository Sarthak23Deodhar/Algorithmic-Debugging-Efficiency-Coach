"""
Sample: Recursive Fibonacci with exponential complexity
This code has O(2^n) time complexity and can be optimized with memoization.
"""

def fibonacci_recursive(n):
    """
    Calculate nth Fibonacci number using naive recursion.
    Time Complexity: O(2^n) - exponential
    Space Complexity: O(n) - recursion stack
    """
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_optimized(n, memo=None):
    """
    Calculate nth Fibonacci number using memoization.
    Time Complexity: O(n) - linear
    Space Complexity: O(n) - memo dictionary
    """
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_optimized(n - 1, memo) + fibonacci_optimized(n - 2, memo)
    return memo[n]


def factorial_recursive(n):
    """
    Calculate factorial using recursion.
    Time Complexity: O(n)
    Space Complexity: O(n) - recursion stack
    """
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)


# Test the functions
if __name__ == "__main__":
    import time
    
    # Test recursive Fibonacci (slow for large n)
    n = 10
    start = time.time()
    result = fibonacci_recursive(n)
    elapsed = time.time() - start
    print(f"Recursive Fibonacci({n}) = {result}, Time: {elapsed:.6f}s")
    
    # Test optimized Fibonacci
    n = 30
    start = time.time()
    result = fibonacci_optimized(n)
    elapsed = time.time() - start
    print(f"Optimized Fibonacci({n}) = {result}, Time: {elapsed:.6f}s")
    
    # Test factorial
    result = factorial_recursive(5)
    print(f"Factorial(5) = {result}")

# Made with Bob

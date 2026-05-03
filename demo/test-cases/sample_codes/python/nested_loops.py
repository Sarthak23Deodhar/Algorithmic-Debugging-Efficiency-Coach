"""
Sample: Nested loops with O(n²) complexity
This code can be optimized using hash maps.
"""

def find_pair_sum(numbers, target):
    """Find two numbers that sum to target using nested loops."""
    n = len(numbers)
    
    # O(n²) approach - inefficient
    for i in range(n):
        for j in range(i + 1, n):
            if numbers[i] + numbers[j] == target:
                return (i, j, numbers[i], numbers[j])
    
    return None


def count_pairs_with_difference(numbers, k):
    """Count pairs with difference k using nested loops."""
    count = 0
    n = len(numbers)
    
    # O(n²) approach
    for i in range(n):
        for j in range(i + 1, n):
            if abs(numbers[i] - numbers[j]) == k:
                count += 1
    
    return count


# Test the functions
if __name__ == "__main__":
    nums = [2, 7, 11, 15, 3, 6]
    target = 9
    
    result = find_pair_sum(nums, target)
    if result:
        print(f"Pair found at indices {result[0]}, {result[1]}: {result[2]} + {result[3]} = {target}")
    
    pairs_count = count_pairs_with_difference(nums, 4)
    print(f"Number of pairs with difference 4: {pairs_count}")

# Made with Bob

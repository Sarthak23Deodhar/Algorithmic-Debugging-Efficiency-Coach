"""
Example: Optimized Python Code
This code demonstrates efficient implementations with O(n) time complexity.
"""

def find_pair_with_sum(numbers, target_sum):
    """
    Find if there exists a pair of numbers that sum to target_sum.
    Optimized complexity: O(n) - uses hash set
    """
    seen = set()
    
    for num in numbers:
        complement = target_sum - num
        if complement in seen:
            return True, (complement, num)
        seen.add(num)
    
    return False, None


def find_duplicates(numbers):
    """
    Find all duplicate numbers in a list.
    Optimized complexity: O(n) - uses set for tracking
    """
    seen = set()
    duplicates = set()
    
    for num in numbers:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)
    
    return list(duplicates)


def count_occurrences(numbers):
    """
    Count occurrences of each number.
    Optimized complexity: O(n) - single pass with dictionary
    """
    result = {}
    
    for num in numbers:
        result[num] = result.get(num, 0) + 1
    
    return result


def find_common_elements(list1, list2):
    """
    Find common elements between two lists.
    Optimized complexity: O(n+m) - uses set intersection
    """
    set1 = set(list1)
    set2 = set(list2)
    
    return list(set1 & set2)


def remove_duplicates(numbers):
    """
    Remove duplicates from a list while preserving order.
    Optimized complexity: O(n) - uses set for O(1) lookups
    """
    seen = set()
    result = []
    
    for num in numbers:
        if num not in seen:
            seen.add(num)
            result.append(num)
    
    return result


def find_max_subarray_sum(numbers):
    """
    Find maximum sum of contiguous subarray (Kadane's algorithm).
    Optimized complexity: O(n) - single pass
    """
    if not numbers:
        return 0
    
    max_sum = current_sum = numbers[0]
    
    for num in numbers[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    
    return max_sum


def two_sum_all_pairs(numbers, target_sum):
    """
    Find all pairs that sum to target_sum.
    Optimized complexity: O(n) - uses hash map
    """
    seen = {}
    pairs = []
    
    for i, num in enumerate(numbers):
        complement = target_sum - num
        if complement in seen:
            pairs.append((complement, num))
        seen[num] = i
    
    return pairs


# Test code
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5, 2, 3, 6, 7, 8, 9, 1]
    
    print("Pair with sum 10:", find_pair_with_sum(numbers, 10))
    print("Duplicates:", find_duplicates(numbers))
    print("Occurrences:", count_occurrences(numbers))
    
    list1 = [1, 2, 3, 4, 5]
    list2 = [4, 5, 6, 7, 8]
    print("Common elements:", find_common_elements(list1, list2))
    
    print("Remove duplicates:", remove_duplicates(numbers))
    print("Max subarray sum:", find_max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]))
    print("All pairs with sum 10:", two_sum_all_pairs(numbers, 10))

# Made with Bob

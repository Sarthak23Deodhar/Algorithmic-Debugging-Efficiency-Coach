"""
Example: Inefficient Python Code
This code has O(n²) time complexity and can be optimized to O(n).
"""

def find_pair_with_sum(numbers, target_sum):
    """
    Find if there exists a pair of numbers that sum to target_sum.
    Current complexity: O(n²) - uses nested loops
    Target complexity: O(n) - can use hash map
    """
    n = len(numbers)
    
    # Inefficient: Nested loops checking all pairs
    for i in range(n):
        for j in range(i + 1, n):
            if numbers[i] + numbers[j] == target_sum:
                return True, (numbers[i], numbers[j])
    
    return False, None


def find_duplicates(numbers):
    """
    Find all duplicate numbers in a list.
    Current complexity: O(n²) - nested loops
    Target complexity: O(n) - can use set or dictionary
    """
    duplicates = []
    
    # Inefficient: Checking each element against all others
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] == numbers[j] and numbers[i] not in duplicates:
                duplicates.append(numbers[i])
    
    return duplicates


def count_occurrences(numbers):
    """
    Count occurrences of each number.
    Current complexity: O(n²) - counting each element separately
    Target complexity: O(n) - can use Counter or dictionary
    """
    result = {}
    
    # Inefficient: Counting each unique number separately
    unique_numbers = []
    for num in numbers:
        if num not in unique_numbers:
            unique_numbers.append(num)
    
    for num in unique_numbers:
        count = 0
        for n in numbers:
            if n == num:
                count += 1
        result[num] = count
    
    return result


def find_common_elements(list1, list2):
    """
    Find common elements between two lists.
    Current complexity: O(n*m) - nested loops
    Target complexity: O(n+m) - can use set intersection
    """
    common = []
    
    # Inefficient: Checking each element of list1 against all of list2
    for item1 in list1:
        for item2 in list2:
            if item1 == item2 and item1 not in common:
                common.append(item1)
    
    return common


def remove_duplicates(numbers):
    """
    Remove duplicates from a list while preserving order.
    Current complexity: O(n²) - checking membership in list
    Target complexity: O(n) - can use set for tracking
    """
    result = []
    
    # Inefficient: Checking if element already in result list
    for num in numbers:
        if num not in result:  # O(n) operation inside O(n) loop
            result.append(num)
    
    return result


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

# Made with Bob

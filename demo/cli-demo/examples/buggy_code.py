"""
Example: Buggy Python Code
This code contains multiple bugs including syntax errors, logic errors, and runtime issues.
"""

def find_duplicates(numbers):
    """Find duplicate numbers in a list."""
    duplicates = []
    
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers))
            if numbers[i] == numbers[j]:
                duplicates.append(numbers[i])
    
    return duplicates


def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    total = 0
    for num in numbers:
        total += num
    
    # Bug: Division by zero if list is empty
    average = total / len(numbers)
    return average


def find_max_value(numbers):
    """Find the maximum value in a list."""
    max_val = numbers[0]
    
    # Bug: Off-by-one error
    for i in range(1, len(numbers) + 1):
        if numbers[i] > max_val:
            max_val = numbers[i]
    
    return max_val


def reverse_string(text):
    """Reverse a string."""
    reversed_text = ""
    
    # Bug: Incorrect range
    for i in range(len(text), 0):
        reversed_text += text[i]
    
    return reversed_text


# Test code with bugs
if __name__ == "__main__":
    numbers = [1, 2, 3, 2, 4, 3, 5]
    
    print("Duplicates:", find_duplicates(numbers))
    print("Average:", calculate_average(numbers))
    print("Max value:", find_max_value(numbers))
    print("Reversed:", reverse_string("hello"))

# Made with Bob

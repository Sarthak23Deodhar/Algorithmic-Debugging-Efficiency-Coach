"""
Optimization strategy recommender
"""

from typing import List, Dict
from ..models.response import OptimizationStrategy, InefficientPattern
from ..utils.logger import get_logger

logger = get_logger(__name__)


class Optimizer:
    """Recommends optimization strategies"""
    
    def __init__(self):
        self.strategy_templates = self._initialize_strategies()
    
    def recommend_strategies(
        self,
        current_time_complexity: str,
        patterns: List[InefficientPattern]
    ) -> List[OptimizationStrategy]:
        """
        Recommend optimization strategies based on complexity and patterns
        
        Args:
            current_time_complexity: Current time complexity notation
            patterns: List of detected inefficient patterns
            
        Returns:
            List of optimization strategies
        """
        strategies = []
        
        # Recommend based on patterns
        for pattern in patterns:
            strategy = self._get_strategy_for_pattern(pattern)
            if strategy and strategy not in strategies:
                strategies.append(strategy)
        
        # Recommend based on complexity
        if current_time_complexity in ['O(n²)', 'O(n³)']:
            # Suggest general optimization for polynomial complexity
            general_strategy = self._get_general_optimization_strategy(current_time_complexity)
            if general_strategy and general_strategy not in strategies:
                strategies.append(general_strategy)
        
        logger.info(f"Generated {len(strategies)} optimization strategies")
        
        return strategies
    
    def estimate_improvement(
        self,
        current_complexity: str,
        target_complexity: str
    ) -> Dict[str, str]:
        """
        Estimate performance improvement for different input sizes
        
        Args:
            current_complexity: Current complexity notation
            target_complexity: Target complexity notation
            
        Returns:
            Dictionary mapping input sizes to improvement estimates
        """
        improvements = {}
        
        # Define complexity growth rates
        complexity_values = {
            'O(1)': lambda n: 1,
            'O(log n)': lambda n: n.bit_length(),
            'O(n)': lambda n: n,
            'O(n log n)': lambda n: n * n.bit_length(),
            'O(n²)': lambda n: n * n,
            'O(n³)': lambda n: n * n * n,
            'O(2^n)': lambda n: 2 ** min(n, 20)  # Cap to prevent overflow
        }
        
        if current_complexity in complexity_values and target_complexity in complexity_values:
            current_func = complexity_values[current_complexity]
            target_func = complexity_values[target_complexity]
            
            for n in [100, 1000, 10000]:
                current_ops = current_func(n)
                target_ops = target_func(n)
                
                if target_ops > 0:
                    speedup = current_ops / target_ops
                    if speedup > 1:
                        improvements[f"n={n}"] = f"{speedup:.0f}x faster"
                    else:
                        improvements[f"n={n}"] = "Similar performance"
        
        return improvements
    
    def _initialize_strategies(self) -> Dict[str, OptimizationStrategy]:
        """Initialize optimization strategy templates"""
        return {
            'nested_loops': OptimizationStrategy(
                technique='Hash Map / Set',
                description='Replace nested loops with hash-based lookups for O(1) access time',
                steps=[
                    'Identify the inner loop operation (usually a search or comparison)',
                    'Create a hash map or set to store elements for O(1) lookup',
                    'Replace inner loop with hash map lookup',
                    'Reduce time complexity from O(n²) to O(n)'
                ],
                complexity_improvement='O(n²) → O(n)',
                code_example='''# Before: O(n²)
for i in range(len(arr)):
    for j in range(len(arr)):
        if arr[i] == arr[j]:
            # ...

# After: O(n)
seen = set()
for item in arr:
    if item in seen:
        # ...
    seen.add(item)'''
            ),
            'redundant_recursion': OptimizationStrategy(
                technique='Dynamic Programming (Memoization)',
                description='Cache recursive results to avoid redundant calculations',
                steps=[
                    'Add a cache dictionary to store computed results',
                    'Check cache before computing',
                    'Store result in cache after computing',
                    'Or use @lru_cache decorator in Python'
                ],
                complexity_improvement='O(2^n) → O(n)',
                code_example='''# Before: O(2^n)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# After: O(n)
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)'''
            ),
            'linear_search_in_loop': OptimizationStrategy(
                technique='Set/Dict for O(1) Lookups',
                description='Convert list to set for constant-time membership testing',
                steps=[
                    'Convert the search collection to a set before the loop',
                    'Use set membership testing (O(1)) instead of list search (O(n))',
                    'Maintain set if elements are added/removed'
                ],
                complexity_improvement='O(n²) → O(n)',
                code_example='''# Before: O(n²)
for item in list1:
    if item in list2:  # O(n) search
        # ...

# After: O(n)
set2 = set(list2)  # O(n) conversion
for item in list1:
    if item in set2:  # O(1) lookup
        # ...'''
            ),
            'string_concatenation_in_loop': OptimizationStrategy(
                technique='List Join Pattern',
                description='Use list to collect strings, then join once at the end',
                steps=[
                    'Create an empty list to collect string parts',
                    'Append strings to the list in the loop',
                    'Use str.join() to concatenate all parts at once',
                    'Reduces from O(n²) to O(n)'
                ],
                complexity_improvement='O(n²) → O(n)',
                code_example='''# Before: O(n²)
result = ""
for item in items:
    result += str(item)  # Creates new string each time

# After: O(n)
parts = []
for item in items:
    parts.append(str(item))
result = "".join(parts)'''
            ),
            'repeated_sorting': OptimizationStrategy(
                technique='Sort Once and Maintain Order',
                description='Sort data once and maintain sorted order, or use appropriate data structures',
                steps=[
                    'Sort the data once at the beginning',
                    'Use binary search for lookups (O(log n))',
                    'Or use a heap/priority queue for maintaining sorted order',
                    'Avoid re-sorting after each modification'
                ],
                complexity_improvement='O(n² log n) → O(n log n)',
                code_example='''# Before: Multiple sorts
for item in items:
    data.append(item)
    data.sort()  # O(n log n) each time

# After: Sort once or use heap
import heapq
heap = []
for item in items:
    heapq.heappush(heap, item)  # O(log n) each time'''
            ),
            'inefficient_list_operation': OptimizationStrategy(
                technique='Use Deque for Efficient Operations',
                description='Use collections.deque for O(1) operations at both ends',
                steps=[
                    'Import deque from collections',
                    'Replace list with deque',
                    'Use appendleft() and popleft() for O(1) operations',
                    'Convert back to list if needed'
                ],
                complexity_improvement='O(n²) → O(n)',
                code_example='''# Before: O(n) per operation
from collections import deque

# list.insert(0, x) is O(n)
for item in items:
    my_list.insert(0, item)

# After: O(1) per operation
my_deque = deque()
for item in items:
    my_deque.appendleft(item)  # O(1)'''
            )
        }
    
    def _get_strategy_for_pattern(self, pattern: InefficientPattern) -> OptimizationStrategy:
        """Get optimization strategy for a specific pattern"""
        return self.strategy_templates.get(pattern.pattern_type)
    
    def _get_general_optimization_strategy(self, complexity: str) -> OptimizationStrategy:
        """Get general optimization strategy for high complexity"""
        if complexity == 'O(n²)':
            return OptimizationStrategy(
                technique='Algorithmic Paradigm Selection',
                description='Consider using more efficient algorithmic approaches',
                steps=[
                    'Analyze if the problem has optimal substructure (Dynamic Programming)',
                    'Check if sorting the data first enables better algorithms',
                    'Consider using hash maps for O(1) lookups',
                    'Explore divide-and-conquer approaches',
                    'Use two-pointer technique for sorted arrays'
                ],
                complexity_improvement='O(n²) → O(n) or O(n log n)',
                code_example='''# Common patterns:
# 1. Two Sum: Use hash map instead of nested loops
# 2. Sliding Window: For subarray problems
# 3. Two Pointers: For sorted array problems
# 4. Binary Search: For search in sorted data'''
            )
        
        return None

# Made with Bob

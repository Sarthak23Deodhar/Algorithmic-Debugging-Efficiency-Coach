/**
 * Sample: C++ code with memory leak
 * This code demonstrates memory management issues.
 */

#include <iostream>
#include <vector>

class DataProcessor {
private:
    int* data;
    int size;

public:
    DataProcessor(int n) {
        size = n;
        data = new int[n];  // Allocate memory
        for (int i = 0; i < n; i++) {
            data[i] = i * 2;
        }
    }
    
    // Missing destructor - memory leak!
    // ~DataProcessor() {
    //     delete[] data;
    // }
    
    void process() {
        for (int i = 0; i < size; i++) {
            std::cout << data[i] << " ";
        }
        std::cout << std::endl;
    }
};

// Function with potential memory leak
int* createArray(int size) {
    int* arr = new int[size];
    for (int i = 0; i < size; i++) {
        arr[i] = i;
    }
    return arr;
    // Caller must remember to delete[]
}

// Function with dangling pointer
int* getDanglingPointer() {
    int localVar = 42;
    return &localVar;  // Returns address of local variable!
}

// Inefficient nested loops - O(n²)
void findPairs(std::vector<int>& nums, int target) {
    int n = nums.size();
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (nums[i] + nums[j] == target) {
                std::cout << "Pair: " << nums[i] << ", " << nums[j] << std::endl;
            }
        }
    }
}

int main() {
    // Memory leak - DataProcessor not properly cleaned up
    DataProcessor* processor = new DataProcessor(10);
    processor->process();
    // Missing: delete processor;
    
    // Memory leak - array not freed
    int* arr = createArray(100);
    // Missing: delete[] arr;
    
    // Inefficient algorithm
    std::vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    findPairs(numbers, 10);
    
    return 0;
}

// Made with Bob

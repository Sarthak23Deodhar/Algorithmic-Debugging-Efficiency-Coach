/**
 * Sample: Java code with inefficient sorting algorithm
 * This code demonstrates O(n²) bubble sort that can be optimized.
 */

import java.util.Arrays;

public class InefficientSort {
    
    /**
     * Bubble sort implementation - O(n²) time complexity
     * Can be optimized using built-in sort or better algorithms
     */
    public static void bubbleSort(int[] arr) {
        int n = arr.length;
        
        // Nested loops - O(n²)
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    // Swap elements
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
    }
    
    /**
     * Selection sort - also O(n²)
     */
    public static void selectionSort(int[] arr) {
        int n = arr.length;
        
        for (int i = 0; i < n - 1; i++) {
            int minIdx = i;
            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[minIdx]) {
                    minIdx = j;
                }
            }
            
            // Swap
            int temp = arr[minIdx];
            arr[minIdx] = arr[i];
            arr[i] = temp;
        }
    }
    
    /**
     * Inefficient search - O(n²) for multiple searches
     */
    public static boolean containsDuplicate(int[] arr) {
        int n = arr.length;
        
        // Nested loops to check for duplicates
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (arr[i] == arr[j]) {
                    return true;
                }
            }
        }
        return false;
    }
    
    /**
     * Inefficient way to find common elements - O(n*m)
     */
    public static int[] findCommonElements(int[] arr1, int[] arr2) {
        int[] temp = new int[Math.min(arr1.length, arr2.length)];
        int count = 0;
        
        // Nested loops - O(n*m)
        for (int i = 0; i < arr1.length; i++) {
            for (int j = 0; j < arr2.length; j++) {
                if (arr1[i] == arr2[j]) {
                    // Check if already added
                    boolean exists = false;
                    for (int k = 0; k < count; k++) {
                        if (temp[k] == arr1[i]) {
                            exists = true;
                            break;
                        }
                    }
                    if (!exists) {
                        temp[count++] = arr1[i];
                    }
                    break;
                }
            }
        }
        
        return Arrays.copyOf(temp, count);
    }
    
    /**
     * Inefficient string concatenation in loop
     */
    public static String concatenateStrings(String[] strings) {
        String result = "";
        
        // String concatenation in loop - inefficient
        // Should use StringBuilder
        for (String s : strings) {
            result += s;  // Creates new String object each time
        }
        
        return result;
    }
    
    public static void main(String[] args) {
        // Test bubble sort
        int[] numbers = {64, 34, 25, 12, 22, 11, 90};
        System.out.println("Original array: " + Arrays.toString(numbers));
        
        bubbleSort(numbers);
        System.out.println("Sorted array: " + Arrays.toString(numbers));
        
        // Test duplicate detection
        int[] withDuplicates = {1, 2, 3, 4, 2, 5};
        System.out.println("Contains duplicates: " + containsDuplicate(withDuplicates));
        
        // Test common elements
        int[] arr1 = {1, 2, 3, 4, 5};
        int[] arr2 = {4, 5, 6, 7, 8};
        int[] common = findCommonElements(arr1, arr2);
        System.out.println("Common elements: " + Arrays.toString(common));
        
        // Test string concatenation
        String[] words = {"Hello", " ", "World", "!"};
        String result = concatenateStrings(words);
        System.out.println("Concatenated: " + result);
    }
}

// Made with Bob

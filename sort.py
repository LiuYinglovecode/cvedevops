# get the n-largest values of an array using NumPy
import numpy as np

arr = np.array([2, 0, 1, 5, 4, 1, 9])

print("Given array:", arr)

sorted_index_array = np.argsort(arr)

sorted_array = arr[sorted_index_array]

print("Sorted array:", sorted_array)

n = 3 

res = sorted_array[-n : ]

print("{} largest value:".format(n),res)

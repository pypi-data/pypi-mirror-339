import numpy as np


def is_one_hot_encoded(arr):
    # Check if the array is one-hot encoded
    # Ensure the input is a numpy ndarray and is 2D
    if not isinstance(arr, np.ndarray):
        raise ValueError("Input must be a NumPy ndarray.")
    if not np.all(np.isin(arr, [0, 1])):
        return False
    # Check if each row (or column) has exactly one "1"
    return np.all(np.sum(arr, axis=1) == 1)  # For row-wise checking


def is_binary_encoded(arr):
    # Ensure the input is a numpy ndarray and is 2D
    if not isinstance(arr, np.ndarray):
        raise ValueError("Input must be a NumPy ndarray.")
    if arr.ndim != 2:
        raise ValueError("Input must be a 2D array.")

    # Check if all elements are either 0 or 1
    return np.all(np.isin(arr, [0, 1]))


def is_binary_vector(arr):
    # Ensure the input is a numpy ndarray and is 1D
    if not isinstance(arr, np.ndarray):
        raise ValueError("Input must be a NumPy ndarray.")
    if arr.ndim != 1:
        raise ValueError("Input must be a 1D array.")
    return arr.ndim == 1 and np.all(np.isin(arr, [0, 1]))


def is_label_encoded(arr):
    # Check if the array is label encoded
    # Ensure the input is a numpy ndarray and is 1D
    if not isinstance(arr, np.ndarray):
        raise ValueError("Input must be a NumPy ndarray.")
    if arr.ndim != 1:
        raise ValueError("Input must be a 1D array.")
    
    # Check if all values are non-negative integers (possible class labels)
    return np.issubdtype(arr.dtype, np.integer) and np.all(arr >= 0)
import numpy as np

def rotate(arr, steps=1):
    """
    Rotates a list or NumPy array by the specified number of steps.

    Args:
        arr (list or np.ndarray): The list or array to rotate.
        steps (int): Number of steps to rotate. Positive for right rotation, negative for left.

    Returns:
        list or np.ndarray: Rotated list or array.
    """
    if arr is None or arr.size == 0:
        return arr
    steps = -steps % len(arr)
    return np.concatenate((arr[steps:], arr[:steps])) if isinstance(arr, np.ndarray) else arr[steps:] + arr[:steps]

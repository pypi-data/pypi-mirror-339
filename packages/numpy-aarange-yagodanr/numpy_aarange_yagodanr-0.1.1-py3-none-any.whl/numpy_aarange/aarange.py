import numpy as np


def aarange(r: int, length: int):
    """
    creates matrix with size (r, length) with values from r to 1
    """
    arr = np.array([np.full(length, r-i) for i in range(r)])

    return arr

# print(aarange(4, 5))

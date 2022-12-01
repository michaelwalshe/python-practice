import time
import numpy as np
import itertools


# Need to calculate w/ pen&paper an optimal solution, naive will never work
def np_elder_age(m, n, l, t):
    arr1 = np.arange(m, dtype=np.int8).reshape((1, m))
    arr2 = np.arange(n, dtype=np.int8).reshape((n, 1))

    age_values = np.bitwise_xor(arr1, arr2) - l
    age_values[age_values < 0] = 0
    return age_values.sum() % t


def product_elder_age(m, n, l, t):
    # rect = ""
    tot = 0
    for i, j in itertools.product(range(m), range(n)):
        val = i ^ j - l
        if val > 0:
            tot = (tot % t) + (val % t)
    return tot % t


# m x n magic square
# Calculate seconds donated by XOR each index
def naive_elder_age(m, n, l, t):
    # rect = ""
    tot = 0
    for j in range(n):
        # row = ""
        for i in range(m):
            val = i ^ j - l
            if val > 0:
                tot = (tot % t) + (val % t)
                # tot += val
            # row += str(val)
        # rect += row + "\r\n"
    return tot % t


t = time.perf_counter()
age = naive_elder_age(8, 5, 1, 100)
# print(rect)
print(age)
print(time.perf_counter() - t)

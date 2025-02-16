import numpy as np
from random import randint


def generate_mines(x_size, y_size, num_mines):

    base_arr = np.zeros((x_size+2, y_size+2), dtype=np.uint8)

    for i in range(num_mines):
        x_rand = randint(1, x_size)
        y_rand = randint(1, y_size)
        base_arr[x_rand, y_rand] = 1
    return base_arr


def generate_hidden_numbers(base_arr, x_size, y_size):

    numbers = np.zeros((x_size+2, y_size+2), dtype=np.uint8)

    for i in range(1, x_size+1):
        for j in range(1, y_size+1):
            if base_arr[i, j]:
                continue
            else:
                numbers[i, j] = sum(sum(base_arr[i-1:i+2, j-1:j+2]))

    numbers = numbers[1:x_size+1, 1:y_size+1]
    return numbers

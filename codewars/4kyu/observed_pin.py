import itertools
from typing import Optional, List

import numpy as np


def try_index(arr: np.array, i: int, j: int) -> str:
    height, width = arr.shape

    if not (i >= 0 and i < height and j >= 0 and j < width):
        return ""

    try:
        return arr[i, j][0]
    except IndexError:
        return ""


def get_pins(observed: str, keypad: Optional[List[List[str]]] = None) -> List[str]:
    if not keypad:
        keypad = np.array(
            [
                ["1", "2", "3"],
                ["4", "5", "6"],
                ["7", "8", "9"],
                ["", "0", ""]
            ]
        )
    else:
        keypad = np.array(keypad)

    digits_alternatives = []
    for digit in observed:
        i, j = np.where(keypad == digit)
        digit_alt = (
            digit
            + try_index(keypad, i - 1, j)
            + try_index(keypad, i + 1, j)
            + try_index(keypad, i, j - 1)
            + try_index(keypad, i, j + 1)
        )

        digits_alternatives.append(digit_alt)

    possible_pins = ["".join(x) for x in itertools.product(*digits_alternatives)]

    return possible_pins

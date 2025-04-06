from typing import Any

def spread_jam(multiply: int, array: list[int]):
    newArray = array

    for i in range(0, len(array), 1):
        newArray[i] = array[i]*multiply

    return newArray

def add_jam(add: int, array: list[int]):
    newArray = array

    for i in range(0, len(array), 1):
        newArray[i] = array[i]+add

    return newArray
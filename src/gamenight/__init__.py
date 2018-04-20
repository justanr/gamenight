from typing import List

__version__ = '0.0.1'
__author__ = 'Alec Nikolas Reiter'
__email__ = 'alecreiter@gmail.com'


def is_odd(x: int) -> bool:
    return bool(x & 1)


def all_odd(*x: int) -> bool:
    """checks if all the ints are odd

    :param x: the ints
    """
    return all(is_odd(x) for x in x)


async def some_async_thingy(y: List[int]):
    """

    :param y: a thing
    """
    return 1

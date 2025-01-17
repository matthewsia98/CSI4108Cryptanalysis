import random
import textwrap


def itob(i: int) -> str:
    return format(i, "b")


def btoi(b: str) -> int:
    b = b.replace(" ", "", -1)
    return int(b, 2)


def itoh(i: int) -> str:
    return format(i, "X")


def htoi(h: str) -> int:
    return int(h, 16)


def btoh(b: str) -> str:
    b = b.replace(" ", "", -1)
    return format(int(b, 2), "X")


def htob(h: str) -> str:
    return format(int(h, 16), "b")


def random_bin(n: int) -> str:
    return format(random.getrandbits(n), "b")


def format_bin(b: str) -> str:
    b = b.replace(" ", "", -1)
    return " ".join(textwrap.wrap(b, 4))


def split_bin(b: str) -> list[str]:
    b = b.replace(" ", "", -1)
    return textwrap.wrap(b, 4)

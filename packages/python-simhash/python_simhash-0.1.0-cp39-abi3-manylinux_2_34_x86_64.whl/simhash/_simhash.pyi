from typing import Any, Literal, Protocol

Hasher = Literal[
    "default",
    "ahash",
    "xxh3",
    "metrohash",
]


class Hashable(Protocol):
    def __hash__(self) -> int:
        ...

    def __eq__(self, other: Any) -> bool:
        ...


def set_num_threads(num_threads: int) -> None:
    """
    Set the number of threads for parallel processing.

    :param num_threads: The number of threads to use.
    :type num_threads: int
    """
    ...


def hamming_distance(left: int, right: int) -> int:
    """
    Calculate the Hamming distance between two integers.

    :param left: The first integer.
    :type left: int
    :param right: The second integer.
    :type right: int
    :return: The Hamming distance between the two integers.
    :rtype: int
    """
    ...

def hamming_distance_parallel(left: list[int], right: list[int]) -> list[list[int]]:
    """
    Calculate the Hamming distance between two lists of integers in parallel.

    :param left: The first list of integers.
    :type left: list[int]
    :param right: The second list of integers.
    :type right: list[int]
    :return: A list of lists containing the Hamming distances.
    :rtype: list[list[int]]
    """
    ...

def simhash(features: list[Hashable], hasher: Hasher | None = None) -> int:
    """
    Calculate the SimHash fingerprint for a list of features.

    :param features: The list of features to hash.
    :type features: list[Hashable]
    :param hasher: The name of the hash function to use (default is None).
    :type hasher: str | None
    :return: The SimHash fingerprint as an integer.
    :rtype: int
    """
    ...


def simhash_parallel(
    features: list[list[Hashable]],
    hasher: Hasher | None = None
) -> list[int]:
    """
    Calculate the SimHash fingerprint for a list of features in parallel.

    :param features: A list of lists of features to hash.
    :type features: list[list[Hashable]]
    :param hasher: The name of the hash function to use (default is None).
    :type hasher: str | None
    :return: The SimHash fingerprints as integers.
    :rtype: list[int]
    """
    ...

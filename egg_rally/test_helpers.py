from math import isclose

import pytest

from egg_rally.helpers import Vector, CartesianPoint


def test_int_equality() -> None:
    for a in {-2_000_000_000, -1_000_000_000, 1, 0, 1, 1_000_000_000, 2_000_000_000}:
        for b in {-2_000_000_000, -1_000_000_000, 1, 0, 1, 1_000_000_000, 2_000_000_000}:
            for c in {-2_000_000_000, -1_000_000_000, 1, 0, 1, 1_000_000_000, 2_000_000_000}:
                for d in {-2_000_000_000, -1_000_000_000, 1, 0, 1, 1_000_000_000, 2_000_000_000}:
                    if a == c and b == d:
                        assert Vector(a, b) == Vector(c, d)
                    else:
                        assert not Vector(a, b) == Vector(c, d)


def test_int_vector_addition() -> None:
    assert Vector(0, 0) + Vector(0, 0) == Vector(0, 0)
    assert Vector(1, 1) + Vector(0, 0) == Vector(1, 1)
    assert Vector(0, 1) + Vector(0, 0) == Vector(0, 1)
    assert Vector(1, 0) + Vector(0, 0) == Vector(1, 0)
    assert Vector(0, 0) + Vector(1, 1) == Vector(1, 1)
    assert Vector(0, 0) + Vector(0, 1) == Vector(0, 1)
    assert Vector(0, 0) + Vector(1, 0) == Vector(1, 0)
    assert Vector(1, 1) + Vector(1, 1) == Vector(2, 2)
    assert Vector(1, 0) + Vector(1, 1) == Vector(2, 1)
    assert Vector(0, 1) + Vector(1, 1) == Vector(1, 2)
    assert Vector(1, 1) + Vector(1, 0) == Vector(2, 1)
    assert Vector(1, 1) + Vector(0, 1) == Vector(1, 2)

    assert Vector(-1, -1) + Vector(0, 0) == Vector(-1, -1)
    assert Vector(0, -1) + Vector(0, 0) == Vector(0, -1)
    assert Vector(-1, 0) + Vector(0, 0) == Vector(-1, 0)
    assert Vector(0, 0) + Vector(-1, -1) == Vector(-1, -1)
    assert Vector(0, 0) + Vector(0, -1) == Vector(0, -1)
    assert Vector(0, 0) + Vector(-1, 0) == Vector(-1, 0)
    assert Vector(-1, -1) + Vector(-1, -1) == Vector(-2, -2)
    assert Vector(-1, 0) + Vector(-1, -1) == Vector(-2, -1)
    assert Vector(0, -1) + Vector(-1, -1) == Vector(-1, -2)
    assert Vector(-1, -1) + Vector(-1, 0) == Vector(-2, -1)
    assert Vector(-1, -1) + Vector(0, -1) == Vector(-1, -2)

    assert Vector(0, 0) + Vector(-1, -1) == Vector(-1, -1)
    assert Vector(0, 0) + Vector(0, -1) == Vector(0, -1)
    assert Vector(0, 0) + Vector(-1, 0) == Vector(-1, 0)
    assert Vector(1, 1) + Vector(-1, -1) == Vector(0, 0)
    assert Vector(1, 0) + Vector(-1, -1) == Vector(0, -1)
    assert Vector(0, 1) + Vector(-1, -1) == Vector(-1, 0)
    assert Vector(1, 1) + Vector(-1, 0) == Vector(0, 1)
    assert Vector(1, 1) + Vector(0, -1) == Vector(1, 0)

    assert Vector(-1, -1) + Vector(0, 0) == Vector(-1, -1)
    assert Vector(0, -1) + Vector(0, 0) == Vector(0, -1)
    assert Vector(-1, 0) + Vector(0, 0) == Vector(-1, 0)
    assert Vector(-1, -1) + Vector(1, 1) == Vector(0, 0)
    assert Vector(-1, -1) + Vector(1, 0) == Vector(0, -1)
    assert Vector(-1, -1) + Vector(0, 1) == Vector(-1, 0)
    assert Vector(-1, 0) + Vector(1, 1) == Vector(0, 1)
    assert Vector(0, -1) + Vector(1, 1) == Vector(1, 0)

    assert Vector(0, 0) + Vector(0, 0) == Vector(0, 0)
    assert Vector(1_000_000_000_000, 1_000_000_000_000) + \
        Vector(0, 0) == Vector(1_000_000_000_000, 1_000_000_000_000)
    assert Vector(0, 1_000_000_000_000) + \
        Vector(0, 0) == Vector(0, 1_000_000_000_000)
    assert Vector(1_000_000_000_000, 0) + \
        Vector(0, 0) == Vector(1_000_000_000_000, 0)
    assert Vector(0, 0) + Vector(1_000_000_000_000,
                                 1_000_000_000_000) == Vector(1_000_000_000_000, 1_000_000_000_000)
    assert Vector(0, 0) + \
        Vector(0, 1_000_000_000_000) == Vector(0, 1_000_000_000_000)
    assert Vector(0, 0) + Vector(1_000_000_000_000,
                                 0) == Vector(1_000_000_000_000, 0)
    assert Vector(1_000_000_000_000, 1_000_000_000_000) + Vector(1_000_000_000_000,
                                                                 1_000_000_000_000) == Vector(2_000_000_000_000, 2_000_000_000_000)
    assert Vector(1_000_000_000_000, 0) + Vector(1_000_000_000_000,
                                                 1_000_000_000_000) == Vector(2_000_000_000_000, 1_000_000_000_000)
    assert Vector(0, 1_000_000_000_000) + Vector(1_000_000_000_000,
                                                 1_000_000_000_000) == Vector(1_000_000_000_000, 2_000_000_000_000)
    assert Vector(1_000_000_000_000, 1_000_000_000_000) + \
        Vector(1_000_000_000_000, 0) == Vector(
            2_000_000_000_000, 1_000_000_000_000)
    assert Vector(1_000_000_000_000, 1_000_000_000_000) + Vector(0,
                                                                 1_000_000_000_000) == Vector(1_000_000_000_000, 2_000_000_000_000)

    assert Vector(-1_000_000_000_000, -1_000_000_000_000) + \
        Vector(0, 0) == Vector(-1_000_000_000_000, -1_000_000_000_000)
    assert Vector(0, -1_000_000_000_000) + \
        Vector(0, 0) == Vector(0, -1_000_000_000_000)
    assert Vector(-1_000_000_000_000, 0) + \
        Vector(0, 0) == Vector(-1_000_000_000_000, 0)
    assert Vector(0, 0) + Vector(-1_000_000_000_000, -
                                 1_000_000_000_000) == Vector(-1_000_000_000_000, -1_000_000_000_000)
    assert Vector(0, 0) + Vector(0, -
                                 1_000_000_000_000) == Vector(0, -1_000_000_000_000)
    assert Vector(0, 0) + Vector(-1_000_000_000_000,
                                 0) == Vector(-1_000_000_000_000, 0)
    assert Vector(-1_000_000_000_000, -1_000_000_000_000) + Vector(-1_000_000_000_000, -
                                                                   1_000_000_000_000) == Vector(-2_000_000_000_000, -2_000_000_000_000)
    assert Vector(-1_000_000_000_000, 0) + Vector(-1_000_000_000_000, -
                                                  1_000_000_000_000) == Vector(-2_000_000_000_000, -1_000_000_000_000)
    assert Vector(0, -1_000_000_000_000) + Vector(-1_000_000_000_000, -
                                                  1_000_000_000_000) == Vector(-1_000_000_000_000, -2_000_000_000_000)
    assert Vector(-1_000_000_000_000, -1_000_000_000_000) + \
        Vector(-1_000_000_000_000,
               0) == Vector(-2_000_000_000_000, -1_000_000_000_000)
    assert Vector(-1_000_000_000_000, -1_000_000_000_000) + Vector(0, -
                                                                   1_000_000_000_000) == Vector(-1_000_000_000_000, -2_000_000_000_000)

    assert Vector(0, 0) + Vector(-1_000_000_000_000, -
                                 1_000_000_000_000) == Vector(-1_000_000_000_000, -1_000_000_000_000)
    assert Vector(0, 0) + Vector(0, -
                                 1_000_000_000_000) == Vector(0, -1_000_000_000_000)
    assert Vector(0, 0) + Vector(-1_000_000_000_000,
                                 0) == Vector(-1_000_000_000_000, 0)
    assert Vector(1_000_000_000_000, 1_000_000_000_000) + \
        Vector(-1_000_000_000_000, -1_000_000_000_000) == Vector(0, 0)
    assert Vector(1_000_000_000_000, 0) + Vector(-1_000_000_000_000, -
                                                 1_000_000_000_000) == Vector(0, -1_000_000_000_000)
    assert Vector(0, 1_000_000_000_000) + Vector(-1_000_000_000_000, -
                                                 1_000_000_000_000) == Vector(-1_000_000_000_000, 0)
    assert Vector(1_000_000_000_000, 1_000_000_000_000) + \
        Vector(-1_000_000_000_000, 0) == Vector(0, 1_000_000_000_000)
    assert Vector(1_000_000_000_000, 1_000_000_000_000) + \
        Vector(0, -1_000_000_000_000) == Vector(1_000_000_000_000, 0)

    assert Vector(-1_000_000_000_000, -1_000_000_000_000) + \
        Vector(0, 0) == Vector(-1_000_000_000_000, -1_000_000_000_000)
    assert Vector(0, -1_000_000_000_000) + \
        Vector(0, 0) == Vector(0, -1_000_000_000_000)
    assert Vector(-1_000_000_000_000, 0) + \
        Vector(0, 0) == Vector(-1_000_000_000_000, 0)
    assert Vector(-1_000_000_000_000, -1_000_000_000_000) + \
        Vector(1_000_000_000_000, 1_000_000_000_000) == Vector(0, 0)
    assert Vector(-1_000_000_000_000, -1_000_000_000_000) + \
        Vector(1_000_000_000_000, 0) == Vector(0, -1_000_000_000_000)
    assert Vector(-1_000_000_000_000, -1_000_000_000_000) + \
        Vector(0, 1_000_000_000_000) == Vector(-1_000_000_000_000, 0)
    assert Vector(-1_000_000_000_000, 0) + Vector(1_000_000_000_000,
                                                  1_000_000_000_000) == Vector(0, 1_000_000_000_000)
    assert Vector(0, -1_000_000_000_000) + Vector(1_000_000_000_000,
                                                  1_000_000_000_000) == Vector(1_000_000_000_000, 0)


def test_int_vector_subtraction() -> None:
    assert Vector(0, 0) - Vector(0, 0) == Vector(0, 0)
    assert Vector(1, 1) - Vector(0, 0) == Vector(1, 1)
    assert Vector(0, 1) - Vector(0, 0) == Vector(0, 1)
    assert Vector(1, 0) - Vector(0, 0) == Vector(1, 0)
    assert Vector(0, 0) - Vector(1, 1) == Vector(-1, -1)
    assert Vector(0, 0) - Vector(0, 1) == Vector(0, -1)
    assert Vector(0, 0) - Vector(1, 0) == Vector(-1, 0)
    assert Vector(1, 1) - Vector(1, 1) == Vector(0, 0)
    assert Vector(1, 0) - Vector(1, 1) == Vector(0, -1)
    assert Vector(0, 1) - Vector(1, 1) == Vector(-1, 0)
    assert Vector(1, 1) - Vector(1, 0) == Vector(0, 1)
    assert Vector(1, 1) - Vector(0, 1) == Vector(1, 0)

    assert Vector(-1, -1) - Vector(0, 0) == Vector(-1, -1)
    assert Vector(0, -1) - Vector(0, 0) == Vector(0, -1)
    assert Vector(-1, 0) - Vector(0, 0) == Vector(-1, 0)
    assert Vector(0, 0) - Vector(-1, -1) == Vector(1, 1)
    assert Vector(0, 0) - Vector(0, -1) == Vector(0, 1)
    assert Vector(0, 0) - Vector(-1, 0) == Vector(1, 0)
    assert Vector(-1, -1) - Vector(-1, -1) == Vector(0, 0)
    assert Vector(-1, 0) - Vector(-1, -1) == Vector(0, 1)
    assert Vector(0, -1) - Vector(-1, -1) == Vector(1, 0)
    assert Vector(-1, -1) - Vector(-1, 0) == Vector(0, -1)
    assert Vector(-1, -1) - Vector(0, -1) == Vector(-1, 0)

    assert Vector(0, 0) - Vector(-1, -1) == Vector(1, 1)
    assert Vector(0, 0) - Vector(0, -1) == Vector(0, 1)
    assert Vector(0, 0) - Vector(-1, 0) == Vector(1, 0)
    assert Vector(1, 1) - Vector(-1, -1) == Vector(2, 2)
    assert Vector(1, 0) - Vector(-1, -1) == Vector(2, 1)
    assert Vector(0, 1) - Vector(-1, -1) == Vector(1, 2)
    assert Vector(1, 1) - Vector(-1, 0) == Vector(2, 1)
    assert Vector(1, 1) - Vector(0, -1) == Vector(1, 2)

    assert Vector(-1, -1) - Vector(0, 0) == Vector(-1, -1)
    assert Vector(0, -1) - Vector(0, 0) == Vector(0, -1)
    assert Vector(-1, 0) - Vector(0, 0) == Vector(-1, 0)
    assert Vector(-1, -1) - Vector(1, 1) == Vector(-2, -2)
    assert Vector(-1, -1) - Vector(1, 0) == Vector(-2, -1)
    assert Vector(-1, -1) - Vector(0, 1) == Vector(-1, -2)
    assert Vector(-1, 0) - Vector(1, 1) == Vector(-2, -1)
    assert Vector(0, -1) - Vector(1, 1) == Vector(-1, -2)

    assert Vector(0, 0) - Vector(0, 0) == Vector(0, 0)
    assert Vector(1_000_000_000_000, 1_000_000_000_000) - \
        Vector(0, 0) == Vector(1_000_000_000_000, 1_000_000_000_000)
    assert Vector(0, 1_000_000_000_000) - \
        Vector(0, 0) == Vector(0, 1_000_000_000_000)
    assert Vector(1_000_000_000_000, 0) - \
        Vector(0, 0) == Vector(1_000_000_000_000, 0)
    assert Vector(0, 0) - Vector(1_000_000_000_000,
                                 1_000_000_000_000) == Vector(-1_000_000_000_000, -1_000_000_000_000)
    assert Vector(0, 0) - \
        Vector(0, 1_000_000_000_000) == Vector(0, -1_000_000_000_000)
    assert Vector(0, 0) - Vector(1_000_000_000_000,
                                 0) == Vector(-1_000_000_000_000, 0)
    assert Vector(1_000_000_000_000, 1_000_000_000_000) - \
        Vector(1_000_000_000_000, 1_000_000_000_000) == Vector(0, 0)
    assert Vector(1_000_000_000_000, 0) - Vector(1_000_000_000_000,
                                                 1_000_000_000_000) == Vector(0, -1_000_000_000_000)
    assert Vector(0, 1_000_000_000_000) - Vector(1_000_000_000_000,
                                                 1_000_000_000_000) == Vector(-1_000_000_000_000, 0)
    assert Vector(1_000_000_000_000, 1_000_000_000_000) - \
        Vector(1_000_000_000_000, 0) == Vector(0, 1_000_000_000_000)
    assert Vector(1_000_000_000_000, 1_000_000_000_000) - \
        Vector(0, 1_000_000_000_000) == Vector(1_000_000_000_000, 0)

    assert Vector(-1_000_000_000_000, -1_000_000_000_000) - \
        Vector(0, 0) == Vector(-1_000_000_000_000, -1_000_000_000_000)
    assert Vector(0, -1_000_000_000_000) - \
        Vector(0, 0) == Vector(0, -1_000_000_000_000)
    assert Vector(-1_000_000_000_000, 0) - \
        Vector(0, 0) == Vector(-1_000_000_000_000, 0)
    assert Vector(0, 0) - Vector(-1_000_000_000_000, -
                                 1_000_000_000_000) == Vector(1_000_000_000_000, 1_000_000_000_000)
    assert Vector(0, 0) - Vector(0, -
                                 1_000_000_000_000) == Vector(0, 1_000_000_000_000)
    assert Vector(0, 0) - Vector(-1_000_000_000_000,
                                 0) == Vector(1_000_000_000_000, 0)
    assert Vector(-1_000_000_000_000, -1_000_000_000_000) - \
        Vector(-1_000_000_000_000, -1_000_000_000_000) == Vector(0, 0)
    assert Vector(-1_000_000_000_000, 0) - Vector(-1_000_000_000_000, -
                                                  1_000_000_000_000) == Vector(0, 1_000_000_000_000)
    assert Vector(0, -1_000_000_000_000) - Vector(-1_000_000_000_000, -
                                                  1_000_000_000_000) == Vector(1_000_000_000_000, 0)
    assert Vector(-1_000_000_000_000, -1_000_000_000_000) - \
        Vector(-1_000_000_000_000, 0) == Vector(0, -1_000_000_000_000)
    assert Vector(-1_000_000_000_000, -1_000_000_000_000) - \
        Vector(0, -1_000_000_000_000) == Vector(-1_000_000_000_000, 0)

    assert Vector(0, 0) - Vector(-1_000_000_000_000, -
                                 1_000_000_000_000) == Vector(1_000_000_000_000, 1_000_000_000_000)
    assert Vector(0, 0) - Vector(0, -
                                 1_000_000_000_000) == Vector(0, 1_000_000_000_000)
    assert Vector(0, 0) - Vector(-1_000_000_000_000,
                                 0) == Vector(1_000_000_000_000, 0)
    assert Vector(1_000_000_000_000, 1_000_000_000_000) - Vector(-1_000_000_000_000, -
                                                                 1_000_000_000_000) == Vector(2_000_000_000_000, 2_000_000_000_000)
    assert Vector(1_000_000_000_000, 0) - Vector(-1_000_000_000_000, -
                                                 1_000_000_000_000) == Vector(2_000_000_000_000, 1_000_000_000_000)
    assert Vector(0, 1_000_000_000_000) - Vector(-1_000_000_000_000, -
                                                 1_000_000_000_000) == Vector(1_000_000_000_000, 2_000_000_000_000)
    assert Vector(1_000_000_000_000, 1_000_000_000_000) - \
        Vector(-1_000_000_000_000,
               0) == Vector(2_000_000_000_000, 1_000_000_000_000)
    assert Vector(1_000_000_000_000, 1_000_000_000_000) - Vector(0, -
                                                                 1_000_000_000_000) == Vector(1_000_000_000_000, 2_000_000_000_000)

    assert Vector(-1_000_000_000_000, -1_000_000_000_000) - \
        Vector(0, 0) == Vector(-1_000_000_000_000, -1_000_000_000_000)
    assert Vector(0, -1_000_000_000_000) - \
        Vector(0, 0) == Vector(0, -1_000_000_000_000)
    assert Vector(-1_000_000_000_000, 0) - \
        Vector(0, 0) == Vector(-1_000_000_000_000, 0)
    assert Vector(-1_000_000_000_000, -1_000_000_000_000) - Vector(1_000_000_000_000,
                                                                   1_000_000_000_000) == Vector(-2_000_000_000_000, -2_000_000_000_000)
    assert Vector(-1_000_000_000_000, -1_000_000_000_000) - \
        Vector(1_000_000_000_000,
               0) == Vector(-2_000_000_000_000, -1_000_000_000_000)
    assert Vector(-1_000_000_000_000, -1_000_000_000_000) - Vector(0,
                                                                   1_000_000_000_000) == Vector(-1_000_000_000_000, -2_000_000_000_000)
    assert Vector(-1_000_000_000_000, 0) - Vector(1_000_000_000_000,
                                                  1_000_000_000_000) == Vector(-2_000_000_000_000, -1_000_000_000_000)
    assert Vector(0, -1_000_000_000_000) - Vector(1_000_000_000_000,
                                                  1_000_000_000_000) == Vector(-1_000_000_000_000, -2_000_000_000_000)


def test_int_vector_constant_multiplication() -> None:
    assert Vector(0, 0) * 0 == Vector(0, 0)
    assert Vector(1, 1) * 0 == Vector(0, 0)
    assert Vector(1, 0) * 0 == Vector(0, 0)
    assert Vector(0, 1) * 0 == Vector(0, 0)
    assert Vector(0, 0) * 1 == Vector(0, 0)
    assert Vector(1, 1) * 1 == Vector(1, 1)
    assert Vector(1, 0) * 1 == Vector(1, 0)
    assert Vector(0, 1) * 1 == Vector(0, 1)
    assert Vector(0, 0) * 2 == Vector(0, 0)
    assert Vector(2, 2) * 2 == Vector(4, 4)
    assert Vector(2, 0) * 2 == Vector(4, 0)
    assert Vector(0, 2) * 2 == Vector(0, 4)
    assert Vector(0, 0) * 1_000_000 == Vector(0, 0)
    assert Vector(1_000_000, 1_000_000) * \
        1_000_000 == Vector(1_000_000_000_000, 1_000_000_000_000)
    assert Vector(1_000_000, 0) * 1_000_000 == Vector(1_000_000_000_000, 0)
    assert Vector(0, 1_000_000) * 1_000_000 == Vector(0, 1_000_000_000_000)
    assert Vector(0, 0) * 2_000_000 == Vector(0, 0)
    assert Vector(2_000_000, 2_000_000) * \
        2_000_000 == Vector(4_000_000_000_000, 4_000_000_000_000)
    assert Vector(2_000_000, 0) * 2_000_000 == Vector(4_000_000_000_000, 0)
    assert Vector(0, 2_000_000) * 2_000_000 == Vector(0, 4_000_000_000_000)


def test_int_constant_division() -> None:
    with pytest.raises(ZeroDivisionError):
        Vector(0, 0) / 0

    with pytest.raises(ZeroDivisionError):
        Vector(1, 1) / 0

    with pytest.raises(ZeroDivisionError):
        Vector(1, 0) / 0

    with pytest.raises(ZeroDivisionError):
        Vector(0, 1) / 0

    assert Vector(0, 0) / 1 == Vector(0, 0)
    assert Vector(1, 1) / 1 == Vector(1, 1)
    assert Vector(1, 0) / 1 == Vector(1, 0)
    assert Vector(0, 1) / 1 == Vector(0, 1)
    assert Vector(0, 0) / 2 == Vector(0, 0)
    assert Vector(2, 2) / 2 == Vector(1, 1)
    assert Vector(2, 0) / 2 == Vector(1, 0)
    assert Vector(0, 2) / 2 == Vector(0, 1)
    assert Vector(0, 0) / 1_000_000 == Vector(0, 0)
    assert Vector(1_000_000, 1_000_000) / \
        1_000_000 == Vector(1, 1)
    assert Vector(1_000_000, 0) / 1_000_000 == Vector(1, 0)
    assert Vector(0, 1_000_000) / 1_000_000 == Vector(0, 1)
    assert Vector(0, 0) / 2_000_000 == Vector(0, 0)
    assert Vector(4_000_000, 4_000_000) / \
        2_000_000 == Vector(2, 2)
    assert Vector(4_000_000, 0) / 2_000_000 == Vector(2, 0)
    assert Vector(0, 4_000_000) / 2_000_000 == Vector(0, 2)


def test_int_magnitude() -> None:
    assert abs(Vector(5, 12)) == 13
    assert abs(Vector(12, 16)) == 20
    assert abs(Vector(21, 20)) == 29
    assert abs(Vector(32, 24)) == 40
    assert abs(Vector(45, 28)) == 53
    assert abs(Vector(60, 32)) == 68
    assert abs(Vector(77, 36)) == 85
    assert abs(Vector(96, 40)) == 104
    assert abs(Vector(117, 44)) == 125
    assert abs(Vector(140, 48)) == 148
    assert abs(Vector(165, 52)) == 173
    assert abs(Vector(192, 56)) == 200
    assert abs(Vector(7, 24)) == 25
    assert abs(Vector(16, 30)) == 34
    assert abs(Vector(27, 36)) == 45
    assert abs(Vector(40, 42)) == 58
    assert abs(Vector(55, 48)) == 73
    assert abs(Vector(72, 54)) == 90
    assert abs(Vector(91, 60)) == 109
    assert abs(Vector(112, 66)) == 130
    assert abs(Vector(135, 72)) == 153
    assert abs(Vector(160, 78)) == 178
    assert abs(Vector(187, 84)) == 205
    assert abs(Vector(9, 40)) == 41
    assert abs(Vector(20, 48)) == 52
    assert abs(Vector(33, 56)) == 65
    assert abs(Vector(48, 64)) == 80
    assert abs(Vector(65, 72)) == 97
    assert abs(Vector(84, 80)) == 116
    assert abs(Vector(105, 88)) == 137
    assert abs(Vector(128, 96)) == 160
    assert abs(Vector(153, 104)) == 185
    assert abs(Vector(180, 112)) == 212
    assert abs(Vector(11, 60)) == 61
    assert abs(Vector(24, 70)) == 74
    assert abs(Vector(39, 80)) == 89
    assert abs(Vector(56, 90)) == 106
    assert abs(Vector(75, 100)) == 125
    assert abs(Vector(96, 110)) == 146
    assert abs(Vector(119, 120)) == 169
    assert abs(Vector(144, 130)) == 194
    assert abs(Vector(171, 140)) == 221
    assert abs(Vector(13, 84)) == 85
    assert abs(Vector(28, 96)) == 100
    assert abs(Vector(45, 108)) == 117
    assert abs(Vector(64, 120)) == 136
    assert abs(Vector(85, 132)) == 157
    assert abs(Vector(108, 144)) == 180
    assert abs(Vector(133, 156)) == 205
    assert abs(Vector(160, 168)) == 232
    assert abs(Vector(15, 112)) == 113
    assert abs(Vector(32, 126)) == 130
    assert abs(Vector(51, 140)) == 149
    assert abs(Vector(72, 154)) == 170
    assert abs(Vector(95, 168)) == 193
    assert abs(Vector(120, 182)) == 218
    assert abs(Vector(147, 196)) == 245
    assert abs(Vector(17, 144)) == 145
    assert abs(Vector(36, 160)) == 164
    assert abs(Vector(57, 176)) == 185
    assert abs(Vector(80, 192)) == 208
    assert abs(Vector(105, 208)) == 233
    assert abs(Vector(132, 224)) == 260
    assert abs(Vector(19, 180)) == 181
    assert abs(Vector(40, 198)) == 202
    assert abs(Vector(63, 216)) == 225
    assert abs(Vector(88, 234)) == 250
    assert abs(Vector(115, 252)) == 277
    assert abs(Vector(21, 220)) == 221
    assert abs(Vector(44, 240)) == 244
    assert abs(Vector(69, 260)) == 269
    assert abs(Vector(96, 280)) == 296
    assert abs(Vector(23, 264)) == 265
    assert abs(Vector(48, 286)) == 290
    assert abs(Vector(75, 308)) == 317
    assert abs(Vector(25, 312)) == 313
    assert abs(Vector(52, 336)) == 340
    assert abs(Vector(27, 364)) == 365


def test_float_vector_addition() -> None:
    for a in {-0.2, 0.1, 0, 0.1, 0.2}:
        for b in {-0.2, 0.1, 0, 0.1, 0.2}:
            for c in {-0.2, 0.1, 0, 0.1, 0.2}:
                for d in {-0.2, 0.1, 0, 0.1, 0.2}:
                    sum_vector = Vector(a, b) + Vector(c, d)
                    assert isclose(sum_vector.x_hat, a + c) and isclose(
                        sum_vector.y_hat, b + d)


def test_float_vector_subtraction() -> None:
    for a in {-0.2, 0.1, 0, 0.1, 0.2}:
        for b in {-0.2, 0.1, 0, 0.1, 0.2}:
            for c in {-0.2, 0.1, 0, 0.1, 0.2}:
                for d in {-0.2, 0.1, 0, 0.1, 0.2}:
                    sum_vector = Vector(a, b) - Vector(c, d)
                    assert isclose(sum_vector.x_hat, a - c) and isclose(
                        sum_vector.y_hat, b - d)


def test_float_vector_constant_multiplication() -> None:
    for a in {-0.2, 0.1, 0, 0.1, 0.2}:
        for b in {-0.2, 0.1, 0, 0.1, 0.2}:
            for c in {-0.2, 0.1, 0, 0.1, 0.2}:
                mult_vector = Vector(a, b) * c
                assert isclose(mult_vector.x_hat, a * c) and isclose(
                    mult_vector.y_hat, b * c)


def test_float_vector_constant_division() -> None:
    for a in {-0.2, 0.1, 0, 0.1, 0.2}:
        for b in {-0.2, 0.1, 0, 0.1, 0.2}:
            for c in {-0.2, 0.1, 0, 0.1, 0.2}:
                if c == 0:
                    with pytest.raises(ZeroDivisionError):
                        Vector(a, b) / c
                else:
                    mult_vector = Vector(a, b) / c
                    assert isclose(mult_vector.x_hat, a / c) and isclose(
                        mult_vector.y_hat, b / c)


def test_float_magnitude() -> None:
    for a in {-0.2, 0.1, 0, 0.1, 0.2}:
        for b in {-0.2, 0.1, 0, 0.1, 0.2}:
            assert isclose(abs(Vector(a, b)), (a**2 + b**2)**0.5)


def test_vector_to_point_conversion() -> None:
    for a in {-2_000_000_000_000, -1_000_000_000_000, -2, -1, -0.2, -0.1, 0, 0.1, 0.2, 1, 2, 1_000_000_000_000, 2_000_000_000_000}:
        for b in {-2_000_000_000_000, -1_000_000_000_000, -2, -1, -0.2, -0.1, 0, 0.1, 0.2, 1, 2, 1_000_000_000_000, 2_000_000_000_000}:
            vector = Vector(a, b)
            point = CartesianPoint(a, b)
            assert vector.convert_to_point().x == point.x and vector.convert_to_point().y == point.y


def test_point_to_vector_conversion() -> None:
    for a in {-2_000_000_000_000, -1_000_000_000_000, -2, -1, -0.2, -0.1, 0, 0.1, 0.2, 1, 2, 1_000_000_000_000, 2_000_000_000_000}:
        for b in {-2_000_000_000_000, -1_000_000_000_000, -2, -1, -0.2, -0.1, 0, 0.1, 0.2, 1, 2, 1_000_000_000_000, 2_000_000_000_000}:
            vector = Vector(a, b)
            point = CartesianPoint(a, b)
            assert vector.x_hat == point.convert_to_vector(
            ).x_hat and vector.y_hat == point.convert_to_vector().y_hat

import pytest
from _helpers import Vector, CartesianPoint

class TestVector:
    def test_vector_creation(self):
        v1 = Vector(1.0, 2.0)
        assert v1.x_hat == 1.0
        assert v1.y_hat == 2.0

        v2 = Vector(0.0, 0.0)
        assert v2.x_hat == 0.0
        assert v2.y_hat == 0.0

        v3 = Vector(-1.0, -2.0)
        assert v3.x_hat == -1.0
        assert v3.y_hat == -2.0

    def test_vector_addition(self):
        
        v1 = Vector(1.0, 2.0)
        v2 = Vector(3.0, 4.0)
        assert v1 + v2 == Vector(4.0, 6.0)

        v3 = Vector(0.0, 0.0)
        v4 = Vector(0.0, 0.0)
        assert v3 + v4 == Vector(0.0, 0.0)

        v5 = Vector(-1.0, -2.0)
        v6 = Vector(-3.0, -4.0)
        assert v5 + v6 == Vector(-4.0, -6.0)

        v7 = Vector(1.0, 2.0)
        v8 = Vector(-3.0, -4.0)
        assert v7 + v8 == Vector(-2.0, -2.0)

    def test_vector_subtraction(self):
        v1 = Vector(1.0, 2.0)
        v2 = Vector(3.0, 4.0)
        assert v1 - v2 == Vector(-2.0, -2.0)

        v3 = Vector(0.0, 0.0)
        v4 = Vector(0.0, 0.0)
        assert v3 - v4 == Vector(0.0, 0.0)

        v5 = Vector(-1.0, -2.0)
        v6 = Vector(-3.0, -4.0)
        assert v5 - v6 == Vector(2.0, 2.0)

        v7 = Vector(1.0, 2.0)
        v8 = Vector(-3.0, -4.0)
        assert v7 - v8 == Vector(4.0, 6.0)

    def test_vector_multiplication(self):
        v1 = Vector(1.0, 2.0)
        assert v1 * 3.0 == Vector(3.0, 6.0)
        assert v1 * 0.0 == Vector(0.0, 0.0)
        assert v1 * -3.0 == Vector(-3.0, -6.0)

        v2 = Vector(-1.0, -2.0)
        assert v2 * -3.0 == Vector(3.0, 6.0)
        assert v2 * 0.0 == Vector(0.0, 0.0)

        v3 = Vector(0.0, 0.0)
        assert v3 * 5.0 == Vector(0.0, 0.0)

    def test_vector_true_division(self):
        v1 = Vector(6.0, 8.0)
        assert v1 / 2.0 == Vector(3.0, 4.0)

        v2 = Vector(0.0, 0.0)
        assert v2 / 2.0 == Vector(0.0, 0.0)
        with pytest.raises(ZeroDivisionError):
            _ = v2 / 0.0

        v3 = Vector(-6.0, -8.0)
        assert v3 / 2.0 == Vector(-3.0, -4.0)
        assert v3 / -2.0 == Vector(3.0, 4.0)
        with pytest.raises(ZeroDivisionError):
            _ = v3 / 0.0

    def test_vector_negation(self):
        v1 = Vector(1.0, -2.0)
        assert -v1 == Vector(-1.0, 2.0)

        v2 = Vector(0.0, 0.0)
        assert -v2 == Vector(0.0, 0.0)

        v3 = Vector(-3.0, 4.0)
        assert -v3 == Vector(3.0, -4.0)

    def test_vector_equality(self):
        v1 = Vector(1.0, 2.0)
        v2 = Vector(1.0, 2.0)
        v3 = Vector(-1.0, -2.0)
        v4 = Vector(0.0, 0.0)

        assert v1 == v2
        assert v1 != v3
        assert v1 != v4
        assert v1 != (1.0, 2.0)
        assert v1 == -v3

    def test_vector_absolute_value(self):
        v1 = Vector(3.0, 4.0)
        assert abs(v1) == 5.0

        v2 = Vector(0.0, 0.0)
        assert abs(v2) == 0.0

        v3 = Vector(-3.0, 4.0)
        assert abs(v3) == 5.0

    def test_vector_dot_product(self):
        v1 = Vector(1.0, 2.0)
        v2 = Vector(3.0, 4.0)
        assert v1.dot_product(v2) == 11.0

        v3 = Vector(0.0, 0.0)
        v4 = Vector(5.0, -2.0)
        assert v3.dot_product(v4) == 0.0
        assert v4.dot_product(v3) == 0.0

        v5 = Vector(-1.0, 3.0)
        v6 = Vector(2.0, -1.0)
        assert v5.dot_product(v6) == -5.0

    def test_vector_projection_onto(self):
        v1 = Vector(1.0, 2.0)
        v2 = Vector(3.0, 0.0)
        projection = v1.project_onto(v2)
        assert projection == Vector(1.0, 0.0)
        
    def test_vector_convert_to_point(self):
        v1 = Vector(1.5, 2.5)
        assert v1.convert_to_point() == CartesianPoint(1.5, 2.5)

        v2 = Vector(0.0, 0.0)
        assert v2.convert_to_point() == CartesianPoint(0.0, 0.0)

        v3 = Vector(-1.5, -2.5)
        assert v3.convert_to_point() == CartesianPoint(-1.5, -2.5)

class TestCartesianPoint:
    def test_cartesian_point_creation(self):
        p1 = CartesianPoint(3.0, 4.0)
        assert p1.x == 3.0
        assert p1.y == 4.0

        p2 = CartesianPoint(0.0, 0.0)
        assert p2.x == 0.0
        assert p2.y == 0.0

        p3 = CartesianPoint(-3.0, -4.0)
        assert p3.x == -3.0
        assert p3.y == -4.0

    def test_cartesian_point_convert_to_vector(self):
        p1 = CartesianPoint(5.0, 6.0)
        assert p1.convert_to_vector() == Vector(5.0, 6.0)

        p2 = CartesianPoint(0.0, 0.0)
        assert p2.convert_to_vector() == Vector(0.0, 0.0)

        p3 = CartesianPoint(-5.0, -6.0)
        assert p3.convert_to_vector() == Vector(-5.0, -6.0)
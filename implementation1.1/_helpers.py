from dataclasses import dataclass
from abc import ABC


@dataclass
class Vector():
    """Data class that represents a vector and has vector operators.
    Relies on the programmer knowing how to use vectors to begin with
    """
    x_hat: float
    y_hat: float

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(
            self.x_hat + other.x_hat,
            self.y_hat + other.y_hat,
        )

    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector(
            self.x_hat - other.x_hat,  # same here
            self.y_hat - other.y_hat,
        )

    def __mul__(self, constant: float) -> 'Vector':
        return Vector(
            self.x_hat * constant,
            self.y_hat * constant,
        )

    def __truediv__(self, constant: float) -> 'Vector':
        return Vector(
            self.x_hat / constant,
            self.y_hat / constant,
        )

    def __neg__(self) -> 'Vector':
        return Vector(-self.x_hat, -self.y_hat)

    # added equality dunder (this is a dundermethod right...)
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return False
        return self.x_hat == other.x_hat and self.y_hat == other.y_hat

    def __abs__(self) -> float:
        return (self.x_hat ** 2 + self.y_hat ** 2) ** 0.5

    # def dot_product(self, other: 'Vector') -> float:
    #     return self.x_hat * other.x_hat + self.y_hat * other.y_hat

    def convert_to_point(self) -> 'CartesianPoint':
        return CartesianPoint(self.x_hat, self.y_hat)


@dataclass
class CartesianPoint():
    x: float
    y: float

    def convert_to_vector(self) -> Vector:
        return Vector(self.x, self.y)

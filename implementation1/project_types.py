from dataclasses import dataclass
from typing import Protocol
from abc import ABC
from dataclasses import dataclass
from typing import Protocol
        
type Movement = tuple[bool, bool, bool, bool] # W, S, A, D 
        
@dataclass(frozen=True)     
class IsKeyPressed():
    movement: Movement
    L: bool
 
class UpdateHandler(Protocol):
    def update(self):
        ...
 
class DrawHandler(Protocol):
    def draw(self):
        ...

@dataclass(frozen=True)
class Vector():
    """This can be any vector really, position, vector, acceleration, anything"""
    x_hat: float
    y_hat: float
    
    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(
            self.x_hat + other.x_hat,  # changed other_y to other_x [sabog k n]
            self.y_hat + other.y_hat,
        )
    
    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector(
            self.x_hat - other.x_hat, # same here
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
    
    def dot_product(self, other: 'Vector') -> float:
        return self.x_hat * other.x_hat + self.y_hat * other.y_hat
    
    # not the m22
    # corrected the operation for magnitude squared
    def project_onto(self, other: 'Vector') -> 'Vector':
        return other * (Vector(self.x_hat, self.y_hat).dot_product(other) / (abs(other)**2))

@dataclass
class Rectangle():
    """A class that stores a representation for what it means to be a 
    rectangle in the game

    Returns:
        top: returns the y value of the top side of the rectangle
        bottom: returns the y value of the bottom side of the rectangle
        left: returns the x value of the left side of the rectangle
        right: returns the x value of the right side of the rectangle
    """
    x: float
    y: float
    width: float
    height: float
    
    @property
    def top(self):
        return self.y
    
    @property
    def bottom(self):
        return self.y + self.height
    
    @property
    def left(self):
        return self.x
    
    @property
    def right(self):
        return self.x + self.width

    # added a .center [conveniency!!]
    @property
    def center(self) -> Vector:
        return Vector(
            x_hat=(self.left + self.right) / 2,
            y_hat=(self.top + self.bottom) / 2
        )
    

@dataclass(frozen=True)
class EggnemyConfig(ABC):
    width: float
    height: float
    movement_speed: float
    base_health: float
    base_damage: float


@dataclass(frozen = True)
class EntityConfig(EggnemyConfig):
    x: float
    y: float
    width: float
    height: float
    movement_speed: float
    base_health: float
    base_damage: float


class HitboxfulObject(Protocol):
    @property
    def top(self) -> float:
        ...
    
    @property
    def bottom(self) -> float:
        ...
    
    @property
    def left(self) -> float:
        ...
    
    @property
    def right(self) -> float:
        ...
        
    @property
    def center(self) -> Vector:
        ...

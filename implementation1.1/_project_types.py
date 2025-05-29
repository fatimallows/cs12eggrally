from dataclasses import dataclass
from typing import Protocol, Callable
from abc import ABC

from _helpers import (CartesianPoint, Vector)

class UpdateHandler(Protocol):
    def update(self):
        ...
        
class DrawHandler(Protocol):
    def draw(self):
        ...
        


@dataclass
class Hitbox(ABC):
    _coordinate: CartesianPoint
    _width: float
    _height: float
    
    def is_touching(self, point: CartesianPoint):
        center_to_point_vector: Vector = self.center.convert_to_vector() - point.convert_to_vector()
        center_to_corner_vector: Vector = self._coordinate.convert_to_vector() - self.center.convert_to_vector()
        return abs(center_to_point_vector.x_hat) <= abs(center_to_corner_vector.x_hat) and \
            abs(center_to_point_vector.y_hat) <= abs(center_to_corner_vector.y_hat)
        
    @property
    def width(self) -> float:
        return self._width
    
    @property
    def height(self) -> float:
        return self._height
    
    @property
    def top(self) -> float:
        return self._coordinate.y
    
    @property
    def bottom(self) -> float:
        return self._coordinate.y + self.height
    
    @property
    def left(self) -> float:
        return self._coordinate.x
    
    @property
    def right(self) -> float:
        return self._coordinate.x + self.width

    @property
    def center(self) -> CartesianPoint:
        return CartesianPoint(
            x=(self.left + self.right) / 2,
            y=(self.top + self.bottom) / 2
        )
    
    # x coordinate
    @property
    def x(self) -> float:
        return self._coordinate.x
    
    @x.setter
    def x(self, val: float):
        self._coordinate.x = val
        
    # y coordinate
    @property
    def y(self) -> float:
        return self._coordinate.y
    
    @y.setter
    def y(self, val: float):
        self._coordinate.y = val
        
    
@dataclass(frozen=True)
class EggConfig():
    hitbox: Hitbox
    movement_speed: float
    max_health: float
    base_damage: float
    damage_hitbox_scale: float # multiplier that decides how large the range of damage is, 1 means damage only when touching  and if > 1, there is some range
    invincibility_frames: int
    
class EggEntity(Protocol):
    def _take_damage(self, damage_value: float) -> None:
        ...
    
    @property
    def hitbox(self) -> Hitbox:
        ...        
    
    @property
    def movement_speed(self) -> float:
        ...
    
    @property
    def max_health(self) -> float:
        ...
    
    @property
    def health(self) -> float:
        ...
    
    @property
    def base_damage(self) -> float:
        ...
        
    @property
    def is_dead(self) -> float:
        ...
        
class EggInfo(Protocol):
    @property
    def hitbox(self) -> Hitbox:
        ...
    
    @property
    def movement_speed(self) -> float:
        ...
    
    @property
    def max_health(self) -> float:
        ...
    
    @property
    def health(self) -> float:
        ...
    
    @property
    def base_damage(self) -> float:
        ...
        
    @property
    def is_dead(self) -> float:
        ...
        
@dataclass(frozen=True)
class Keybinds:
    up: bool
    down: bool
    left: bool
    right: bool
    attack: bool
    
    @property
    def y_one_pressed(self) -> bool:
        return self.up ^ self.down
    
    @property
    def x_one_pressed(self) -> bool:
        return self.left ^ self.right


from dataclasses import dataclass
from typing import Protocol
from abc import ABC
from enum import IntEnum, auto

from _helpers import (CartesianPoint, Vector)
from _egg_entities import Eggnemy

class UpdateHandler(Protocol):
    def update(self):
        ...
        
class DrawHandler(Protocol):
    def draw(self):
        ...
        
@dataclass(frozen=True)
class EggnemyTag(IntEnum):
    EGGNEMY = auto()
    BOSS_EGGNEMY = auto()


@dataclass(frozen=True)
class EggnemyType:
    eggnemy_tag: EggnemyTag
    eggnemy: Eggnemy

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
        return self.width
    
    @property
    def height(self) -> float:
        return self.height
    
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
    y_one_pressed: bool = up ^ down
    x_one_pressed: bool = left ^ right

@dataclass
class EggnemyList():
    _eggnemy_list_len: int = 0
    _eggnemy_list: list[EggnemyType]
    
    def append(self, eggnemy: EggnemyType) -> None:
        self._eggnemy_list.append(eggnemy)
        if eggnemy.eggnemy_tag == EggnemyTag.EGGNEMY:
            self._eggnemy_list_len += 1
            
    def pop(self, index: int) -> None:
        self._eggnemy_list.pop(index)
        if self._eggnemy_list[index].eggnemy_tag == EggnemyTag.EGGNEMY:
            self._eggnemy_list_len -= 1
        
    def len(self) -> int:
        return self._eggnemy_list_len
    
    def update_list(self, updater: callable) -> None:
        for eggnemy_type in self._eggnemy_list:
            updater(eggnemy_type)
        
    @property
    def eggnemy_list(self) -> list[EggnemyType]:
        return self._eggnemy_list.copy()
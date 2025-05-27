from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class Vector():
    """This can be any vector really, position, vector, acceleration, anything"""
    x_hat: float
    y_hat: float

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
    

@dataclass(frozen = True)
class EntityConfig():
    x: float
    y: float
    width: float
    height: float
    movement_speed: float
    base_health: float
    base_damage: float
    

class HitboxfulObject(Protocol):
    @property
    def top(self):
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


class Entity(ABC):
    """Entities are any objects in the game that can move around, fight, and bleed.
    All entities have a rectangle hitbox, just so we can have freedom in what
    we can use as the sprite"""
    def __init__(self, entity_config: EntityConfig):
        self.x = entity_config.x
        self.y = entity_config.y
        self.width = entity_config.width
        self.height = entity_config.height
        self.movement_speed = entity_config.movement_speed
        self.base_health = entity_config.base_health
        self.base_damage = entity_config.base_damage
        
    @abstractmethod
    def deal_damage(self, target: 'Entity') -> None:
        raise NotImplementedError
        
    @abstractmethod
    def move(self, positionVector: Vector) -> None:
        raise NotImplementedError
        
    def take_damage(self, attacker: 'Entity') -> None:
        """Basic taking damage, self base health - attacker base damage  

        Args:
            attacker (Entity): The attacker
        """
        self.base_health -= attacker.base_damage
        
    def get_square_distance_to(self, other: HitboxfulObject) -> float:
        """Takes the coordinates of the other guy and calculates their square distance

        Args:
            other (Entity): Whoever we are checking

        Returns:
            float: The square distance
        """
        # delta y
        if self.bottom > other.top:
            delta_y: float = self.bottom - other.top
        elif other.bottom > self.top:
            delta_y = other.bottom - self.top
        else:
            delta_y = 0
            
        # delta x
        if self.left > other.right:
            delta_x: float = self.left - other.right
        elif other.left > self.right:
            delta_x = other.left - self.right
        else:
            delta_x = 0
            
        # may have weird floating point errors
        # if x and y gets too big, it may cause overflows
        distance: float = delta_y ** 2 + delta_x ** 2 

        return distance
    
    def is_in_collission(self, other: 'Entity') -> bool:
        """Checks if it is in collission with the other entity

        Args:
            other (Entity): _description_

        Returns:
            bool: _description_
        """
        return self.get_square_distance_to(other) == 0
    
    @property
    def top(self) -> float:
        return self.y
    
    @property
    def bottom(self) -> float:
        return self.y + self.height
    
    @property
    def left(self) -> float:
        return self.x
    
    @property
    def right(self) -> float:
        return self.x + self.width
    
    # a little rough (this calculation will be done every single time its called lawl)
    @property
    def center(self) -> Vector:
        return Vector(
            x_hat=(self.right - self.left)/2,
            y_hat=(self.top - self.bottom)/2,
        )
        

class EggEntity(Entity):
    def __init__(self, entity_config: EntityConfig, attack_radius: float):
        super().__init__(entity_config)
        self.attack_radius: float = attack_radius
    
    def deal_damage(self, target):
        ...
        
    def move(self, target):
        ...
    
    
class Eggnemy(Entity):
    ...
        

if __name__ == "__main__":
    entity_config: EntityConfig = EntityConfig(
        x=0,
        y=0,
        width=10,
        height=10,
        movement_speed=10,
        base_damage=100,
        base_health=10,
    )
    
    entity_1: Entity = EggEntity(entity_config, 2)
    entity_2: Entity = EggEntity(entity_config, 2)
    
    entity_1.take_damage(entity_2)

# from __future__ import annotations
# import random
# from dataclasses import dataclass
# from project_types import BirdInfo, Rectangle, PipePairInfo
# from collections.abc import Sequence
 
 
# GAP_HEIGHT = 50
# PIPE_WIDTH = 30
# BIRD_VY = -3
# PIPE_VX = -2
# MIN_PIPE_HEIGHT = 10
 
 
 
# @dataclass
# class Bird:
#     x: float
#     y: float
#     radius: float
#     vy: float
 
#     @property
#     def top(self):
#         return self.y - self.radius
 
#     @property
#     def bottom(self):
#         return self.y + self.radius
 
#     @property
#     def left(self):
#         return self.x - self.radius
 
#     @property
#     def right(self):
#         return self.x + self.radius
 
 
# # PipePair <: PipePairInfo
# @dataclass(eq=False)
# class PipePair:
#     x: float
#     gap_y_start: float
#     gap_height: float
#     screen_height: int
 
#     @property
#     def top_pipe(self) -> Rectangle:
#         return Rectangle(self.x, 0, PIPE_WIDTH, self.gap_y_start)
 
#     @property
#     def bottom_pipe(self) -> Rectangle:
#         y = self.gap_y_start + self.gap_height
#         return Rectangle(self.x, y, PIPE_WIDTH, self.screen_height - y)
 
#     @property
#     def right(self):
#         return self.x + PIPE_WIDTH
 
 
# class Model:
#     def __init__(self, width: int, height: int, fps: int):
#         self._width = width
#         self._height = height
#         self._fps = fps
 
#         self._bird = Bird(width // 2, height // 2, 8, 0)
#         self._is_game_over = False
#         self._pipes: list[PipePair] = []
#         self._done_pipes: set[PipePair] = set()
#         self._score = 0
#         self._frame_count = 0
 
#     def update(self, was_spacebar_just_pressed: bool):
#         """Should be called once per frame/tick."""
#         bird = self._bird
 
#         if bird.top <= 0 or bird.bottom >= self._height:
#             self._is_game_over = True
 
#         if self._is_game_over:
#             return
 
#         if self._frame_count % (self._fps * 2) == 0:
#             gap_start_y = random.randint(
#                 MIN_PIPE_HEIGHT, self._height - MIN_PIPE_HEIGHT - GAP_HEIGHT)
 
#             self._pipes.append(
#                 PipePair(self._width, gap_start_y, GAP_HEIGHT, self._height))
 
#         if was_spacebar_just_pressed:
#             bird.vy = BIRD_VY
 
#         bird.vy += 0.2
#         bird.y += bird.vy
 
#         for pipe_pair in self._pipes:
#             pipe_pair.x += PIPE_VX
 
#             if pipe_pair not in self._done_pipes and bird.x > pipe_pair.x:
#                 self._score += 1
#                 self._done_pipes.add(pipe_pair)
 
#             for pipe in [pipe_pair.top_pipe, pipe_pair.bottom_pipe]:
#                 if self._is_in_collision(bird, pipe):
#                     self._is_game_over = True
#                     break
 
#         self._pipes = [pipe_pair for pipe_pair in self._pipes
#                        if pipe_pair.right >= 0]
 
#         self._one_pipes = {pipe_pair for pipe_pair in self._done_pipes
#                            if pipe_pair.right >= 0}
 
#         self._frame_count += 1
 
#     def _is_in_collision(self, circle: Bird, rect: Rectangle) -> bool:
#         # Left, right, or within?
#         if circle.right < rect.left:
#             test_x = rect.left
#         elif circle.left > rect.right:
#             test_x = rect.right
#         else:
#             test_x = circle.x
 
#         # Up, down, or within?
#         if circle.bottom < rect.top:
#             test_y = rect.top
#         elif circle.top > rect.bottom:
#             test_y = rect.bottom
#         else:
#             test_y = circle.y
 
#         dist = ((test_x - circle.x)**2 + (test_y - circle.y)**2)**0.5
 
#         return dist < circle.radius
 
#     @property
#     def width(self):
#         return self._width
 
#     @property
#     def height(self):
#         return self._height
 
#     @property
#     def fps(self):
#         return self._fps
 
#     @property
#     def pipes(self) -> Sequence[PipePairInfo]:
#         return self._pipes
 
#     @property
#     def bird(self) -> BirdInfo:
#         return self._bird
 
#     @property
#     def score(self) -> int:
#         return self._score
 
#     @property
#     def is_game_over(self) -> int:
#         return self._is_game_over
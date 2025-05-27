from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol
from random import random

FRAMES_PER_SECOND = 30

@dataclass(frozen=True)
class Vector():
    """This can be any vector really, position, vector, acceleration, anything"""
    x_hat: float
    y_hat: float
    
    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(
            self.x_hat + other.y_hat,
            self.y_hat + other.y_hat,
        )
    
    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector(
            self.x_hat - other.y_hat,
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
        
    def __abs__(self) -> float:
        return (self.x_hat ** 2 + self.y_hat ** 2) ** 0.5
    
    def dot_product(self, other: 'Vector') -> float:
        return self.x_hat * other.x_hat + self.y_hat * other.y_hat
    
    def project_onto(self, other: 'Vector') -> 'Vector':
        return other * (Vector(self.x_hat, self.y_hat).dot_product(other) / abs(other)*2)

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
    fps: int
    model_width: int
    model_height: int
    
@dataclass(frozen=True)
class EggnemyConfig(Protocol):
    width: float
    height: float
    movement_speed: float
    base_health: float
    base_damage: float
    fps: int
    

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
    def __init__(self, entity_config: EntityConfig) -> None:
        self.x = entity_config.x
        self.y = entity_config.y
        self.width = entity_config.width
        self.height = entity_config.height
        self.movement_speed = entity_config.movement_speed
        self.base_health = entity_config.base_health
        self.base_damage = entity_config.base_damage
        self.fps = entity_config.fps
        self.model_width = entity_config.model_width
        self.model_height = entity_config.model_height
        
    @abstractmethod
    def move(self, positionVector: Vector) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def tick(self) -> None:
        """anything that requires to be done every frame is done here
        """
        raise NotImplementedError
        
    def get_distance_vector_to(self, other: HitboxfulObject) -> Vector:
        """Simply get the x and y distance of the two objects and slap them on a vector.
        Let R be the object on the right
        Let L be the object on the left
        Let T be the top most object
        Let B be the object on the bottom
        <R.left - L.right, B.top - T.bottom>

        Args:
            other (HitboxfulObject): just anything with a hitbox

        Returns:
            Vector: A position vector that embeds distance and magnitude to another object
        """
        # delta y
        if other.bottom > self.top:
            delta_y: float = other.bottom - self.top
        elif other.top > self.bottom:
            delta_y = other.top - self.bottom
        else:
            delta_y = 0
            
        # delta x
        if self.left > other.right:
            delta_x: float =  other.right - self.left
        elif other.left > self.right:
            delta_x = other.left - self.right
        else:
            delta_x = 0
            
        return Vector(delta_x, delta_y)
        
    def get_distance_to(self, other: HitboxfulObject) -> float:
        """Takes the coordinates of the other guy and calculates their distance

        Args:
            other (Entity): Whoever we are checking

        Returns:
            float: The square distance
        """
        
            
        # may have weird floating point errors
        # if x and y gets too big, it may cause overflows
        
        distance_vector: Vector = self.get_distance_vector_to(other)
        distance: float = abs(distance_vector)

        return distance
    
    def is_in_collission(self, other: 'Entity') -> bool:
        """Checks if it is in collission with the other entity

        Args:
            other (Entity): _description_

        Returns:
            bool: _description_
        """
        return self.get_distance_vector_to(other) == Vector(0, 0)
    
    def take_damage(self, attacker: 'Entity') -> None:
        self.base_health -= attacker.base_damage
    
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
            x_hat=(self.right - self.left),
            y_hat=(self.top - self.bottom),
        ) / 2
    

class EggEntity(Entity):
    def __init__(self, entity_config: EntityConfig, attack_radius: float) -> None:
        super().__init__(entity_config)
        self.attack_radius: float = attack_radius
        self.invincibility_timer: float = 0
        
    def take_damage(self, attacker) -> None:
        if self.invincibility_timer == 0:
            super().take_damage(attacker)
            self.invincibility_timer = FRAMES_PER_SECOND
    
    def attack_eggnemy(self, target: 'EggnemyEntity') -> None:
        if self.get_distance_to(target) <= self.attack_radius:
            target.take_damage(self)
        
    def move(self, direction_vector: Vector) -> None:
        delta_x: float = direction_vector.x_hat * self.movement_speed
        delta_y: float = direction_vector.y_hat * self.movement_speed
        
        self.x += delta_x if 0 <= self.x + delta_x <= self.model_width else 0
        self.y += delta_y if 0 <= self.y + delta_y <= self.model_height else 0
    
    def _tick_invincibility_timer(self) -> None:
        self.invincibility_timer -= 1 if self.invincibility_timer > 0 else 0
        
    def tick(self) -> None:
        self._tick_invincibility_timer()
    
    
class EggnemyEntity(Entity):
    def __init__(self, entity_config: EntityConfig, target_egg: EggEntity) -> None:
        super().__init__(entity_config)   
        self.target_egg = target_egg
        
    def attack_egg(self, target: EggEntity) -> None:
        if self.is_in_collission(target):
            target.take_damage(self)
            
    def move(self, vector_to_egg: Vector) -> None:
        direction_vector: Vector = vector_to_egg / abs(vector_to_egg)
        velocity_vector: Vector = direction_vector * self.movement_speed
        self.x += velocity_vector.x_hat
        self.y += velocity_vector.y_hat
        
    def tick(self) -> None:
        vector_to_egg: Vector = self.get_distance_vector_to(self.target_egg)
        self.attack_egg(self.target_egg)
        self.move(vector_to_egg)
        
        
type Movement = tuple[bool, bool, bool, bool] # W, S, A, D 
        
@dataclass(frozen=True)     
class IsKeyPressed():
    movement: Movement
    L: bool

    
class Model():
    def __init__(self, 
                 fps: int, width: int, height: int, isKeyPressed: IsKeyPressed,
                 attack_radius: float, egg_config: EntityConfig, eggnemy_config: EggnemyConfig):
        self._fps: int = fps
        self._width: int = width
        self._height: int = height
        self._isKeyPressed: IsKeyPressed = isKeyPressed
        
        self.is_game_over: bool = False
        
        self._egg: EggEntity = EggEntity(egg_config, attack_radius)
        self._eggnemies: dict[int, EggnemyEntity] = {
            num: EggnemyEntity(EntityConfig(
                x=(random() * (width - 2 * width)) + width,
                y=(random() * (height - 2 * height)) + height,
                width=eggnemy_config.width,
                height=eggnemy_config.height,
                movement_speed=eggnemy_config.movement_speed,
                base_health=eggnemy_config.base_health,
                base_damage=eggnemy_config.base_damage,
                fps=eggnemy_config.fps,
                model_width=self._width,
                model_height=self._height
            ), self._egg)  for num in range(50)
        }
        
    def update(self):
        # this is hacky as hell
        match(self._isKeyPressed.movement):
            #       W       S       A      D
            case((False, False, False, False) |
                 (True, True, False, False) |
                 (False, False, True, True) |
                 (True, True, True, True)):
                pass
            case((True, False, False, False) |
                 (True, False, True, True)):
                self._egg.move(Vector(-1, 0))
            case((False, True, False, False) |
                 (False, True, True, True)):
                self._egg.move(Vector(1, 0))
            case((False, False, True, False) |
                 (True, True, True, False)):
                self._egg.move(Vector(0, -1))
            case((False, False, False, True) |
                 (True, True, False, True)):
                self._egg.move(Vector(0, 1))
            case((True, False, True, False)):
                self._egg.move(Vector(-1, -1))
            case((True, False, False, True)):
                self._egg.move(Vector(-1, 1))
            case((False, True, True, False)):
                self._egg.move(Vector(1, -1))
            case((False, True, False, True)):
                self._egg.move(Vector(1, 1))
            case _:
                raise RuntimeError("How the fuck")
        
        if self._isKeyPressed.L:
            for i_num in self._eggnemies:
                self._egg.attack_eggnemy(self._eggnemies[i_num])
        

if __name__ == "__main__":
    entity_config: EntityConfig = EntityConfig(
        x=0,
        y=0,
        width=10,
        height=10,
        movement_speed=10,
        base_damage=100,
        base_health=10,
        fps=30,
        model_width=100,
        model_height=100,
    )
    
    entity_1: Entity = EggEntity(entity_config, 2)
    entity_2: Entity = EggEntity(entity_config, 2)
    
    entity_1.take_damage(entity_2)

"""from __future__ import annotations
import random
from dataclasses import dataclass
from project_types import BirdInfo, Rectangle, PipePairInfo
from collections.abc import Sequence
 
 
GAP_HEIGHT = 50
PIPE_WIDTH = 30
BIRD_VY = -3
PIPE_VX = -2
MIN_PIPE_HEIGHT = 10
 
 
 
@dataclass
class Bird:
    x: float
    y: float
    radius: float
    vy: float
 
    @property
    def top(self):
        return self.y - self.radius
 
    @property
    def bottom(self):
        return self.y + self.radius
 
    @property
    def left(self):
        return self.x - self.radius
 
    @property
    def right(self):
        return self.x + self.radius
 
 
# PipePair <: PipePairInfo
@dataclass(eq=False)
class PipePair:
    x: float
    gap_y_start: float
    gap_height: float
    screen_height: int
 
    @property
    def top_pipe(self) -> Rectangle:
        return Rectangle(self.x, 0, PIPE_WIDTH, self.gap_y_start)
 
    @property
    def bottom_pipe(self) -> Rectangle:
        y = self.gap_y_start + self.gap_height
        return Rectangle(self.x, y, PIPE_WIDTH, self.screen_height - y)
 
    @property
    def right(self):
        return self.x + PIPE_WIDTH"""
 
 
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
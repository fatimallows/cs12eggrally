from random import random, uniform
from egg_entities import (
    Entity, EggEntity, EggnemyEntity
)
from project_types import (
    EntityConfig, EggnemyConfig,
    Rectangle, IsKeyPressed, Vector,
    )
import pyxel


class Model():
    def __init__(self, 
                 fps: int, width: int, height: int, world_width: int, world_height: int, eggnemy_entity_limit: int,
                 attack_radius: float, egg_config: EntityConfig, eggnemy_config: EggnemyConfig):
        self._fps: int = fps
        self._width: int = width
        self._height: int = height
        self._world_width: int = world_width
        self._world_height: int = world_height
        # to make sure eggnemise dont spawn so near
        min_distance = 50
        self._elapsed_frames = 0
        
        self.is_game_over: bool = False
        
        egg_config_centered = EntityConfig(
            x=(width - egg_config.width) / 2,
            y=(height - egg_config.height) / 2,
            width=egg_config.width,
            height=egg_config.height,
            movement_speed=egg_config.movement_speed,
            base_health=egg_config.base_health,
            base_damage=egg_config.base_damage,
        )
        self._egg: EggEntity | None = EggEntity(
            egg_config_centered, self._fps, self._world_width, self._world_height,  # added world
            attack_radius)
        # crashing the FUCK out
        self._eggnemies: dict[int, EggnemyEntity] = {}
        
        for num in range(eggnemy_entity_limit):
            while True:
                x = uniform(0, width - eggnemy_config.width)
                y = uniform(0, height - eggnemy_config.height)
                test_entity = Rectangle(x, y, eggnemy_config.width, eggnemy_config.height)
                if self._egg.get_distance_to(test_entity) > min_distance:
                    break
            self._eggnemies[num] = EggnemyEntity(EntityConfig(
                x=x,
                y=y,
                width=eggnemy_config.width,
                height=eggnemy_config.height,
                movement_speed=eggnemy_config.movement_speed,
                base_health=eggnemy_config.base_health,
                base_damage=eggnemy_config.base_damage,
            ), self._fps, self._width, self._height, self._egg)
        
    def update(self, is_key_pressed: IsKeyPressed):
        self._elapsed_frames += 1
        # game over girl
        if self._egg is None or self._egg.is_dead:
            self._egg = None
            return
        
        self._egg.move(Vector(
            (-1 if is_key_pressed.movement[2] else 0) + (1 if is_key_pressed.movement[3] else 0), 
            (-1 if is_key_pressed.movement[0] else 0) + (1 if is_key_pressed.movement[1] else 0), 
        ))
        
        if is_key_pressed.L:
            for i_num in self._eggnemies:
                self._egg.attack_eggnemy(self._eggnemies[i_num])
        
        dead_enemies: list[int] = [] 
        for key in self._eggnemies:
            if self._eggnemies[key].is_dead:
                dead_enemies.append(key)
                
        for key in dead_enemies:
            del self._eggnemies[key]
            
        if pyxel.btnp(pyxel.KEY_Q):
            # use this to check certain values lmfao
            print(self._eggnemies)

    # this is for time
    def get_elapsed_time_formatted(self) -> str:
        total_seconds = self._elapsed_frames // self._fps
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"  # zero-padded time

            
            
            

if __name__ == "__main__":
    pass

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
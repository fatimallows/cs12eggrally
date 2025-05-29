from random import uniform
from dataclasses import dataclass

import itertools

from _project_types import Hitbox, EggnemyType, EggnemyTag, EggnemyList, Keybinds
from _helpers import CartesianPoint, Vector
from _egg_entities import EggConfig, Egg, Eggnemy



class Model():
    def __init__(self,
                 fps: int, screen_width: int, screen_height: int, world_width: int, world_height: int, 
                 eggnemy_entity_limit: int, eggnemy_kills_boss_trigger: int,
                 egg_config: EggConfig, eggnemy_config: EggConfig, boss_eggnemy_config: EggConfig):        
        # world definitions
        self._fps: int = fps
        self._screen_width: int = screen_width
        self._screen_height: int = screen_height
        self._world_width: int = world_width
        self._world_height: int = world_height
        self._world_x: float = (self._screen_width - self._world_width) / 2  
        self._world_y: float = (self._screen_height - self._world_height) / 2
        
        # eggnemy generation fields
        # to make sure eggnemise dont spawn so near
        self._safe_radius = 50
        self._counter = itertools.count()
        self._eggnemy_entity_limit: int = eggnemy_entity_limit
        self._eggnemy_kills_boss_trigger: int = eggnemy_kills_boss_trigger 
        
        # game state
        self._is_game_over: bool = False
        self._elapsed_frames: int = 0
        self._eggnemies_killed: int = 0
        self._no_boss_generated: bool = True
        self._boss_id: int |  None = None 
        self._is_boss_alive: bool | None = None
        
        
        # entities
        self._egg: Egg = Egg(egg_config)
        self._eggnemy_config: EggConfig = eggnemy_config
        self._boss_eggnemy_config: EggConfig = boss_eggnemy_config
        self._eggnemy_list: EggnemyList = EggnemyList(
            eggnemy_list=[]
        )
        
    def _is_hitbox_in_bounds(self, hitbox: Hitbox) -> bool:
        is_within_x: bool = hitbox.right <= self.world_right and hitbox.left >= self.world_left
        is_within_y: bool = hitbox.top >= self.world_top and hitbox.left <= self.world_bottom
        return is_within_x and is_within_y
        
    def _generate_spawn_location(self) -> CartesianPoint:
        while True:
            x = uniform(self._world_x, self._world_width - self._eggnemy_config.hitbox.width)
            y = uniform(self._world_y, self._world_height - self._eggnemy_config.hitbox.height)
            test_egg = Hitbox(CartesianPoint(x, y), self._eggnemy_config.hitbox.width, self._eggnemy_config.hitbox.height)
            if not self._egg._is_dead and self._egg._get_vector_to_hitbox(test_egg) > self._safe_radius and self._is_hitbox_in_bounds(test_egg):
                return CartesianPoint(x, y)
            
    def _generate_eggnemies(self) -> None:
        while self._eggnemy_list.len() < self._eggnemy_entity_limit:
            self._eggnemy_list.append(EggnemyType(
                eggnemy_tag=EggnemyTag.EGGNEMY,
                eggnemy=Eggnemy(self._eggnemy_config)
            ))
            
    def _generate_boss(self) -> None:
        self._eggnemy_list.append(EggnemyType(
                eggnemy_tag=EggnemyTag.BOSS_EGGNEMY,
                eggnemy=Eggnemy(self._boss_eggnemy_config, self._egg),
            ))
            
        
    def update(self, keybinds: Keybinds) -> None:
        if self.is_game_over:
            return
        
        self._elapsed_frames += 1
        
        if keybinds.x_one_pressed:
            x_hat: int = 1 if keybinds.left else -1
        else:
            x_hat = 0    
        
        if keybinds.y_one_pressed:
            y_hat: int = 1 if keybinds.up else -1
        else:
            y_hat = 0
            
        velocity_vector = Vector(x_hat, y_hat)
        
        try:
            velocity_vector = velocity_vector / abs(velocity_vector)
        except ZeroDivisionError:
            pass
        
        move_vector = velocity_vector * self._egg.movement_speed
        
        if keybinds.attack:
            self._eggnemy_list.update_list(lambda eggnemy : self._egg.deal_damage(eggnemy))
            
        # moves the world
        cond_x: bool = self.world_right + move_vector.x_hat >= self._egg.right and self._egg.left >= self.world_left + move_vector.x_hat  
        cond_y: bool = self.world_bottom + move_vector.y_hat >= self._egg.bottom and self._egg.top >= self.world_top + move_vector.y_hat
        
        # print(f"is x OOB {cond_x}\n is y OOB {cond_y}")
                
        self._world_x += move_vector.x_hat if cond_x else 0
        self._world_y += move_vector.y_hat if cond_y else 0
          
          
        self._eggnemy_list.update_list(self._move_all(Vector(
            move_vector.x_hat if cond_x else 0,
            move_vector.y_hat if cond_y else 0,
        )))        
        
        if self._eggnemies_killed >= self._eggnemy_kills_boss_trigger and self._no_boss_generated:
            self._generate_boss()
    
    def _move_all(self, move_vector: Vector) -> None:
        def _f(eggnemy: Eggnemy) -> None:
            eggnemy.move(move_vector)
        
        return _f
    
    @property
    def fps(self) -> int:
            return self._fps
        
    @property
    def world_x(self) -> int:
            return self._world_x
        
    @property
    def world_y(self) -> int:
            return self._world_y
        
    @property
    def world_top(self) -> float:
        return self._world_y
    
    @property
    def world_bottom(self) -> float:
        return self._world_y + self._world_height
    
    @property
    def world_left(self) -> float:
        return self._world_x
    
    @property
    def world_right(self) -> float:
        return self._world_x + self._world_width

    @property
    def screen_width(self) -> int:
            return self._screen_width
    
    @property
    def screen_height(self) -> int:
            return self._screen_height
        
    @property
    def world_width(self) -> int:
            return self._world_width
        
    @property
    def world_height(self) -> int:
            return self._world_height
        
    @property
    def is_game_over(self) -> bool:
        return self._is_game_over
    
    @property
    def elapsed_frames(self) -> int:
            return self.elapsed_frames
        
    @property
    def eggnemies_killed(self) -> int:
            return self._eggnemies_killed
    
    
        
    
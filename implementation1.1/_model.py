from random import uniform
from typing import Callable
from dataclasses import dataclass

import itertools

from _project_types import Hitbox, Keybinds, InitEggConfig
from _helpers import CartesianPoint, Vector
from _egg_entities import EggConfig, Egg, Eggnemy, EggnemyType, EggnemyTag, EggnemyList



class Model():
    def __init__(self,
                 fps: int, screen_width: int, screen_height: int, world_width: int, world_height: int, 
                 eggnemy_entity_limit: int, eggnemy_kills_boss_trigger: int,
                 egg_config: InitEggConfig, eggnemy_config: InitEggConfig, boss_eggnemy_config: InitEggConfig):        
        # world definitions
        self._fps: int = fps
        self._screen_width: int = screen_width
        self._screen_height: int = screen_height
        self._world_width: int = world_width
        self._world_height: int = world_height
        self._world_x: float = (self._screen_width - self._world_width) // 2 if self._screen_width - self._world_width > 0 else 0
        self._world_y: float = (self._screen_height - self._world_height) // 2 if self._screen_height - self._world_height > 0 else 0
        
        # eggnemy generation fields
        # to make sure eggnemise dont spawn so near
        self._safe_radius = 10
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
        self._egg: Egg = Egg(EggConfig(
            hitbox=Hitbox(
                _coordinate=CartesianPoint(
                    (self.screen_width - egg_config._width) // 2,
                    (self.screen_height - egg_config._height) // 2,
                ),
                _width=egg_config._width,
                _height=egg_config._height
            ),
            movement_speed=egg_config.movement_speed,
            max_health=egg_config.max_health,
            base_damage=egg_config.base_damage,
            damage_hitbox_scale=egg_config.damage_hitbox_scale,
            invincibility_frames=egg_config.invincibility_frames,
        ))
        self._eggnemy_config: InitEggConfig = eggnemy_config
        self._boss_eggnemy_config: InitEggConfig = boss_eggnemy_config
        self._eggnemy_list: EggnemyList = EggnemyList(
            _eggnemy_list={}
        )
    def _is_hitbox_in_bounds(self, hitbox: Hitbox) -> bool:
        # breakpoint()
        is_within_x: bool = hitbox.right <= self.world_right and hitbox.left >= self.world_left
        is_within_y: bool = hitbox.top >= self.world_top and hitbox.left <= self.world_bottom
        return is_within_x and is_within_y
        
    def _generate_spawn_location(self) -> CartesianPoint:
        while True:
            x = uniform(self.world_left, self.world_right - self._eggnemy_config._width)
            y = uniform(self.world_top, self.world_bottom - self._eggnemy_config._height)
            test_egg = Hitbox(CartesianPoint(x, y), self._eggnemy_config._width, self._eggnemy_config._height)
            # breakpoint()
            if not self._egg._is_dead and abs(self._egg._get_vector_to_hitbox(test_egg)) > self._safe_radius and self._is_hitbox_in_bounds(test_egg):
                break
        return CartesianPoint(x, y)
            
    def _generate_individual_eggnemy(self) -> Eggnemy:
        point = self._generate_spawn_location()
        return Eggnemy(
            egg_config=EggConfig(
                hitbox=Hitbox(
                    _coordinate=point,
                    _width=self._eggnemy_config._width,
                    _height=self._eggnemy_config._height,
                ),
                movement_speed=self._eggnemy_config.movement_speed,
                max_health=self._eggnemy_config.max_health,
                base_damage=self._eggnemy_config.base_damage,
                damage_hitbox_scale=self._eggnemy_config.damage_hitbox_scale,
                invincibility_frames=self._eggnemy_config.invincibility_frames,
            ),
            egg_target=self._egg
        )
            
    def _generate_eggnemies(self) -> None:
        while self._eggnemy_list.len() < self._eggnemy_entity_limit:
            self._eggnemy_list.append(EggnemyType(
                eggnemy_tag=EggnemyTag.EGGNEMY,
                eggnemy=self._generate_individual_eggnemy()
            ))
            
    def _generate_boss(self) -> None:
        point = self._generate_spawn_location()
        self._eggnemy_list.append(EggnemyType(
                eggnemy_tag=EggnemyTag.BOSS_EGGNEMY,
                eggnemy=Eggnemy(
                egg_config=EggConfig(
                    hitbox=Hitbox(
                        _coordinate=point,
                        _width=self._boss_eggnemy_config._width,
                        _height=self._boss_eggnemy_config._height,
                    ),
                    movement_speed=self._boss_eggnemy_config.movement_speed,
                    max_health=self._boss_eggnemy_config.max_health,
                    base_damage=self._boss_eggnemy_config.base_damage,
                    damage_hitbox_scale=self._boss_eggnemy_config.damage_hitbox_scale,
                    invincibility_frames=self._boss_eggnemy_config.invincibility_frames,
                ),
            egg_target=self._egg
        ),
            ))
        # breakpoint()
            
        
    def update(self, keybinds: Keybinds) -> None:
        # game over check
        if self.is_game_over:
            return
        
        # generate or regenerate eggnemies
        self._generate_eggnemies()
        
        # move time by one
        self._elapsed_frames += 1
        
        # movement 
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
            # print("attacking")
            self._eggnemy_list.update_list(self._damage_all)
            # self._eggnemy_list.update_list(self.)
            
        # moves the world
        cond_x: bool = self.world_right + move_vector.x_hat >= self._egg.hitbox.right and self._egg.hitbox.left >= self.world_left + move_vector.x_hat  
        cond_y: bool = self.world_bottom + move_vector.y_hat >= self._egg.hitbox.bottom and self._egg.hitbox.top >= self.world_top + move_vector.y_hat
        
        # print(f"is x OOB {cond_x}\n is y OOB {cond_y}")
                
        self._world_x += move_vector.x_hat if cond_x else 0
        self._world_y += move_vector.y_hat if cond_y else 0
          
          
        self._eggnemy_list.update_list(self._move_all(Vector(
            move_vector.x_hat if cond_x else 0,
            move_vector.y_hat if cond_y else 0,
        )))        
        
        self._eggnemy_list.update_list(self._attack_egg)
        self._egg.tick()
        
        if self._egg.is_dead:
            self._is_game_over = True
        
        if self._eggnemies_killed >= self._eggnemy_kills_boss_trigger and self._no_boss_generated:
            self._generate_boss()
            self._no_boss_generated = False
            for key in self._eggnemy_list._eggnemy_list:
                if self._eggnemy_list._eggnemy_list[key].eggnemy_tag is EggnemyTag.BOSS_EGGNEMY:
                    self._boss_id = key
        elif not self._no_boss_generated and self._boss_id is not None:
            try:
                self._eggnemy_list.eggnemy_list[self._boss_id]
            except:
                print("you win")
                self._is_game_over = True
                return
            
    def _attack_egg(self, eggnemy: Eggnemy) -> None:
        eggnemy.deal_damage(self._egg)
        
    
    def _move_all(self, move_vector: Vector) -> Callable:
        def _f(eggnemy: Eggnemy) -> None:
            eggnemy.move(move_vector)
        
        return _f
    
    def _damage_all(self, eggnemy: Eggnemy) -> None:
            self._egg.deal_damage(eggnemy)
            
            # print(eggnemy.health)
            
            if eggnemy.is_dead:
                self._eggnemies_killed += 1
    
    @property
    def fps(self) -> int:
            return self._fps
        
    @property
    def world_x(self) -> float:
            return self._world_x
        
    @property
    def world_y(self) -> float:
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
            return self._elapsed_frames
        
    @property
    def eggnemies_killed(self) -> int:
            return self._eggnemies_killed
    
    

# model = Model(
#     fps=30,
#     screen_width=200,
#     screen_height=200,
#     world_width=100,
#     world_height=100,
#     eggnemy_entity_limit=10,
#     eggnemy_kills_boss_trigger=20,
#     egg_config=InitEggConfig(
#         _width=20,
#         _height=20,
#         movement_speed=2,
#         max_health=10,
#         base_damage=1,
#         damage_hitbox_scale=1.3,
#         invincibility_frames=30,
#         ),
#     eggnemy_config=InitEggConfig(
#         _width=10,
#         _height=10,
#         movement_speed=0.5,
#         max_health=5,
#         base_damage=1,
#         damage_hitbox_scale=1,
#         invincibility_frames=0
#         ),
#     boss_eggnemy_config=InitEggConfig(
#         _width=30,
#         _height=30,
#         movement_speed=1,
#         max_health=30,
#         base_damage=3,
#         damage_hitbox_scale=1,
#         invincibility_frames=0
#         )        
# )
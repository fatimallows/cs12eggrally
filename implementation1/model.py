from random import random, uniform
from egg_entities import (
    Entity, EggEntity, EggnemyEntity, BossEntity
)
from project_types import (
    EntityConfig, EggnemyConfig,
    Rectangle, IsKeyPressed, Vector,
    )
import pyxel
import itertools


class Model():
<<<<<<< HEAD
    def __init__(self, 
                 fps: int, width: int, height: int, eggnemy_entity_limit: int,
                 attack_radius: float, egg_config: EntityConfig, eggnemy_config: EggnemyConfig, boss_config: EggnemyConfig):
        self._fps: int = fps
        self._width: int = width
        self._height: int = height
        # timer stats
        self.timer_frames: int = 0
        # to make sure eggnemise dont spawn so near
        min_distance = 50
        # score
        self.eggnemies_killed = 0
        # for boss purposes
        self.boss_config = boss_config
        self.boss_spawned_for_kill = set()
        self.has_won = False

        self.is_game_over: bool = False
=======
    def __init__(self, #world_x: int, world_y: int,
                 fps: int, screen_width: int, screen_height: int, world_width: int, world_height: int, 
                 eggnemy_entity_limit: int, eggnemy_kills_boss_trigger: int, attack_radius: float, 
                 egg_config: EntityConfig, eggnemy_config: EggnemyConfig, boss_eggnemy_config: EggnemyConfig):
        self._fps: int = fps
        
        # world definitions
        self._screen_width: int = screen_width
        self._screen_height: int = screen_height
        self._world_width: int = world_width
        self._world_height: int = world_height
        self._world_x: float = (self._screen_width - self._world_width) / 2  
        self._world_y: float = (self._screen_height - self._world_height) / 2
        
        # eggnemy generation fields
        # to make sure eggnemise dont spawn so near
        self._min_distance = 50
        # self._spawn_radius = (self._world_width ** 2 + self._world_height ** 2) ** 0.5
        self._coutner = itertools.count()
        self._eggnemy_entity_limit: int = eggnemy_entity_limit
        self._eggnemy_config: EggnemyConfig = eggnemy_config
        self._eggnemy_kills_boss_trigger: int = eggnemy_kills_boss_trigger 
        
        # game state
        self._is_game_over: bool = False
        self._elapsed_frames: int = 0
        self._eggnemies_killed: int = 0
        self._no_boss_generated: bool = True
        self._boss_id: int |  None = None 
        self._is_boss_alive: bool | None = None
>>>>>>> 62444033178977a8dda0cd316888e59fb533f7f5
        
        
        # entities
        egg_config_centered = EntityConfig(
            x=(screen_width - egg_config.width) / 2,
            y=(screen_height - egg_config.height) / 2,
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
        self._boss_eggnemy_config: EggnemyConfig = boss_eggnemy_config
        
        while True:
            try:
                self.generate_eggnemies()
            except OverflowError:
                break
            
    def generate_eggnemies(self):
        if len(self._eggnemies) <= self._eggnemy_entity_limit:
            while True:
                x = uniform(self._world_x, self._world_width - self._eggnemy_config.width)
                y = uniform(self._world_y, self._world_height - self._eggnemy_config.height)
                test_entity = Rectangle(x, y, self._eggnemy_config.width, self._eggnemy_config.height)
                if self._egg is not None and self._egg.get_distance_to(test_entity) > self._min_distance and self.is_test_entity_in_bounds(test_entity):
                    break
            self._eggnemies[next(self._coutner)] = EggnemyEntity(EntityConfig(
                x=x,
                y=y,
                width=self._eggnemy_config.width,
                height=self._eggnemy_config.height,
                movement_speed=self._eggnemy_config.movement_speed,
                base_health=self._eggnemy_config.base_health,
                base_damage=self._eggnemy_config.base_damage,
            ), self._fps, self._world_width, self._world_height, self._egg)
        else:
            raise OverflowError("Eggnemy entity cap reached")
        
<<<<<<< HEAD
        self.next_id = len(self._eggnemies)

    def update(self, is_key_pressed: IsKeyPressed):
        # is it over now
        if self.has_won:
            self.is_game_over = True
            return
        
        if self._egg is None or self._egg.is_dead:
            self.is_game_over = True
            return

        # BOSS!!!
        if self.eggnemies_killed > 0 and self.eggnemies_killed % 10 == 0:
            if self.eggnemies_killed not in self.boss_spawned_for_kill:
                boss_x = uniform(0, self._width - self._width // 10)
                boss_y = uniform(0, self._height - self._height // 10)

                boss_entity_config = EntityConfig(
                    x=boss_x,
                    y=boss_y,
                    width=30,
                    height=40,
                    movement_speed=self.boss_config.movement_speed,
                    base_health=self.boss_config.base_health,
                    base_damage=self.boss_config.base_damage,
                )

                boss = BossEntity(boss_entity_config, self._fps, self._width, self._height, self._egg)
                self._eggnemies[self.next_id] = boss
                self.next_id += 1
                self.boss_spawned_for_kill.add(self.eggnemies_killed)
                
        # timer
        self.timer_frames += 1
        
        self._egg.move(Vector(
            (-1 if is_key_pressed.movement[2] else 0) + (1 if is_key_pressed.movement[3] else 0), 
            (-1 if is_key_pressed.movement[0] else 0) + (1 if is_key_pressed.movement[1] else 0), 
        ))
=======
    def is_test_entity_in_bounds(self, test_entity: Rectangle):
        is_within_x: bool = test_entity.right <= self.world_right and test_entity.left >= self.world_left
        is_within_y: bool = test_entity.top >= self.world_top and test_entity.bottom <= self.world_bottom
        return is_within_x and is_within_y
                
    def update(self, is_key_pressed: IsKeyPressed):
        self._elapsed_frames += 1
        # game over girl
        if self._egg is None or self._egg.is_dead:
            self._egg = None
            return
        
        # vector that would dictate how the world and enemies should move based on 
        # user input
        # just the direction
        velocity_vector = Vector(
            (1 if is_key_pressed.movement[2] else 0) + (-1 if is_key_pressed.movement[3] else 0), # x movement
            (1 if is_key_pressed.movement[0] else 0) + (-1 if is_key_pressed.movement[1] else 0), # y movement
        )
>>>>>>> 62444033178977a8dda0cd316888e59fb533f7f5
        
        try:
            velocity_vector = velocity_vector / abs(velocity_vector) # normalize
        except ZeroDivisionError:
            velocity_vector = Vector(0, 0)
        
        egg_velocity_vector = velocity_vector * self._egg._movement_speed
                    
        # if L is pressed on the current frame, attempt an attack on every single enemy in the game
        # a little inefficient but whatever
        if is_key_pressed.L: 
            for i_num in self._eggnemies:
                self._egg.attack_eggnemy(self._eggnemies[i_num])
        
<<<<<<< HEAD
        dead_enemies: list[int] = [] 
        for key in self._eggnemies:
            if self._eggnemies[key].is_dead:
                if isinstance(self._eggnemies[key], BossEntity):
                    self.has_won = True
                dead_enemies.append(key)
               
        for key in dead_enemies:
            del self._eggnemies[key]
            self.eggnemies_killed += 1

=======
        # moves the world
        cond_x: bool = self.world_right + egg_velocity_vector.x_hat >= self._egg.right and self._egg.left >= self.world_left + egg_velocity_vector.x_hat  
        cond_y: bool = self.world_bottom + egg_velocity_vector.y_hat >= self._egg.bottom and self._egg.top >= self.world_top + egg_velocity_vector.y_hat
        
        # print(f"is x OOB {cond_x}\n is y OOB {cond_y}")
                
        self._world_x += egg_velocity_vector.x_hat if cond_x else 0
        self._world_y += egg_velocity_vector.y_hat if cond_y else 0
                
        self.update_enemy_list(Vector(
            egg_velocity_vector.x_hat if cond_x else 0,
            egg_velocity_vector.y_hat if cond_y else 0,
        ))
        
        if self._eggnemies_killed >= self._eggnemy_kills_boss_trigger and self._no_boss_generated:
            self.generate_boss()
            
>>>>>>> 62444033178977a8dda0cd316888e59fb533f7f5
        if pyxel.btnp(pyxel.KEY_Q):
            # use this to check certain values lmfao
            print(self._eggnemies)
            
<<<<<<< HEAD

=======
    # this is for time
    def get_elapsed_time_formatted(self) -> str:
        total_seconds = self._elapsed_frames // self._fps
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"  # zero-padded time
    
    def update_enemy_list(self, velocity_vector: Vector) -> None:
        dead_enemies: list[int] = [] 
        for key in self._eggnemies:
            eggnemy = self._eggnemies[key] 
            
            if key == self._boss_id and eggnemy.is_dead:
                self._is_boss_alive = False
                self._eggnemy_entity_limit -= 1
                
            if eggnemy.is_dead:
                dead_enemies.append(key)
                self._eggnemies_killed += 1
                continue
            
            eggnemy.set_offset_vector(velocity_vector)
            eggnemy.tick()
                
        for key in dead_enemies:
            del self._eggnemies[key]
            
        while True:
            try:
                self.generate_eggnemies()
            except OverflowError:
                break  
            
    def generate_boss(self) -> None :
        self._eggnemy_entity_limit += 1
        self._no_boss_generated = False
        self._is_boss_alive = True
        while True:
            x = uniform(0, self._screen_width - self._eggnemy_config.width)
            y = uniform(0, self._screen_height - self._eggnemy_config.height)
            test_entity = Rectangle(x, y, self._eggnemy_config.width, self._eggnemy_config.height)
            if self._egg is not None and self._egg.get_distance_to(test_entity) > self._min_distance and self.is_test_entity_in_bounds(test_entity):
                break
        boss_eggnemy: EggnemyEntity = EggnemyEntity(
                EntityConfig(
                    width=self._boss_eggnemy_config.width,
                    height=self._boss_eggnemy_config.height,
                    movement_speed=self._boss_eggnemy_config.movement_speed,
                    base_health=self._boss_eggnemy_config.base_health,
                    base_damage=self._boss_eggnemy_config.base_damage,
                    x=x,
                    y=y,
                ), 
            self._fps, self._world_width, self._world_height, self._egg)
        self._boss_id = next(self._coutner)
        self._eggnemies[self._boss_id] = boss_eggnemy
    
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
    def eggnemies_killed(self) -> int:
        return self._eggnemies_killed

            
            
>>>>>>> 62444033178977a8dda0cd316888e59fb533f7f5
            

if __name__ == "__main__":
    pass

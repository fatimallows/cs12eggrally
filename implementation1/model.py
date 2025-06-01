from random import random, uniform
from egg_entities import (
    Entity, EggEntity, EggnemyEntity, BossEntity
)
from project_types import (
    EntityConfig, EggnemyConfig,
    Rectangle, IsKeyPressed, Vector,
    )
import pyxel


class Model():
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
            egg_config_centered, self._fps, self._width, self._height, 
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
        
        if is_key_pressed.L:
            for i_num in self._eggnemies:
                self._egg.attack_eggnemy(self._eggnemies[i_num])
        
        dead_enemies: list[int] = [] 
        for key in self._eggnemies:
            if self._eggnemies[key].is_dead:
                if isinstance(self._eggnemies[key], BossEntity):
                    self.has_won = True
                dead_enemies.append(key)
               
        for key in dead_enemies:
            del self._eggnemies[key]
            self.eggnemies_killed += 1

        if pyxel.btnp(pyxel.KEY_Q):
            # use this to check certain values lmfao
            print(self._eggnemies)
            

            

if __name__ == "__main__":
    pass

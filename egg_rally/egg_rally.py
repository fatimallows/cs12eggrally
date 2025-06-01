from egg_rally.model import Model
from egg_rally.view import View
from egg_rally.controller import Controller
from egg_rally.project_types import InitEggConfig
# from egg_rally.helpers import CartesianPoint
from egg_rally.extract_json import json_handler_protocol


class EggRally:
    def main(json_handler: json_handler_protocol) -> None:
        _settings = json_handler.extract_settings('all')
        width: int = _settings['screen_width']
        height: int = _settings['screen_height']
        world_width: int = _settings['world_width']  # added world width
        world_height: int = _settings['world_height']  # and height
        fps: int = _settings['game_fps']
        eggnemy_width: float = _settings['eggnemy_width']
        eggnemy_height: float = _settings['eggnemy_height']
        egg_health: float = _settings['egg_health']
        egg_width: float = _settings['egg_width']
        egg_height: float = _settings['egg_height']
        # added enemy health
        eggnemy_health: float = _settings['eggnemy_health']
        eggnemy_entity_limit: int = _settings['eggnemy_cap']
        boss_spawn_count: int = _settings['boss_spawn_counter']
        boss_health: float = _settings['boss_health']
        boss_width: float = _settings['boss_width']
        boss_height: float = _settings['boss_height']

        model = Model(
            fps=fps,
            screen_width=width,
            screen_height=height,
            world_width=world_width,
            world_height=world_height,
            eggnemy_entity_limit=eggnemy_entity_limit,
            eggnemy_kills_boss_trigger=boss_spawn_count,
            egg_config=InitEggConfig(
                _width=egg_width,
                _height=egg_height,
                movement_speed=2,
                max_health=egg_health,
                base_damage=1,
                damage_hitbox_scale=2,
                invincibility_frames=fps*1,
            ),
            eggnemy_config=InitEggConfig(
                _width=eggnemy_width,
                _height=eggnemy_height,
                movement_speed=0.5,
                max_health=eggnemy_health,
                base_damage=1,
                damage_hitbox_scale=1,
                invincibility_frames=0
            ),
            boss_eggnemy_config=InitEggConfig(
                _width=boss_width,
                _height=boss_height,
                movement_speed=1,
                max_health=boss_health,
                base_damage=3,
                damage_hitbox_scale=1,
                invincibility_frames=0
            )
        )
        view = View(screen_width=width,
                    screen_height=height,
                    world_width=world_width,
                    world_height=world_height,
                    fps=fps)
        controller = Controller(_settings)

        controller.start()

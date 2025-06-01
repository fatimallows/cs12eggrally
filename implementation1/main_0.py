from model import Model, EntityConfig, EggnemyConfig
from controller import Controller
from view import View
from extract_json import json_handler_protocol, json_handler
from typing import Literal


def main(json_handler: json_handler_protocol) -> None:
    _settings = json_handler.extract_settings('all')
    width: int = _settings['screen_width']
    height: int = _settings['screen_height']
    world_width: int = _settings['world_width']  # added world width
    world_height: int = _settings['world_height']  # and height
    fps: int = _settings['game_fps']

    eggnemy_entity_limit: int = _settings['eggnemy_cap']
    eggnemy_width: float = _settings['eggnemy_width']
    eggnemy_height: float = _settings['eggnemy_height']
    eggnemy_health: float = _settings['eggnemy_health']  # added enemy health

    egg_health: float = _settings['egg_health']
    egg_width: float = _settings['egg_width']
    egg_height: float = _settings['egg_height']

    boss_spawn_count: int = _settings['boss_spawn_counter']
    boss_health: float = _settings['boss_health']
    boss_width: float = _settings['boss_width']
    boss_height: float = _settings['boss_height']
    attack_range: int = 10

    model = Model(fps, width, height, world_width, world_height, eggnemy_entity_limit, boss_spawn_count, attack_range,
                  # changed dmg to 1 for test purposes
                  EntityConfig(egg_width, egg_height, 2,
                               egg_health, 1, 10, 10),
                  EggnemyConfig(eggnemy_width, eggnemy_height,
                                0.5, eggnemy_health, 1),
                  EggnemyConfig(boss_width, boss_height, 1, boss_health, 3))
    view = View(width, height, world_width, world_height)
    controller = Controller(model, view)

    controller.start()


if __name__ == '__main__':
    # running this on directory /implementation 1
    main(json_handler('implementation1/settings.json'))
    # so i temporarily removed /implemetation 1
    # just add it back pag ikaw na nagrun

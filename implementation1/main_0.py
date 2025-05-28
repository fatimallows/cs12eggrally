from model import Model, EntityConfig, EggnemyConfig
from controller import Controller
from view import View
from extract_json import json_handler_protocol, json_handler
from typing import Literal
 
 
def main(json_handler: json_handler_protocol) -> None:
    _settings = json_handler.extract_settings('all')
    width: int = _settings['world_width']
    height: int = _settings['world_height']
    fps: int = _settings['game_fps']
    eggnemy_width: float = _settings['eggnemy_width']
    eggnemy_height: float = _settings['eggnemy_height']
    egg_health: float = _settings['egg_health']
    egg_width: float = _settings['egg_width']
    egg_height: float = _settings['egg_height']
    eggnemy_entity_limit: int = _settings['eggnemy_cap']
    attack_range: int = 10
 
    model = Model(fps, width, height, eggnemy_entity_limit, attack_range, 
                  EntityConfig(egg_width, egg_height, 2, egg_health, 2, 10, 10), 
                  EggnemyConfig(eggnemy_width, eggnemy_height, 0.5, egg_health, 1))
    view = View(width, height)
    controller = Controller(model, view)
 
    controller.start()
 
 
if __name__ == '__main__':
    # "game_fps": 30,
    # "world_width": 200,
    # "world_height": 300,
    # "egg_health": 100,
    # "egg_width": 10,
    # "egg_height": 30,
    # "eggnemy_cap": 10,
    # "eggnemy_width": 10,
    # "eggnemy_height": 30
    main(json_handler('implementation1/settings.json'))
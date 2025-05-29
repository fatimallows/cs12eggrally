from model import Model, EntityConfig, EggnemyConfig
from controller import Controller
from view import View
from extract_json import json_handler_protocol, json_handler
from typing import Literal
 
 
def main(json_handler: json_handler_protocol) -> None:
    _settings = json_handler.extract_settings('all')
    width: int = _settings['screen_width']
    height: int = _settings['screen_height']
    world_width: int = _settings['world_width'] # added world width
    world_height: int = _settings['world_height'] # and height
    fps: int = _settings['game_fps']
    eggnemy_width: float = _settings['eggnemy_width']
    eggnemy_height: float = _settings['eggnemy_height']
    egg_health: float = _settings['egg_health']
    egg_width: float = _settings['egg_width']
    egg_height: float = _settings['egg_height']
    eggnemy_health: float = _settings['eggnemy_health'] # added enemy health
    eggnemy_entity_limit: int = _settings['eggnemy_cap']
    attack_range: int = 10
 
    # model = Model(0, 0, fps, width, height, eggnemy_entity_limit, attack_range, 
    #               EntityConfig(egg_width, egg_height, 2, egg_health, 2, 10, 10), 
    #               EggnemyConfig(eggnemy_width, eggnemy_height, 0.5, egg_health, 1))
    view = View(width, height)
    model = Model(0, 0, fps, width, height, world_width, world_height, eggnemy_entity_limit, attack_range, 
                  EntityConfig(egg_width, egg_height, 2, egg_health, 1, 10, 10),  # changed dmg to 1 for test purposes
                  EggnemyConfig(eggnemy_width, eggnemy_height, 0.5, eggnemy_health, 1))
    # view = View(width, height, world_width, world_height)
    controller = Controller(model, view)
 
    controller.start()
 
 
if __name__ == '__main__':
    main(json_handler('settings.json')) # running this on directory /implementation 1
                                        # so i temporarily removed /implemetation 1
                                        # just add it back pag ikaw na nagrun
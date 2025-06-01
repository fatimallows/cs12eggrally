from _model import Model
from _view import View
from _controller import Controller
from _extract_json import json_handler, json_handler_protocol


def main(json_handler: json_handler_protocol) -> None:
    _settings = json_handler.extract_settings('all')
    width: int = _settings['screen_width']
    height: int = _settings['screen_height']
<<<<<<< HEAD
    world_width: int = _settings['world_width']  # added world width
    world_height: int = _settings['world_height']  # and height

    model = Model(screen_width=width,
                  screen_height=height,
                  world_width=world_width,
                  world_height=world_height,)
||||||| 1e24f34
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
=======
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
    boss_spawn_count: int = _settings['boss_spawn_counter']
    boss_health: float = _settings['boss_health']
    boss_width: float = _settings['boss_width']
    boss_height: float = _settings['boss_height']
    xp_threshold: float=_settings["eggxperience_threshold"],
    egghancement_hp: float =_settings["egghancement_max_hp_increase"],
    egghancement_atk: float=_settings["egghancement_attack_increase"],
    egghancement_spd: float =_settings["egghancement_speed_increase"]     
    
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
            ),
        xp_threshold=xp_threshold,
        egghancement_hp=egghancement_hp,
        egghancement_atk=egghancement_atk,
        egghancement_spd=egghancement_spd,     
    )
>>>>>>> 324971d7a3a9be0fc48ba7e9cb3973e4463671f5
    view = View(screen_width=width,
                screen_height=height,
                world_width=world_width,
                world_height=world_height,)
    controller = Controller(model, view)

    controller.start()


if __name__ == "__main__":
    main(json_handler('implementation1.1/_settings.json'))

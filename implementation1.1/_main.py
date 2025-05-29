from _model import Model
from _view import View
from _controller import Controller
from _project_types import EggConfig, Hitbox
from _helpers import CartesianPoint

def main() -> None:
    model = Model(
        fps=30,
        screen_width=200,
        screen_height=200,
        world_width=100,
        world_height=100,
        eggnemy_entity_limit=10,
        eggnemy_kills_boss_trigger=20,
        egg_config=EggConfig(
            hitbox=Hitbox(
                _coordinate=CartesianPoint(100, 100),
                _width=20,
                _height=20),
            movement_speed=2,
            max_health=10,
            base_damage=1,
            damage_hitbox_scale=1.3,
            invincibility_frames=30,
            ),
        eggnemy_config=EggConfig(
            hitbox=Hitbox(
                _coordinate=CartesianPoint(100, 100),
                _width=10,
                _height=10),
            movement_speed=0.5,
            max_health=5,
            base_damage=1,
            damage_hitbox_scale=1,
            invincibility_frames=0
            ),
        boss_eggnemy_config=EggConfig(hitbox=Hitbox(
                _coordinate=CartesianPoint(100, 100),
                _width=30,
                _height=30),
            movement_speed=1,
            max_health=30,
            base_damage=3,
            damage_hitbox_scale=1,
            invincibility_frames=0
            )        
    )
    view = View(screen_width=200,
        screen_height=200,
        world_width=100,
        world_height=100,)
    controller = Controller(model, view)
    
    controller.start()
    
if __name__ == "__main__":
    main()
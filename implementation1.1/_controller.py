import pyxel

from _model import Model
from _project_types import Keybinds
from _egg_entities import Eggnemy
from _view import View
from _view_types import (
    PyxelObjectModel,)  # ContentObject, FloatObject, RootObject)
from _leaderboard import load_leaderboard, save_leaderboard

class Controller():
    def __init__(self, settings: dict):
        self._settings = settings
        self._init_from_settings(settings)

    def _init_from_settings(self, settings: dict):
        from _model import Model
        from _view import View
        from _view_types import PyxelObjectModel
        from _egg_entities import Eggnemy
        from _project_types import InitEggConfig

        self._model = Model(
            fps=settings['game_fps'],
            screen_width=settings['screen_width'],
            screen_height=settings['screen_height'],
            world_width=settings['world_width'],
            world_height=settings['world_height'],
            eggnemy_entity_limit=settings['eggnemy_cap'],
            eggnemy_kills_boss_trigger=settings['boss_spawn_counter'],
            egg_config=InitEggConfig(
                _width=settings['egg_width'],
                _height=settings['egg_height'],
                movement_speed=2,
                max_health=settings['egg_health'],
                base_damage=1,
                damage_hitbox_scale=2,
                invincibility_frames=settings['game_fps'] * 1,
            ),
            eggnemy_config=InitEggConfig(
                _width=settings['eggnemy_width'],
                _height=settings['eggnemy_height'],
                movement_speed=0.5,
                max_health=settings['eggnemy_health'],
                base_damage=1,
                damage_hitbox_scale=1,
                invincibility_frames=0,
            ),
            boss_eggnemy_config=InitEggConfig(
                _width=settings['boss_width'],
                _height=settings['boss_height'],
                movement_speed=1,
                max_health=settings['boss_health'],
                base_damage=3,
                damage_hitbox_scale=1,
                invincibility_frames=0,
            ),
        )
        self._view = View(
            screen_width=settings['screen_width'],
            screen_height=settings['screen_height'],
            world_width=settings['world_width'],
            world_height=settings['world_height'],
            fps=settings['game_fps']
        )
        self._pyxel_object_model = PyxelObjectModel(
            self._model.screen_width, self._model.screen_height
        )

    def start(self):
        model = self._model

        self._view.start(model.fps, self, self)

    def update(self):
        keybinds = Keybinds(
            up=pyxel.btn(pyxel.KEY_W),
            down=pyxel.btn(pyxel.KEY_S),
            left=pyxel.btn(pyxel.KEY_A),
            right=pyxel.btn(pyxel.KEY_D),
            attack=pyxel.btn(pyxel.KEY_L),
        )
        if pyxel.btnp(pyxel.KEY_Q):  # quit
            self.reset_leaderboard()
            pyxel.quit()
        if self._model.is_game_over and not self._model.egg.is_dead:
            self._view.draw_end(self._model.egg.hitbox, "YOU WIN")
            if self._model.elapsed_frames > 0:
                self._record_leaderboard_entry(self._model.elapsed_frames)

        if self._model.is_game_over and pyxel.btnp(pyxel.KEY_R):
            self._restart_game()
            return
        self._model.update(keybinds)

    def draw(self):
        self._view.clear_screen()

        # print([a.eggnemy.hitbox for a in self._model._eggnemy_list._eggnemy_list])

        # print(self._model.egg.hitbox)
        # print(self._model.eggnemy_list.eggnemy_list[0].eggnemy.hitbox)

        # holy shit it works
        # egg_rally_object = self._pyxel_object_model.generate_float_object(
        #     self._model.screen_width, (self._model.screen_height * 2) // 3, 'self', {'egg_rally_object'})
        # leaderboard_object = self._pyxel_object_model.generate_float_object(
        #     self._model.screen_width, self._model.screen_height // 3, 'self', {
        #         'leaderboard_object'}
        # )
        # leaderboard_object.float_to(
        #     egg_rally_object.reference_point['x'], (self._model.screen_height * 2) // 3)

        # self._pyxel_object_model.add_child_current_object(egg_rally_object)
        # self._pyxel_object_model.add_child_current_object(leaderboard_object)

        # self._view.draw_object_box(
        #     self._pyxel_object_model.root, pyxel.COLOR_GRAY)
        # self._pyxel_object_model.go_to_node_with_tag('egg_rally_object')
        # self._view.draw_object_box(
        #     self._pyxel_object_model.current_object, pyxel.COLOR_GREEN)
        # self._pyxel_object_model.go_to_node_with_tag('leaderboard_object')
        # self._view.draw_object_box(
        #     self._pyxel_object_model.current_object, pyxel.COLOR_CYAN)

        self._view.draw_border(self._model.world_right, self._model.world_left, self._model.world_top,
                               self._model.world_bottom, self._model.world_width, self._model.world_height)
        self._view.draw_information(
            self._model.elapsed_frames, self._model.fps, self._model.eggnemies_killed)

        self._view.draw_leaderboard(self._model._leaderboard)
        # self._view.draw_hitbox(self._model._egg._damage_hitbox, pyxel.COLOR_YELLOW)
        self._view.draw_hitbox(self._model.egg.hitbox, pyxel.COLOR_WHITE)
        self._view.draw_health(self._model.egg, 11)

        self._model._eggnemy_list.update_list(self._draw_eggmemy)

        if self._model.is_game_over and not self._model.egg.is_dead:
            self._view.draw_end(self._model.egg.hitbox, "YOU WIN")

        if self._model.is_game_over and self._model.egg.is_dead:
            self._view.draw_end(self._model.egg.hitbox, "YOU LOSE")

    def _draw_eggmemy(self, eggnemy: Eggnemy):
        # self._view.draw_hitbox(eggnemy._damage_hitbox, pyxel.COLOR_YELLOW)
        self._view.draw_hitbox(eggnemy.hitbox, pyxel.COLOR_GRAY)
        self._view.draw_health(eggnemy, 8)

    def _restart_game(self):
        self._init_from_settings(self._settings)

    def _record_leaderboard_entry(self, time_in_frames: int):
        self._model._leaderboard.append(time_in_frames)
        self._model._leaderboard = sorted(self._model._leaderboard)[:3]  # lmao the emoji keep top 3
        save_leaderboard(self._model._leaderboard)

    def reset_leaderboard(self):
        self._model._leaderboard = []
        save_leaderboard(self._model._leaderboard)
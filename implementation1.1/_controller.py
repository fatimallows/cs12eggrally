import pyxel

from _model import Model
from _project_types import Keybinds
from _egg_entities import Eggnemy
from _view import View
from _view_types import (
    PyxelObjectModel,)  # ContentObject, FloatObject, RootObject)


class Controller():
    def __init__(self, model: Model, view: View):
        self._model = model
        self._view = view
        self._pyxel_object_model = PyxelObjectModel(
            self._model.screen_width, self._model.screen_height)

        # egg_rally_object = self._pyxel_object_model.generate_float_object(
        #     self._model.screen_width, (self._model.screen_height * 2) // 3, 'self', ['egg_rally_object'])
        # leaderboard_object = self._pyxel_object_model.generate_float_object(
        #     self._model.screen_width, self._model.screen_height // 3, 'self', [
        #         'leaderboard_object']
        # )
        # leaderboard_object.float_to(
        #     egg_rally_object.reference_point['x'], (self._model.screen_height * 2) // 3)

        # self._pyxel_object_model.add_child_current_object(egg_rally_object)
        # self._pyxel_object_model.add_child_current_object(leaderboard_object)

    def start(self):
        model = self._model

        self._view.start(model.fps, self, self)

    def update(self):
        keybinds = Keybinds(
            up=pyxel.btn(pyxel.KEY_W),
            down=pyxel.btn(pyxel.KEY_S),
            left=pyxel.btn(pyxel.KEY_A),
            right=pyxel.btn(pyxel.KEY_D),
            attack=pyxel.btn(pyxel.KEY_L)
        )

        self._model.update(keybinds)

    def draw(self):
        self._view.clear_screen()

        # print([a.eggnemy.hitbox for a in self._model._eggnemy_list._eggnemy_list])

        # print(self._model.egg.hitbox)
        # print(self._model.eggnemy_list.eggnemy_list[0].eggnemy.hitbox)

        # holy shit it works

        # self._view.draw_object_box(
        #     self._pyxel_object_model.root, pyxel.COLOR_GRAY)
        # self._pyxel_object_model.go_to_node_with_tag('egg_rally_object')
        # self._view.draw_object_box(
        #     self._pyxel_object_model.current_object, pyxel.COLOR_GRAY)
        # self._pyxel_object_model.go_to_node_with_tag('leaderboard_object')
        # self._view.draw_object_box(
        #     self._pyxel_object_model.current_object, pyxel.COLOR_CYAN)

        self._view.draw_border(self._model.world_right, self._model.world_left, self._model.world_top,
                               self._model.world_bottom, self._model.world_width, self._model.world_height)
        self._view.draw_information(
            self._model.elapsed_frames, self._model.fps, self._model.eggnemies_killed)

        # self._view.draw_hitbox(
        #     self._model._egg._damage_hitbox, pyxel.COLOR_YELLOW)
        self._view.draw_hitbox(self._model.egg.hitbox, pyxel.COLOR_WHITE)
        self._view.draw_health(self._model.egg)

        self._model._eggnemy_list.update_list(self._draw_eggmemy)

        if self._model.is_game_over and not self._model.egg.is_dead:
            self._view.draw_end(self._model.egg.hitbox, "YOU WIN")

        if self._model.is_game_over and self._model.egg.is_dead:
            self._view.draw_end(self._model.egg.hitbox, "YOU LOSE")

    def _draw_eggmemy(self, eggnemy: Eggnemy):
        # self._view.draw_hitbox(eggnemy._damage_hitbox, pyxel.COLOR_YELLOW)
        self._view.draw_hitbox(eggnemy.hitbox, pyxel.COLOR_GRAY)
        self._view.draw_health(eggnemy)

import pyxel

from egg_rally.model import Model
from egg_rally.project_types import Keybinds
from egg_rally.egg_entities import Eggnemy
from egg_rally.view import View
from egg_rally.leaderboard import save_leaderboard


class Controller():
    def __init__(self, model: Model, view: View):
        self._model = model
        self._view = view

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
            restart=pyxel.btnp(pyxel.KEY_R),
            quit=pyxel.btnp(pyxel.KEY_Q),
        )
        if self._model.is_game_over and not self._model.egg.is_dead:
            self._view.draw_end(self._model.egg.hitbox, "YOU WIN")
            # if self._model.elapsed_frames > 0:
            #     self._record_leaderboard_entry(self._model.elapsed_frames)

            # if self._model.is_game_over and pyxel:
            #     self._restart_game()
            #     return
        self._model.update(keybinds)

        if self._model.stop_game:
            pyxel.quit()

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

import pyxel

from egg_rally.model import Model
from egg_rally.project_types import Keybinds
from egg_rally.egg_entities import Eggnemy
from egg_rally.view import View
from egg_rally.leaderboard import save_leaderboard

# from egg_rally.helpers import Vector, CartesianPoint


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

        # eggahancement
        if self._model.in_enhancement_menu:
            if pyxel.btnp(pyxel.KEY_W):
                self._model.selected_enhancement_index = (
                    self._model.selected_enhancement_index - 1) % len(self._model.enhancement_options)
            elif pyxel.btnp(pyxel.KEY_S):
                self._model.selected_enhancement_index = (
                    self._model.selected_enhancement_index + 1) % len(self._model.enhancement_options)

            if pyxel.btnp(pyxel.KEY_1):
                self._model.apply_enhancement(0)
            elif pyxel.btnp(pyxel.KEY_2):
                self._model.apply_enhancement(1)
            elif pyxel.btnp(pyxel.KEY_3):
                self._model.apply_enhancement(2)

        if self._model.stop_game:
            save_leaderboard(self._model.leaderboard)
            pyxel.quit()

        self._model.update(keybinds)

    def draw(self):
        self._view.clear_screen()

        self._view.draw_border(self._model.world_right, self._model.world_left, self._model.world_top,
                               self._model.world_bottom, self._model.world_width, self._model.world_height)
        self._view.draw_information(
            self._model.elapsed_frames, self._model.fps, self._model.eggnemies_killed)

        self._view.draw_egg_stats(
            atk=self._model.egg.base_damage,
            spd=self._model.egg.movement_speed,
            eggxperience=self._model.egg.eggxperience,
            eggxperience_required=self._model.egg.xp_threshold
        )

        self._view.draw_leaderboard(self._model._leaderboard)
        # self._view.draw_hitbox(self._model._egg._damage_hitbox, pyxel.COLOR_YELLOW)
        self._view.draw_hitbox(self._model.egg.hitbox, pyxel.COLOR_WHITE)
        self._view.draw_health(self._model.egg, 11)

        self._model._eggnemy_list.update_list(self._draw_eggmemy)

        if self._model.is_game_over and not self._model.egg.is_dead:
            self._view.draw_end(self._model.egg.hitbox, "YOU WIN")

        if self._model.is_game_over and self._model.egg.is_dead:
            self._view.draw_end(self._model.egg.hitbox, "YOU LOSE")\

        if self._model.in_enhancement_menu:
            self._view.draw_enhancement_screen(
                self._model.enhancement_options, self._model.selected_enhancement_index)

    def _draw_eggmemy(self, eggnemy: Eggnemy):
        # self._view.draw_hitbox(eggnemy._damage_hitbox, pyxel.COLOR_YELLOW)
        self._view.draw_hitbox(eggnemy.hitbox, pyxel.COLOR_GRAY)
        self._view.draw_health(eggnemy, 8)

        # c1 = eggnemy.hitbox.center
        # v = eggnemy.test_only_move_velocity
        # c2 = c1.convert_to_vector() + v * 20
        # pyxel.line(c1.x, c1.y, c2.x_hat, c2.y_hat, pyxel.COLOR_YELLOW)
        # pyxel.text(
        #     c1.x + 5, c1.y, f"{((eggnemy.test_only_move_velocity.x_hat * 1000) // 10) / 100}", pyxel.COLOR_YELLOW, None)
        # pyxel.text(
        #     c1.x, c1.y - 5, f"{((eggnemy.test_only_move_velocity.y_hat * 1000) // 10) / 100}", pyxel.COLOR_YELLOW, None)

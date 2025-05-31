import pyxel

from _model import Model
from _project_types import Keybinds
from _egg_entities import Eggnemy
from _view import View

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
            attack=pyxel.btn(pyxel.KEY_L)
        )
        
        self._model.update(keybinds)
        
    def draw(self):
        self._view.clear_screen()
        
        # print([a.eggnemy.hitbox for a in self._model._eggnemy_list._eggnemy_list])
        
        # print(self._model.egg.hitbox)
        # print(self._model.eggnemy_list.eggnemy_list[0].eggnemy.hitbox)
        
        self._view.draw_border(self._model.world_right, self._model.world_left, self._model.world_top, self._model.world_bottom, self._model.world_width, self._model.world_height)
        self._view.draw_information(self._model.elapsed_frames, self._model.fps, self._model.eggnemies_killed)
        
        # self._view.draw_hitbox(self._model._egg._damage_hitbox, pyxel.COLOR_YELLOW)
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
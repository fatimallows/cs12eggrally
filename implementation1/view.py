import pyxel
from model import Model
from project_types import (
    UpdateHandler, DrawHandler,
)
from egg_entities import (
    Entity, EggEntity, EggnemyEntity
)
# from project_types import UpdateHandler, DrawHandler, PipePairInfo, BirdInfo

class View:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        
    def start(self, fps: int, update_handler: UpdateHandler, draw_handler: DrawHandler) -> None:
        pyxel.init(self._width, self._height, fps=fps)
        pyxel.run(update_handler.update, draw_handler.draw)
        
    def clear_screen(self) -> None:
        pyxel.cls(0)
        
    def was_w_just_pressed(self) -> bool:
        return pyxel.btn(pyxel.KEY_W) 

    def was_a_just_pressed(self) -> bool:
        return pyxel.btn(pyxel.KEY_A)
    
    def was_s_just_pressed(self) -> bool:
        return pyxel.btn(pyxel.KEY_S)
    
    def was_d_just_pressed(self) -> bool:
        return pyxel.btn(pyxel.KEY_D)
    
    def was_l_just_pressed(self) -> bool:
        return pyxel.btn(pyxel.KEY_L)

    # game over draw
    # this isnt FUCKING WORKINGG
    def draw(self, model: Model) -> None:
        self.clear_screen()
        print("Drawing frame. Game over status:", model.is_game_over) 
        if model.is_game_over:
            # draw game over popup only
            box_width = 100
            box_height = 40
            box_x = (self._width - box_width) // 2
            box_y = (self._height - box_height) // 2

            # draw white box
            pyxel.rect(box_x, box_y, box_width, box_height, pyxel.COLOR_WHITE)
            # draw black border
            pyxel.rectb(box_x, box_y, box_width, box_height, pyxel.COLOR_BLACK)

            # draw centered "GAME OVER" text inside box
            text = "GAME OVER"
            text_x = box_x + (box_width - len(text) * 4) // 2  # pyxel.text char width ~4 px
            text_y = box_y + box_height // 2 - 4  # approx vertical center

            pyxel.text(text_x, text_y, text, pyxel.COLOR_BLACK, None)
        else:
            # draw normal game stuff
            self.draw_egg(model._egg)
            for enemy in model._eggnemies.values():
                self.draw_eggnemy(enemy)

            
    def draw_egg(self, egg: EggEntity) -> None:
        pyxel.rect(egg.x, egg.y, egg.width, egg.height, 1)

        # HP BARRRR
        self.draw_hp_bar(egg)
        
    def draw_eggnemy(self, egg: EggnemyEntity) -> None:
        pyxel.rect(egg.x, egg.y, egg.width, egg.height, 2)
    
    def draw_hp_bar(self, egg: EggEntity) -> None:
        max_hp = 10  # assumed max HP for scale

        # dimesions
        hp_value = int(egg.base_health / (max_hp / 10))
        hp_text = f"{hp_value}/10"
        text_width = len(hp_text) * 4 

        # position below the egg
        padding = 2
        text_x = egg.x + (egg.width - text_width) // 2
        text_y = egg.y + egg.height + padding

        # hp bar settings based on text width
        bar_width = text_width
        bar_height = 2
        hp_ratio = egg.base_health / max_hp
        filled_width = int(bar_width * hp_ratio)

        
        bar_x = text_x
        bar_y = text_y + 8  # below text

        pyxel.text(text_x, text_y, hp_text, 7, None)  # white
        pyxel.rect(bar_x, bar_y, bar_width, bar_height, 5)  # background: gray
        pyxel.rect(bar_x, bar_y, filled_width, bar_height, 11)  # foreground: green
    
# class View:
#     def __init__(self, width: int, height: int):
#         self._width = width
#         self._height = height
 
#     def start(self, fps: int, update_handler: UpdateHandler, draw_handler: DrawHandler):
#         pyxel.init(self._width, self._height, fps=fps)
#         pyxel.run(update_handler.update, draw_handler.draw)
 
#     def was_spacebar_just_pressed(self):
#         return pyxel.btnp(pyxel.KEY_SPACE)
 
#     def clear_screen(self):
#         pyxel.cls(0)
 
#     def draw_pipes(self, pipes: Sequence[PipePairInfo]):
#         for pipe_pair in pipes:
#             for pipe in [pipe_pair.top_pipe, pipe_pair.bottom_pipe]:
#                 pyxel.rect(pipe.x, pipe.y, pipe.width, pipe.height, 4)
 
#     def draw_bird(self, bird: BirdInfo):
#         pyxel.circ(bird.x, bird.y, bird.radius, 2)
 
#     def draw_score(self, score: int):
#         pyxel.text(self._width // 2 - 3, 10, str(score), 7)
 
#     def draw_game_over(self):
#         pyxel.text(self._width // 2 - 15, self._height // 2, "Game over", 7)
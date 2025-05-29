import pyxel
from extract_json import json_handler
from model import Model
from project_types import (
    UpdateHandler, DrawHandler,
)
from egg_entities import (
    Entity, EggEntity, EggnemyEntity
)
# from project_types import UpdateHandler, DrawHandler, PipePairInfo, BirdInfo

class View:
    def __init__(self, width: int, height: int, world_width: int, world_height: int) -> None:
        self._width = width
        self._height = height
        self._world_width = world_width
        self._world_height = world_height # added world height and width
        
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

        # thus is for time...
        elapsed = model.get_elapsed_time_formatted()
        timer_text = f"Time: {elapsed}"
        eggnemies_killed_text = f"Eggnemies killed: {model.eggnemies_killed}"
        
        timer_width = len(timer_text) * 5  # pixel  
        eggnemies_killed_width = len(eggnemies_killed_text) * 5 # 5??
        x_timer = pyxel.width - timer_width - 2  # padding from the right
        x_eggnemies_killed = pyxel.width - eggnemies_killed_width
        y = 7

        pyxel.text(x_timer, y, timer_text, 7, None)
        pyxel.text(x_eggnemies_killed, 2 * y, eggnemies_killed_text, 7, None)
        

        # for centering the cam
        if model._egg is not None:
            ox = (self._width - model._egg.width) // 2 
            oy = (self._height - model._egg.height) // 2
            # print(f"({model._egg.x} - {self._width // 2}, {model._egg.y} - {self._height // 2})")
            print(f"({ox}, {oy})")
            
        else:
            ox = 0
            oy = 0

        self.draw_world_border(model)
        
        if model._egg is not None:
            offset_x, offset_y = self.compute_camera_offset(
                model._egg, model._world_width, model._world_height
            )
            
            self.draw_egg(model._egg, offset_x, offset_y) # for camera offset PLEASE WORK 

            for eggnemy in model._eggnemies.values():
                self.draw_eggnemy(eggnemy, offset_x, offset_y)
            
            
        # working game over screen
        # print("Drawing frame. Game over status:", model.is_game_over) 
        
        if model._egg is None:
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
        # else:
        #     # draw normal game stuff
        #     self.draw_egg(model._egg, offset_x, offset_y)
        #     # for enemy in model._eggnemies.values():
        #     #     self.draw_eggnemy(enemy, offset_x, offset_y)
        # pyxel.circ(self._width // 2, self._height // 2, 2, pyxel.COLOR_LIME)

            
            
    def draw_egg(self, egg: EggEntity, ox: int, oy: int) -> None:
        pyxel.rect(egg.x - ox, egg.y - oy, egg.width, egg.height, 7)
         
        # HP BARR
        self.draw_hp_bar(egg, ox, oy)

    def draw_eggnemy(self, enemy: EggnemyEntity, ox: int, oy: int) -> None:
        pyxel.rect(enemy.x - ox, enemy.y - oy, enemy.width, enemy.height, 13)

        # ENEMY HP
        self.draw_hp_bar(enemy, ox, oy, color=8)


    # made it dynamic (to accommodate every entity incld eggnemies and bosses)
    # changes color !
    def draw_hp_bar(self, entity: Entity, ox: int, oy: int, color: int = 11) -> None:
        # dimesions
        hp_text = f"{entity.base_health}/{entity.max_health}"
        text_width = len(hp_text) * 4 

        # position below the egg
        padding = 2
        text_x = entity.x - ox + (entity.width - text_width) // 2
        text_y = entity.y - oy + entity.height + padding

        # hp bar settings based on text width
        bar_width = text_width
        bar_height = 2
        hp_ratio = entity.base_health / entity.max_health
        filled_width = int(bar_width * hp_ratio)

        
        bar_x = text_x
        bar_y = text_y + 8  # below text

        pyxel.text(text_x, text_y, hp_text, 7, None)  # white
        pyxel.rect(bar_x, bar_y, bar_width, bar_height, 5)  # background: gray
        pyxel.rect(bar_x, bar_y, filled_width, bar_height, color)  # foreground: green
    

    def draw_world_border(self, model: Model):
    # def draw_world_border(self, model: Model):
    
        border_color = pyxel.COLOR_WHITE
        thickness = 1
        
        num_x_gridlines: int = 5
        num_y_gridlines: int = 5
        
        x_gridline_spacing: int = int(model._world_width) // num_x_gridlines
        y_gridline_spacing: int = int(model._world_height) // num_y_gridlines

        for i in range(num_x_gridlines):
            x_coord =  i*x_gridline_spacing + model.world_left
            pyxel.line(x_coord, model.world_top, x_coord, model.world_bottom, pyxel.COLOR_LIGHT_BLUE)
            
        for i in range(num_y_gridlines):
            y_coord = i*y_gridline_spacing + model.world_top
            pyxel.line(model.world_left, y_coord, model.world_right, y_coord, pyxel.COLOR_LIGHT_BLUE)
        
        # top
        pyxel.rect(model.world_x, model.world_y, model._world_width, thickness, border_color)
        # bottom
        pyxel.rect(model.world_x, model._world_height + model.world_y, model._world_width, thickness, border_color)
        # left
        pyxel.rect(model.world_x, model.world_y, thickness, model._world_height, border_color)
        # right
        pyxel.rect(model._world_width + model.world_x, model.world_y, thickness, model._world_height, border_color)

        # top
        # pyxel.rect(model.world_left, model.world_top, model._world_width, thickness, border_color)
        # bottom
        # pyxel.rect(model.world_left, model.world_bottom - thickness, model._world_width, thickness, border_color)
        # left
        # pyxel.rect(-ox, -oy, thickness, world_height, border_color)
        # right
        # pyxel.rect(world_width - thickness - ox, -oy, thickness, world_height, border_color)

    def compute_camera_offset(self, egg: EggEntity, world_width: int, world_height: int) -> tuple[int, int]:
        half_width = self._width // 2
        half_height = self._height // 2

        # center camera on egg
        ox = (egg.x + egg.width // 2) - half_width
        oy = (egg.y + egg.height // 2) - half_height
        
        # ox = (egg.width - self._width) // 2
        # oy = (egg.height - self._height) // 2


        return ox, oy
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
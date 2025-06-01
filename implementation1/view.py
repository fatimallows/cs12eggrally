import pyxel
from extract_json import json_handler
from model import Model
from project_types import (
    UpdateHandler, DrawHandler,
)
from egg_entities import (
    Entity, EggEntity, EggnemyEntity, BossEntity
)
# from project_types import UpdateHandler, DrawHandler, PipePairInfo, BirdInfo

class View:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self.pyxelW = 256
        self.pyxelH = 256
        
    
    def start(self, fps: int, update_handler: UpdateHandler, draw_handler: DrawHandler) -> None:
        pyxel.init(self.pyxelW,  self.pyxelH, title="Egg Rally!", fps=fps, capture_scale=3)
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
        cam_x, cam_y = 0, 0

        # phase 0 specs technically
        if model._egg is not None:
            cam_x, cam_y = 0, 0
            cam_x = model._egg.x - self.pyxelW // 2 + model._egg.width // 2
            cam_y = model._egg.y - self.pyxelH // 2 + model._egg.height // 2
            # world border
            pyxel.rectb(-cam_x, -cam_y, model._width, model._height, pyxel.COLOR_WHITE)
            

            self.draw_egg(model._egg, cam_x, cam_y)
            
            for enemy in model._eggnemies.values():
                if enemy.is_dead:
                    continue
                screen_x = enemy.x - cam_x
                screen_y = enemy.y - cam_y
                if -enemy.width < screen_x < self.pyxelW and -enemy.height < screen_y < self.pyxelH:
                    self.draw_eggnemy(enemy, cam_x, cam_y)
            
        #working game over screen
        print("Drawing frame. Game over status:", model.is_game_over) 
        
        if model.is_game_over:
            if model._egg.is_dead:
                # draw game over popup only
                model.is_game_over = True
                box_width = 100
                box_height = 40
                box_x = (self.pyxelW - box_width) // 2
                box_y = (self.pyxelH - box_height) // 2

                # draw white box
                pyxel.rect(box_x, box_y, box_width, box_height, pyxel.COLOR_WHITE)

                # draw black border
                pyxel.rectb(box_x, box_y, box_width, box_height, pyxel.COLOR_BLACK)

                # draw centered "GAME OVER" text inside box
                text = "GAME OVER"
                text_x = box_x + (box_width - len(text) * 4) // 2  # pyxel.text char width ~4 px
                text_y = box_y + box_height // 2 - 4  # approx vertical center

                print(box_height, box_width, box_x, box_y)

                pyxel.text(text_x, text_y, text, pyxel.COLOR_BLACK, None)
                return

            # please be over
            elif model.has_won:
                egg = model._egg
                screen_x = egg.x - cam_x + egg.width // 2 - len("YOU WIN!") * 2
                screen_y = egg.y - cam_y - 10  # slightly above egg
                pyxel.text(screen_x, screen_y, "YOU WIN!", pyxel.COLOR_YELLOW)
                return

        # convert frames to mm:ss
        total_seconds = model.timer_frames // 30
        minutes = total_seconds // 30
        seconds = total_seconds % 30
        timer_text = f"{minutes:02}:{seconds:02}"

        # draw at top-right (adjust x if needed)
        pyxel.text(pyxel.width - 30, 10, timer_text, 7)

        # draw score
        score_text = f'{model.eggnemies_killed}'
        pyxel.text(15, 10, score_text, 7)

            
    def draw_egg(self, egg: EggEntity, cam_x: int, cam_y: int) -> None:
        screen_x = egg.x - cam_x 
        screen_y = egg.y - cam_y
        pyxel.rect(screen_x, screen_y, egg.width, egg.height, 7)
        # HP BARRRR
        self.draw_hp_bar(egg, cam_x, cam_y)

        
    def draw_eggnemy(self, egg: EggnemyEntity, cam_x: int, cam_y: int) -> None:
        if isinstance(egg, BossEntity):
            pyxel.rect(egg.x - cam_x, egg.y - cam_y, egg.width, egg.height, 8)
        else:
            pyxel.rect(egg.x - cam_x, egg.y - cam_y, egg.width, egg.height, 13)
        self.draw_hp_bar(egg, cam_x, cam_y)
    

    def draw_hp_bar(self, egg: EggEntity, cam_x: int, cam_y: int) -> None:
        # dimesions
        hp_text = f"{egg.base_health}/{egg.max_health}"
        text_width = len(hp_text) * 4 

        # position below the egg
        padding = 2
        text_x = egg.x - cam_x + (egg.width - text_width) // 2
        text_y = egg.y - cam_y + egg.height + padding


        # hp bar settings based on text width
        bar_width = text_width
        bar_height = 2
        hp_ratio = egg.base_health / egg.max_health
        filled_width = int(bar_width * hp_ratio)

        
        bar_x = text_x
        bar_y = text_y + 8  # below text

        pyxel.text(text_x, text_y, hp_text, 7, None)  # white
        pyxel.rect(bar_x, bar_y, bar_width, bar_height, 5)  # background: gray
        if isinstance(egg, EggnemyEntity):   
            pyxel.rect(bar_x, bar_y, filled_width, bar_height, 4)  # foreground: red
        else:
            pyxel.rect(bar_x, bar_y, filled_width, bar_height, 11)  # foreground: green
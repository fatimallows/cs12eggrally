import pyxel
 
# from project_types import UpdateHandler, DrawHandler, PipePairInfo, BirdInfo

class View:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        
    def start(self, fps: int, update_handler, draw_handler):
        pyxel.init(self._width, self._height, fps=fps)
        pyxel.run(update_handler.update, draw_handler.draw)
        
    def clear_screen(self):
        pyxel.cls(0)
        
    def was_w_just_pressed(self):
        return pyxel.btn(pyxel.KEY_W)

    def was_a_just_pressed(self):
        return pyxel.btn(pyxel.KEY_A)
    
    def was_s_just_pressed(self):
        return pyxel.btn(pyxel.KEY_S)
    
    def was_d_just_pressed(self):
        return pyxel.btn(pyxel.KEY_D)
    
    def was_l_just_pressed(self):
        return pyxel.btn(pyxel.KEY_L)
    
    def draw_egg(self, egg):
        pyxel.rect(egg.x, egg.y, egg.width, egg.height, 1)
        
    def draw_eggnemy(self, egg):
        pyxel.rect(egg.x, egg.y, egg.width, egg.height, 2)
    
 
 
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
from model import Model, IsKeyPressed
from view import View


class Controller:
    def __init__(self, model: Model, view: View):
        self._model = model
        self._view = view
        
    def start(self):
        model = self._model
        
        self._view.start(model._fps, self, self) # fix accessing private var
        
    def update(self):
        is_key_pressed = IsKeyPressed(
            (self._view.was_w_just_pressed(),
             self._view.was_s_just_pressed(),
             self._view.was_a_just_pressed(),
             self._view.was_d_just_pressed()),
            self._view.was_l_just_pressed()
        )
        
        self._model.update(is_key_pressed)
        
        
        if self._model._egg is not None:
            self._model._egg.tick()
        else:
            return
        
        for i_num in self._model._eggnemies:
            self._model._eggnemies[i_num].tick()
        
        
        
    def draw(self):
        self._view.draw(self._model)
        
 
# Controller <: UpdateHandler
# Controller <: DrawHandler
# class Controller:
#     def __init__(self, model: Model, view: View):
#         self._model = model
#         self._view = view
 
#     def start(self):
#         model = self._model
 
#         self._view.start(model.fps, self, self)
 
#     def update(self):
#         self._model.update(self._view.was_spacebar_just_pressed())
 
#     def draw(self):
#         self._view.clear_screen()
 
#         self._view.draw_pipes(self._model.pipes)
#         self._view.draw_bird(self._model.bird)
#         self._view.draw_score(self._model.score)
 
#         if self._model.is_game_over:
#             self._view.draw_game_over()
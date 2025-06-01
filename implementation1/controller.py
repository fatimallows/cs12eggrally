from model import Model, IsKeyPressed
from view import View


class Controller:
    def __init__(self, model: Model, view: View):
        self._model = model
        self._view = view
        
    def start(self):
        model = self._model
        
        self._view.start(model._fps, self, self) # fix accessing private var
        
    def update(self): # and this update function is supposed to be the one that handles most of the thing we were updating in model
        is_key_pressed = IsKeyPressed(
            (self._view.was_w_just_pressed(),
             self._view.was_s_just_pressed(),
             self._view.was_a_just_pressed(),
             self._view.was_d_just_pressed()),
            self._view.was_l_just_pressed()
        )
        
<<<<<<< HEAD
        self._model.update(is_key_pressed)
        
        if self._model.is_game_over:
            return
=======
        curr_model = self._model
        conditions = (curr_model._no_boss_generated, curr_model._is_boss_alive)
                
        if conditions == (False, False):
            return
            
>>>>>>> 62444033178977a8dda0cd316888e59fb533f7f5
        if self._model._egg is not None:
            self._model._egg.tick()
        else:
            return
    
        self._model.update(is_key_pressed)
        
        
        
    def draw(self):
        self._view.draw(self._model) # think we fucked up here, this draw function is supposed to be the one that draws everything
        
 
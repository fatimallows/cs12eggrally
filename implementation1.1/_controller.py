from _model import Model
from _view import View

class Controller():
    def __init__(self, model: Model, view: View):
        self._model = model
        self._view = view
        
    def start(self):
        model = self._model
        
        self._view.start(model.fps, self, self)
        
    def update(self):
        ...
        
    def draw(self):
        ...
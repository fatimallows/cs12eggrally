from model import Model, EntityConfig, EggnemyConfig
from controller import Controller
from view import View
 
 
def main() -> None:
    width: int = 200
    height: int = 200
    fps: int = 30
 
    model = Model(fps, width, height, 10, EntityConfig(10, 10, 2, 10, 2, 10, 10, fps, width, height), 
                  EggnemyConfig(10, 10, 0.5, 10, 1, fps))
    view = View(width, height)
    controller = Controller(model, view)
 
    controller.start()
 
 
if __name__ == '__main__':
    main()
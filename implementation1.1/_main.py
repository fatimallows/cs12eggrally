from _model import Model
from _view import View
from _controller import Controller
from _extract_json import json_handler, json_handler_protocol


def main(json_handler: json_handler_protocol) -> None:
    _settings = json_handler.extract_settings('all')
    width: int = _settings['screen_width']
    height: int = _settings['screen_height']
    world_width: int = _settings['world_width']  # added world width
    world_height: int = _settings['world_height']  # and height

    model = Model(screen_width=width,
                  screen_height=height,
                  world_width=world_width,
                  world_height=world_height,)
    view = View(screen_width=width,
                screen_height=height,
                world_width=world_width,
                world_height=world_height,)
    controller = Controller(model, view)

    controller.start()


if __name__ == "__main__":
    main(json_handler('implementation1.1/_settings.json'))

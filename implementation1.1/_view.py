import pyxel

from _project_types import (UpdateHandler, DrawHandler, Hitbox, EggInfo)
from _view_types import ObjectBox


class View:
    def __init__(self, screen_width: int, screen_height: int, world_width: int, world_height: int) -> None:
        self._screen_width: int = screen_width
        self._screen_height: int = screen_height
        self._world_width: int = world_width
        self._world_height: int = world_height

    def start(self, fps: int, update_handler: UpdateHandler, draw_handler: DrawHandler) -> None:
        pyxel.init(self._screen_width, self._screen_height, fps=fps)

        pyxel.run(update_handler.update, draw_handler.draw)

    def clear_screen(self) -> None:
        pyxel.cls(0)

    def draw_hitbox(self, hitbox: Hitbox, color: int) -> None:
        pyxel.rect(
            x=hitbox.x,
            y=hitbox.y,
            w=hitbox.width,
            h=hitbox.height,
            col=color
        )

    def draw_object_box(self, object_box: ObjectBox, color: int) -> None:
        pyxel.rect(
            x=object_box.reference_point['x'],
            y=object_box.reference_point['y'],
            w=object_box.width,
            h=object_box.height,
            col=color
        )

    def draw_health(self, egg_entity: EggInfo) -> None:
        egg_hitbox = egg_entity.hitbox

        # dimesions
        hp_text = f"{egg_entity.health}/{egg_entity.max_health}"
        text_width = len(hp_text) * 4

        # position below the egg
        padding = 2
        text_x = egg_hitbox.x + (egg_hitbox.width - text_width) // 2
        text_y = egg_hitbox.y + egg_hitbox.height + padding

        # hp bar settings based on text width
        bar_width = text_width
        bar_height = 2
        hp_ratio = egg_entity.health / egg_entity.max_health
        filled_width = int(bar_width * hp_ratio)

        bar_x = text_x
        bar_y = text_y + 8  # below text

        pyxel.text(text_x, text_y, hp_text, pyxel.COLOR_WHITE, None)  # white
        pyxel.rect(bar_x, bar_y, bar_width, bar_height,
                   pyxel.COLOR_GRAY)  # background: gray
        pyxel.rect(bar_x, bar_y, filled_width, bar_height,
                   pyxel.COLOR_GREEN)  # foreground: green

    def draw_information(self, frames_elapsed: int, fps: int, eggnemies_killed: int) -> None:
        total_seconds = frames_elapsed // fps
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        # return f"{minutes:02d}:{seconds:02d}"

        timer_text = f"Time: {minutes:02d}:{seconds:02d}"
        eggnemies_killed_text = f"Eggnemies killed: {eggnemies_killed}"

        timer_width = len(timer_text) * 5  # pixel
        eggnemies_killed_width = len(eggnemies_killed_text) * 5  # 5??
        x_timer = pyxel.width - timer_width - 2  # padding from the right
        x_eggnemies_killed = pyxel.width - eggnemies_killed_width
        y = 7

        pyxel.text(x_timer, y, timer_text, 7, None)
        pyxel.text(x_eggnemies_killed, 2 * y, eggnemies_killed_text, 7, None)

    # def draw_win(self, egg_hitbox: Hitbox) -> None:
    #     text: str = "YOU WIN !"
    #     text_width: int = len(text)

    #     padding = 2
    #     text_x = egg_hitbox.x + ((egg_hitbox.width - text_width) // 2)
    #     text_y = egg_hitbox.y - egg_hitbox.height - padding

    #     pyxel.text(text_x, text_y, text, pyxel.COLOR_YELLOW, None)  # white

    def draw_end(self, egg_hitbox: Hitbox, text: str) -> None:
        box_width = 100
        box_height = 40

        box_x = (self._screen_width - box_width) // 2
        box_y = (self._screen_height - box_height) // 2

        # draw white box
        pyxel.rect(box_x, box_y, box_width, box_height, pyxel.COLOR_WHITE)
        # draw black border
        pyxel.rectb(box_x, box_y, box_width, box_height, pyxel.COLOR_BLACK)

        # draw centered f"{text}" text inside box
        # pyxel.text char width ~4 px
        text_x = box_x + (box_width - len(text) * 4) // 2
        text_y = box_y + box_height // 2 - 4  # approx vertical center

        pyxel.text(text_x, text_y, text, pyxel.COLOR_BLACK, None)

    def draw_border(self, world_right: float, world_left: float, world_top: float, world_bottom: float,
                    world_width: float, world_height: float) -> None:
        border_color = pyxel.COLOR_WHITE
        thickness = 1

        # num_x_gridlines: int = 5
        # num_y_gridlines: int = 5

        # x_gridline_spacing: int = int(model._world_width) // num_x_gridlines
        # y_gridline_spacing: int = int(model._world_height) // num_y_gridlines

        # for i in range(num_x_gridlines):
        #     x_coord =  i*x_gridline_spacing + model.world_left
        #     pyxel.line(x_coord, model.world_top, x_coord, model.world_bottom, pyxel.COLOR_LIGHT_BLUE)

        # for i in range(num_y_gridlines):
        #     y_coord = i*y_gridline_spacing + model.world_top
        #     pyxel.line(model.world_left, y_coord, model.world_right, y_coord, pyxel.COLOR_LIGHT_BLUE)

        # top
        pyxel.rect(world_left, world_top, world_width, thickness, border_color)
        # bottom
        pyxel.rect(world_left, world_bottom,
                   world_width, thickness, border_color)
        # left
        pyxel.rect(world_left, world_top, thickness,
                   world_height, border_color)
        # right
        pyxel.rect(world_right, world_top, thickness,
                   world_height, border_color)

import pyxel

from _project_types import (UpdateHandler, DrawHandler, Hitbox, EggInfo)
from _view_types import ObjectBox


class View:
    def __init__(self, screen_width: int, screen_height: int, world_width: int, world_height: int, fps: int) -> None:
        self._screen_width: int = screen_width
        self._screen_height: int = screen_height
        self._world_width: int = world_width
        self._world_height: int = world_height
        self._fps: int = fps

    def start(self, fps: int, update_handler: UpdateHandler, draw_handler: DrawHandler) -> None:
        pyxel.init(self._screen_width, self._screen_height, fps=fps)
        pyxel.load("eggrally.pyxres")  
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


    def draw_health(self, egg_entity: EggInfo, hp_color: int) -> None:
        egg_hitbox = egg_entity.hitbox

        # dimesions
        hp_text = f"{egg_entity.health}/{egg_entity.max_health}"
        text_width = len(hp_text) * 4

        # position below the egg
        # layout paddings
        padding = 2
        bar_height = 2
        bar_width = text_width

        # positions
        text_x = egg_hitbox.x + (egg_hitbox.width - text_width) // 2
        text_y = egg_hitbox.y + egg_hitbox.height + padding + 6

        bar_x = text_x
        bar_y = text_y + 6  # space between text and bar (approx height of text + padding)

        # health bar fill
        hp_ratio = egg_entity.health / egg_entity.max_health
        filled_width = int(bar_width * hp_ratio)

        # draw
        pyxel.text(text_x, text_y, hp_text, pyxel.COLOR_WHITE)
        pyxel.rect(bar_x, bar_y, bar_width, bar_height, pyxel.COLOR_GRAY)  # background
        pyxel.rect(bar_x, bar_y, filled_width, bar_height, hp_color)       # foreground

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


    def draw_leaderboard(self, leaderboard: list[int]):
        padding = 5
        line_height = 10
        num_lines = 4  # 1 for title, 3 for scores

        start_y = self._screen_height - (num_lines * line_height) - padding

        pyxel.text(padding, start_y, "Top 1", pyxel.COLOR_YELLOW)

        for i in range(3):
            y = start_y + (i + 1) * line_height
            if i < len(leaderboard):
                time = leaderboard[i]
                total_seconds = time // self._fps
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                time_str = f"{minutes:02}:{seconds:02}"
            else:
                time_str = "--:--"
            pyxel.text(padding, y, f"  {i+1}  {time_str}", pyxel.COLOR_WHITE)
    
    def draw_egg_stats(self, atk: float, spd: float, eggxperience: int, eggxperience_required: int) -> None:
        # Draw XP bar
        bar_width = 100
        bar_height = 6
        bar_x = 10
        bar_y = 10
    
        xp_ratio = eggxperience / eggxperience_required if eggxperience_required > 0 else 0
        filled_width = int(bar_width * xp_ratio)

        # XP bar background (gray)
        pyxel.rect(bar_x, bar_y, bar_width, bar_height, pyxel.COLOR_DARK_BLUE)
        # XP bar fill (green)
        pyxel.rect(bar_x, bar_y, filled_width, bar_height, pyxel.COLOR_GREEN)

        # XP text
        xp_text = f"Exp: {eggxperience}/{eggxperience_required}"
        pyxel.text(bar_x, bar_y + bar_height + 2, xp_text, pyxel.COLOR_WHITE)

        # atk text
        atk_text = f"Atk: {atk:.2f}"
        pyxel.text(bar_x, bar_y + bar_height + 12, atk_text, pyxel.COLOR_WHITE)

        # Speed text
        spd_text = f"Spd: {spd:.2f}"
        pyxel.text(bar_x, bar_y + bar_height + 22, spd_text, pyxel.COLOR_WHITE)

    # enhancement screen
    def draw_enhancement_screen(self, options: list[str], selected_index: int) -> None:
        box_width = 140
        box_height = 20 + 18 * len(options)
        box_x = (self._screen_width - box_width) // 2
        box_y = (self._screen_height - box_height) // 2

        # Draw background box
        pyxel.rect(box_x, box_y, box_width, box_height, pyxel.COLOR_DARK_BLUE)
        pyxel.rectb(box_x, box_y, box_width, box_height, pyxel.COLOR_WHITE)

        # Draw title
        title = "Choose Upgrade:"
        pyxel.text(box_x + 10, box_y + 4, title, pyxel.COLOR_YELLOW)

        # Draw options
        for i, option in enumerate(options):
            y = box_y + 20 + i * 18
            if i == selected_index:
                # Make selector blink: visible every ~10 frames
                blink = (pyxel.frame_count // 10) % 2 == 0
                prefix = "> " if blink else "  "
                color = pyxel.COLOR_GREEN
                pyxel.text(box_x + 8, y, prefix + option, color)
            else:
                color = pyxel.COLOR_WHITE
                pyxel.text(box_x + 10, y, option, color)
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

        pyxel.text(text_x - 2, text_y - 2, text, pyxel.COLOR_BLACK, None)
        
        #reset
        restart_text = "Press R to Restart"
        restart_text_x = box_x + (box_width - len(restart_text) * 4) // 2
        pyxel.text(restart_text_x - 2, text_y + 8, restart_text, pyxel.COLOR_BLACK)

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

import pytest
from unittest.mock import Mock, call

from egg_rally.controller import Controller
from egg_rally.project_types import Keybinds
from egg_rally.egg_entities import Eggnemy


class TestController:
    @pytest.fixture
    def mock_model(self):
        model = Mock()
        model.fps = 60
        model.world_right = 100
        model.world_left = 0
        model.world_top = 0
        model.world_bottom = 100
        model.world_width = 100
        model.world_height = 100
        model.elapsed_frames = 0
        model.eggnemies_killed = 0
        model._leaderboard = []
        model.is_game_over = False
        model.egg = Mock()
        model.egg.is_dead = False
        model.egg.hitbox = (10, 10, 20, 20)
        model.stop_game = False
        model._eggnemy_list = Mock()
        model._eggnemy_list.update_list = Mock()
        return model

    @pytest.fixture
    def mock_view(self):
        view = Mock()
        return view

    @pytest.fixture
    def mock_pyxel(self, mocker):
        mocker.patch('egg_rally.controller.pyxel.btn', return_value=False)
        mocker.patch('egg_rally.controller.pyxel.btnp', return_value=False)
        mocker.patch('egg_rally.controller.pyxel.quit')
        mocker.patch('egg_rally.controller.pyxel.KEY_W', 1)
        mocker.patch('egg_rally.controller.pyxel.KEY_S', 2)
        mocker.patch('egg_rally.controller.pyxel.KEY_A', 3)
        mocker.patch('egg_rally.controller.pyxel.KEY_D', 4)
        mocker.patch('egg_rally.controller.pyxel.KEY_L', 5)
        mocker.patch('egg_rally.controller.pyxel.KEY_R', 6)
        mocker.patch('egg_rally.controller.pyxel.KEY_Q', 7)
        mocker.patch('egg_rally.controller.pyxel.COLOR_GRAY', 10)
        mocker.patch('egg_rally.controller.pyxel.COLOR_WHITE', 11)
        mocker.patch('egg_rally.controller.pyxel.COLOR_YELLOW', 12)
        return mocker.patch('egg_rally.controller.pyxel')

    @pytest.fixture
    def controller(self, mock_model, mock_view):
        return Controller(mock_model, mock_view)

    def test_init(self, mock_model, mock_view):
        controller = Controller(mock_model, mock_view)
        assert controller._model == mock_model
        assert controller._view == mock_view

    def test_start(self, controller, mock_model, mock_view):
        controller.start()
        mock_view.start.assert_called_once_with(mock_model.fps, controller, controller)

    @pytest.mark.parametrize("key_w, key_s, key_a, key_d, key_l, key_r, key_q, expected_keybinds", [
        (False, False, False, False, False, False, False, Keybinds(False, False, False, False, False, False, False)),
        (True, False, False, False, False, False, False, Keybinds(True, False, False, False, False, False, False)),
        (False, False, False, False, True, False, False, Keybinds(False, False, False, False, True, False, False)),
        (False, False, False, False, False, True, False, Keybinds(False, False, False, False, False, True, False)),
        (False, False, False, False, False, False, True, Keybinds(False, False, False, False, False, False, True)),
        (True, False, True, False, True, False, False, Keybinds(True, False, True, False, True, False, False)),
    ])
    def test_update_keybinds(self, controller, mock_model, mock_view, mock_pyxel,
                             key_w, key_s, key_a, key_d, key_l, key_r, key_q, expected_keybinds):
        mock_pyxel.btn.side_effect = lambda key: {
            mock_pyxel.KEY_W: key_w,
            mock_pyxel.KEY_S: key_s,
            mock_pyxel.KEY_A: key_a,
            mock_pyxel.KEY_D: key_d,
            mock_pyxel.KEY_L: key_l,
        }.get(key, False)
        mock_pyxel.btnp.side_effect = lambda key: {
            mock_pyxel.KEY_R: key_r,
            mock_pyxel.KEY_Q: key_q,
        }.get(key, False)

        controller.update()

        mock_model.update.assert_called_once_with(expected_keybinds)
        mock_pyxel.btn.assert_has_calls([
            call(mock_pyxel.KEY_W),
            call(mock_pyxel.KEY_S),
            call(mock_pyxel.KEY_A),
            call(mock_pyxel.KEY_D),
            call(mock_pyxel.KEY_L),
        ], any_order=True)
        mock_pyxel.btnp.assert_has_calls([
            call(mock_pyxel.KEY_R),
            call(mock_pyxel.KEY_Q),
        ], any_order=True)

    def test_update_win_condition(self, controller, mock_model, mock_view, mock_pyxel):
        mock_model.is_game_over = True
        mock_model.egg.is_dead = False

        controller.update()

        mock_view.draw_end.assert_called_once_with(mock_model.egg.hitbox, "YOU WIN")
        mock_model.update.assert_called_once()

    def test_update_game_running(self, controller, mock_model, mock_view, mock_pyxel):
        mock_model.is_game_over = False
        mock_model.egg.is_dead = False

        controller.update()

        mock_view.draw_end.assert_not_called()
        mock_model.update.assert_called_once()
        mock_pyxel.quit.assert_not_called()

    def test_update_quit_game(self, controller, mock_model, mock_view, mock_pyxel):
        mock_model.stop_game = True

        controller.update()

        mock_model.update.assert_called_once()
        mock_pyxel.quit.assert_called_once()

    def test_draw(self, controller, mock_model, mock_view, mock_pyxel):
        mock_eggnemy1 = Mock(spec=Eggnemy)
        mock_eggnemy1.hitbox = (50, 50, 60, 60)
        mock_eggnemy1.health = 10
        mock_eggnemy2 = Mock(spec=Eggnemy)
        mock_eggnemy2.hitbox = (70, 70, 80, 80)
        mock_eggnemy2.health = 5

        mock_model._eggnemy_list.update_list.side_effect = \
            lambda draw_func: [draw_func(mock_eggnemy1), draw_func(mock_eggnemy2)]

        controller.draw()

        mock_view.clear_screen.assert_called_once()
        mock_view.draw_border.assert_called_once_with(
            mock_model.world_right, mock_model.world_left, mock_model.world_top,
            mock_model.world_bottom, mock_model.world_width, mock_model.world_height
        )
        mock_view.draw_information.assert_called_once_with(
            mock_model.elapsed_frames, mock_model.fps, mock_model.eggnemies_killed
        )
        mock_view.draw_leaderboard.assert_called_once_with(mock_model._leaderboard)
        mock_view.draw_hitbox.assert_has_calls([
            call(mock_model.egg.hitbox, mock_pyxel.COLOR_WHITE),
            call(mock_eggnemy1.hitbox, mock_pyxel.COLOR_GRAY),
            call(mock_eggnemy2.hitbox, mock_pyxel.COLOR_GRAY),
        ])
        mock_view.draw_health.assert_has_calls([
            call(mock_model.egg, 11),
            call(mock_eggnemy1, 8),
            call(mock_eggnemy2, 8),
        ])

        mock_model._eggnemy_list.update_list.assert_called_once()

        mock_view.draw_end.assert_not_called()

    def test_draw_win_condition_at_end(self, controller, mock_model, mock_view, mock_pyxel):
        mock_model.is_game_over = True
        mock_model.egg.is_dead = False

        controller.draw()
        mock_view.draw_end.assert_called_once_with(mock_model.egg.hitbox, "YOU WIN")

    def test_draw_lose_condition_at_end(self, controller, mock_model, mock_view, mock_pyxel):
        mock_model.is_game_over = True
        mock_model.egg.is_dead = True

        controller.draw()
        mock_view.draw_end.assert_called_once_with(mock_model.egg.hitbox, "YOU LOSE")

    def test_draw_eggmemy(self, controller, mock_view, mock_pyxel):
        eggnemy = Mock(spec=Eggnemy)
        eggnemy.hitbox = (20, 20, 30, 30)
        eggnemy.health = 5

        controller._draw_eggmemy(eggnemy)

        mock_view.draw_hitbox.assert_called_once_with(eggnemy.hitbox, mock_pyxel.COLOR_GRAY)
        mock_view.draw_health.assert_called_once_with(eggnemy, 8)
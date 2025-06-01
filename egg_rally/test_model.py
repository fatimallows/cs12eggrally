import pytest
from unittest.mock import Mock, patch, call
from random import uniform
import itertools

from egg_rally.model import Model, SettingsData, EggSpecificData, EggnemySpecificData, BossEggnemySpecificData, Keybinds
from egg_rally.project_types import Hitbox
from egg_rally.helpers import CartesianPoint, Vector
from egg_rally.egg_entities import Egg, Eggnemy, EggnemyType, EggnemyTag, EggnemyList

@pytest.fixture(autouse=True)
def mock_settings_data():
    with patch('egg_rally.model.json_handler') as mock_json_handler:
        mock_instance = Mock()
        mock_json_handler.return_value = mock_instance
        mock_instance.extract_settings.return_value = {
            'game_fps': 60,
            'eggnemy_cap': 5,
            'boss_spawn_counter': 10,
            'egg_health': 100,
            'egg_width': 20,
            'egg_height': 20,
            'egg_movement_speed': 4,
            'egg_base_damage': 10,
            'egg_damage_hitbox_scale': 1.5,
            'eggnemy_health': 10,
            'eggnemy_width': 10,
            'eggnemy_height': 10,
            'boss_health': 200,
            'boss_width': 40,
            'boss_height': 40,
            'boss_base_damage': 20,
        }
        Model._settings = mock_instance.extract_settings('all')
        SettingsData.fps = Model._settings['game_fps']
        SettingsData.eggnemy_cap = Model._settings['eggnemy_cap']
        SettingsData.boss_spawn_counter = Model._settings['boss_spawn_counter']
        EggSpecificData.egg_health = Model._settings['egg_health']
        EggSpecificData.egg_width = Model._settings['egg_width']
        EggSpecificData.egg_height = Model._settings['egg_height']
        EggSpecificData.movement_speed = Model._settings['egg_movement_speed']
        EggSpecificData.base_damage = Model._settings['egg_base_damage']
        EggSpecificData.damage_hitbox_scale = Model._settings['egg_damage_hitbox_scale']
        EggSpecificData.invincibility_frames = int(SettingsData.fps) * 1
        EggnemySpecificData.eggnemy_health = Model._settings['eggnemy_health']
        EggnemySpecificData.eggnemy_width = Model._settings['eggnemy_width']
        EggnemySpecificData.eggnemy_height = Model._settings['eggnemy_height']
        BossEggnemySpecificData.boss_health = Model._settings['boss_health']
        BossEggnemySpecificData.boss_width = Model._settings['boss_width']
        BossEggnemySpecificData.boss_height = Model._settings['boss_height']
        BossEggnemySpecificData.base_damage = Model._settings['boss_base_damage']
        yield

@pytest.fixture
def model_instance():
    return Model(fps=60, screen_width=800, screen_height=600, world_width=400, world_height=300)

@pytest.fixture
def mock_uniform(mocker):
    return mocker.patch('egg_rally.model.uniform')

@pytest.fixture(autouse=True)
def mock_leaderboard_io(mocker):
    mock_load = mocker.patch('egg_rally.model.load_leaderboard', return_value=[])
    mock_save = mocker.patch('egg_rally.model.save_leaderboard')
    yield mock_load, mock_save

class TestModelInit:
    def test_init_sets_world_dimensions_correctly(self):
        model = Model(fps=60, screen_width=800, screen_height=600, world_width=400, world_height=300)
        assert model.fps == 60
        assert model.screen_width == 800
        assert model.screen_height == 600
        assert model.world_width == 400
        assert model.world_height == 300
        assert model.world_x == (800 - 400) // 2
        assert model.world_y == (600 - 300) // 2

    @pytest.mark.parametrize("screen_w, screen_h, world_w, world_h, expected_world_x, expected_world_y", [
        (100, 100, 200, 200, 0, 0),
        (800, 600, 400, 300, 200, 150),
        (400, 300, 400, 300, 0, 0),
    ])
    def test_init_world_offset_logic(self, screen_w, screen_h, world_w, world_h, expected_world_x, expected_world_y):
        model = Model(fps=60, screen_width=screen_w, screen_height=screen_h, world_width=world_w, world_height=world_h)
        assert model.world_x == expected_world_x
        assert model.world_y == expected_world_y
        assert model.world_left == expected_world_x
        assert model.world_right == expected_world_x + world_w
        assert model.world_top == expected_world_y
        assert model.world_bottom == expected_world_y + world_h

    def test_init_sets_initial_game_state(self, model_instance):
        assert not model_instance.stop_game
        assert not model_instance.is_game_over
        assert model_instance.elapsed_frames == 0
        assert model_instance.eggnemies_killed == 0
        assert model_instance._no_boss_generated
        assert model_instance._boss_id is None
        assert model_instance._is_boss_alive is None
        assert not model_instance._is_time_recorded
        assert model_instance._leaderboard == []

    def test_init_eggnemy_configs_are_correct(self, model_instance):
        assert model_instance._eggnemy_config._width == EggnemySpecificData.eggnemy_width
        assert model_instance._eggnemy_config.max_health == EggnemySpecificData.eggnemy_health
        assert model_instance._boss_eggnemy_config._width == BossEggnemySpecificData.boss_width
        assert model_instance._boss_eggnemy_config.max_health == BossEggnemySpecificData.boss_health

    def test_init_eggnemy_list_is_empty(self, model_instance):
        assert isinstance(model_instance._eggnemy_list, EggnemyList)
        assert model_instance._eggnemy_list.len() == 0

class TestModelRestart:
    def test_restart_resets_game_state(self, model_instance):
        model_instance._is_game_over = True
        model_instance._elapsed_frames = 100
        model_instance._eggnemies_killed = 5
        model_instance._no_boss_generated = False
        model_instance._boss_id = 123
        model_instance._is_boss_alive = True
        model_instance._is_time_recorded = True
        model_instance._eggnemy_list.append(Mock())

        model_instance.restart()

        assert not model_instance.is_game_over
        assert model_instance.elapsed_frames == 0
        assert model_instance.eggnemies_killed == 0
        assert model_instance._no_boss_generated
        assert model_instance._boss_id is None
        assert model_instance._is_boss_alive is None
        assert not model_instance._is_time_recorded
        assert model_instance._eggnemy_list.len() == 0

    def test_restart_resets_egg_position_and_health(self, model_instance):
        original_egg = model_instance.egg
        original_egg.hitbox._coordinate = CartesianPoint(1,1)
        original_egg.health = 1

        model_instance.restart()

        new_egg = model_instance.egg
        expected_x = (model_instance.screen_width - int(EggSpecificData.egg_width)) // 2
        expected_y = (model_instance.screen_height - int(EggSpecificData.egg_height)) // 2
        assert new_egg.hitbox.left == expected_x
        assert new_egg.hitbox.top == expected_y
        assert new_egg.health == EggSpecificData.egg_health

class TestModelGenerateSpawnLocation:
    def test_generate_spawn_location_avoids_egg_and_is_in_bounds(self, model_instance, mock_uniform, mocker):
        mock_uniform.side_effect = [
            (model_instance.world_left + model_instance.world_right - EggnemySpecificData.eggnemy_width) / 2,
            (model_instance.world_top + model_instance.world_bottom - EggnemySpecificData.eggnemy_height) / 2,
            (model_instance.world_left + model_instance.world_right - EggnemySpecificData.eggnemy_width) / 2,
            (model_instance.world_top + model_instance.world_bottom - EggnemySpecificData.eggnemy_height) / 2,
            (model_instance.world_left + model_instance.world_right - EggnemySpecificData.eggnemy_width) / 2,
            (model_instance.world_top + model_instance.world_bottom - EggnemySpecificData.eggnemy_height) / 2
        ]

        mock_get_vector = mocker.patch.object(model_instance._egg, '_get_vector_to_hitbox')
        mock_get_vector.side_effect = [Vector(0,0), Vector(0,0), Vector(25, 0)]

        spawn_point = model_instance._generate_spawn_location()

        assert mock_uniform.call_count >= 2
        assert mock_get_vector.called
        assert spawn_point.x == (model_instance.world_left + model_instance.world_right - EggnemySpecificData.eggnemy_width) / 2
        assert spawn_point.y == (model_instance.world_top + model_instance.world_bottom - EggnemySpecificData.eggnemy_height) / 2

class TestModelCombatHelpers:
    def test_move_all_calls_move_on_eggnemy(self, model_instance, mocker):
        mock_eggnemy = Mock(spec=Eggnemy)
        mocker.patch.object(mock_eggnemy, 'move')
        move_vector = Vector(1, 0)

        move_func = model_instance._move_all(move_vector)
        move_func(mock_eggnemy)

        mock_eggnemy.move.assert_called_once_with(move_vector)

class TestModelUpdate:
    def test_update_quits_game_when_quit_key_pressed(self, model_instance, mock_leaderboard_io):
        mock_load, mock_save = mock_leaderboard_io
        keybinds = Keybinds(up=False, down=False, left=False, right=False, attack=False, restart=False, quit=True)
        model_instance._leaderboard = [10.0, 20.0, 30.0, 40.0]

        model_instance.update(keybinds)

        assert model_instance.stop_game
        mock_save.assert_called_once_with([10.0, 20.0, 30.0])

    def test_update_does_nothing_when_game_over_and_no_restart(self, model_instance, mocker):
        keybinds = Keybinds(up=False, down=False, left=False, right=False, attack=False, restart=False, quit=False)
        model_instance._is_game_over = True

        mocker.patch.object(model_instance, 'restart')
        mocker.patch.object(model_instance, '_generate_eggnemies')
        mocker.patch.object(model_instance._egg, 'tick')
        mocker.patch.object(model_instance._eggnemy_list, 'update_list')

        model_instance.update(keybinds)

        model_instance.restart.assert_not_called()
        model_instance._generate_eggnemies.assert_not_called()
        model_instance._egg.tick.assert_not_called()
        model_instance._eggnemy_list.update_list.assert_not_called()
        assert model_instance.is_game_over

    def test_update_increments_elapsed_frames(self, model_instance):
        keybinds = Keybinds(up=False, down=False, left=False, right=False, attack=False, restart=False, quit=False)
        initial_frames = model_instance.elapsed_frames
        model_instance.update(keybinds)
        assert model_instance.elapsed_frames == initial_frames + 1
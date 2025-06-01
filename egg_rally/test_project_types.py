import pytest
from egg_rally.helpers import Vector, CartesianPoint
from egg_rally.project_types import InitEggConfig, Hitbox, EggConfig, Keybinds

class TestVector:
    def test_vector_creation(self):
        v1 = Vector(1.0, 2.0)
        assert v1.x_hat == 1.0
        assert v1.y_hat == 2.0

        v2 = Vector(0.0, 0.0)
        assert v2.x_hat == 0.0
        assert v2.y_hat == 0.0

        v3 = Vector(-1.0, -2.0)
        assert v3.x_hat == -1.0
        assert v3.y_hat == -2.0

    def test_vector_addition(self):
        
        v1 = Vector(1.0, 2.0)
        v2 = Vector(3.0, 4.0)
        assert v1 + v2 == Vector(4.0, 6.0)

        v3 = Vector(0.0, 0.0)
        v4 = Vector(0.0, 0.0)
        assert v3 + v4 == Vector(0.0, 0.0)

        v5 = Vector(-1.0, -2.0)
        v6 = Vector(-3.0, -4.0)
        assert v5 + v6 == Vector(-4.0, -6.0)

        v7 = Vector(1.0, 2.0)
        v8 = Vector(-3.0, -4.0)
        assert v7 + v8 == Vector(-2.0, -2.0)

    def test_vector_subtraction(self):
        v1 = Vector(1.0, 2.0)
        v2 = Vector(3.0, 4.0)
        assert v1 - v2 == Vector(-2.0, -2.0)

        v3 = Vector(0.0, 0.0)
        v4 = Vector(0.0, 0.0)
        assert v3 - v4 == Vector(0.0, 0.0)

        v5 = Vector(-1.0, -2.0)
        v6 = Vector(-3.0, -4.0)
        assert v5 - v6 == Vector(2.0, 2.0)

        v7 = Vector(1.0, 2.0)
        v8 = Vector(-3.0, -4.0)
        assert v7 - v8 == Vector(4.0, 6.0)

    def test_vector_multiplication(self):
        v1 = Vector(1.0, 2.0)
        assert v1 * 3.0 == Vector(3.0, 6.0)
        assert v1 * 0.0 == Vector(0.0, 0.0)
        assert v1 * -3.0 == Vector(-3.0, -6.0)

        v2 = Vector(-1.0, -2.0)
        assert v2 * -3.0 == Vector(3.0, 6.0)
        assert v2 * 0.0 == Vector(0.0, 0.0)

        v3 = Vector(0.0, 0.0)
        assert v3 * 5.0 == Vector(0.0, 0.0)

    def test_vector_true_division(self):
        v1 = Vector(6.0, 8.0)
        assert v1 / 2.0 == Vector(3.0, 4.0)

        v2 = Vector(0.0, 0.0)
        assert v2 / 2.0 == Vector(0.0, 0.0)
        with pytest.raises(ZeroDivisionError):
            _ = v2 / 0.0

        v3 = Vector(-6.0, -8.0)
        assert v3 / 2.0 == Vector(-3.0, -4.0)
        assert v3 / -2.0 == Vector(3.0, 4.0)
        with pytest.raises(ZeroDivisionError):
            _ = v3 / 0.0

    def test_vector_negation(self):
        v1 = Vector(1.0, -2.0)
        assert -v1 == Vector(-1.0, 2.0)

        v2 = Vector(0.0, 0.0)
        assert -v2 == Vector(0.0, 0.0)

        v3 = Vector(-3.0, 4.0)
        assert -v3 == Vector(3.0, -4.0)

    def test_vector_equality(self):
        v1 = Vector(1.0, 2.0)
        v2 = Vector(1.0, 2.0)
        v3 = Vector(-1.0, -2.0)
        v4 = Vector(0.0, 0.0)

        assert v1 == v2
        assert v1 != v3
        assert v1 != v4
        assert v1 != (1.0, 2.0)
        assert v1 == -v3

    def test_vector_absolute_value(self):
        v1 = Vector(3.0, 4.0)
        assert abs(v1) == 5.0

        v2 = Vector(0.0, 0.0)
        assert abs(v2) == 0.0

        v3 = Vector(-3.0, 4.0)
        assert abs(v3) == 5.0

    def test_vector_dot_product(self):
        v1 = Vector(1.0, 2.0)
        v2 = Vector(3.0, 4.0)
        assert v1.dot_product(v2) == 11.0

        v3 = Vector(0.0, 0.0)
        v4 = Vector(5.0, -2.0)
        assert v3.dot_product(v4) == 0.0
        assert v4.dot_product(v3) == 0.0

        v5 = Vector(-1.0, 3.0)
        v6 = Vector(2.0, -1.0)
        assert v5.dot_product(v6) == -5.0

    def test_vector_projection_onto(self):
        v1 = Vector(1.0, 2.0)
        v2 = Vector(3.0, 0.0)
        projection = v1.project_onto(v2)
        assert projection == Vector(1.0, 0.0)
        
    def test_vector_convert_to_point(self):
        v1 = Vector(1.5, 2.5)
        assert v1.convert_to_point() == CartesianPoint(1.5, 2.5)

        v2 = Vector(0.0, 0.0)
        assert v2.convert_to_point() == CartesianPoint(0.0, 0.0)

        v3 = Vector(-1.5, -2.5)
        assert v3.convert_to_point() == CartesianPoint(-1.5, -2.5)

class TestCartesianPoint:
    def test_cartesian_point_creation(self):
        p1 = CartesianPoint(3.0, 4.0)
        assert p1.x == 3.0
        assert p1.y == 4.0

        p2 = CartesianPoint(0.0, 0.0)
        assert p2.x == 0.0
        assert p2.y == 0.0

        p3 = CartesianPoint(-3.0, -4.0)
        assert p3.x == -3.0
        assert p3.y == -4.0

    def test_cartesian_point_convert_to_vector(self):
        p1 = CartesianPoint(5.0, 6.0)
        assert p1.convert_to_vector() == Vector(5.0, 6.0)

        p2 = CartesianPoint(0.0, 0.0)
        assert p2.convert_to_vector() == Vector(0.0, 0.0)

        p3 = CartesianPoint(-5.0, -6.0)
        assert p3.convert_to_vector() == Vector(-5.0, -6.0)

class TestInitEggConfig:
    def test_init_egg_config_creation(self):
        config = InitEggConfig(
            _width=10.0,
            _height=20.0,
            movement_speed=5.0,
            max_health=100.0,
            base_damage=10.0,
            damage_hitbox_scale=1.5,
            invincibility_frames=30
        )
        assert config._width == 10.0
        assert config._height == 20.0
        assert config.movement_speed == 5.0
        assert config.max_health == 100.0
        assert config.base_damage == 10.0
        assert config.damage_hitbox_scale == 1.5
        assert config.invincibility_frames == 30

        zero_config = InitEggConfig(
            _width=0.0,
            _height=0.0,
            movement_speed=0.0,
            max_health=0.0,
            base_damage=0.0,
            damage_hitbox_scale=1.0,
            invincibility_frames=0
        )
        assert zero_config._width == 0.0
        assert zero_config._height == 0.0
        assert zero_config.movement_speed == 0.0
        assert zero_config.max_health == 0.0
        assert zero_config.base_damage == 0.0
        assert zero_config.damage_hitbox_scale == 1.0
        assert zero_config.invincibility_frames == 0

class TestHitbox:
    def test_hitbox_creation(self):
        coordinate = CartesianPoint(1.0, 2.0)
        hitbox = Hitbox(_coordinate=coordinate, _width=3.0, _height=4.0)
        assert hitbox._coordinate == coordinate
        assert hitbox._width == 3.0
        assert hitbox._height == 4.0

        zero_hitbox = Hitbox(_coordinate=CartesianPoint(0.0, 0.0), _width=0.0, _height=0.0)
        assert zero_hitbox._coordinate == CartesianPoint(0.0, 0.0)
        assert zero_hitbox._width == 0.0
        assert zero_hitbox._height == 0.0

        negative_hitbox = Hitbox(_coordinate=CartesianPoint(-1.0, -2.0), _width=3.0, _height=4.0)
        assert negative_hitbox._coordinate == CartesianPoint(-1.0, -2.0)
        assert negative_hitbox._width == 3.0
        assert negative_hitbox._height == 4.0

    def test_hitbox_properties(self):
        coordinate = CartesianPoint(1.0, 2.0)
        hitbox = Hitbox(_coordinate=coordinate, _width=3.0, _height=4.0)
        assert hitbox.width == 3.0
        assert hitbox.height == 4.0
        assert hitbox.top == 2.0
        assert hitbox.bottom == 6.0
        assert hitbox.left == 1.0
        assert hitbox.right == 4.0
        assert hitbox.x == 1.0
        assert hitbox.y == 2.0
        assert hitbox.center == CartesianPoint(2.5, 4.0)

        zero_hitbox = Hitbox(_coordinate=CartesianPoint(0.0, 0.0), _width=0.0, _height=0.0)
        assert zero_hitbox.width == 0.0
        assert zero_hitbox.height == 0.0
        assert zero_hitbox.top == 0.0
        assert zero_hitbox.bottom == 0.0
        assert zero_hitbox.left == 0.0
        assert zero_hitbox.right == 0.0
        assert zero_hitbox.x == 0.0
        assert zero_hitbox.y == 0.0
        assert zero_hitbox.center == CartesianPoint(0.0, 0.0)


    def test_hitbox_setters(self):
        coordinate = CartesianPoint(1.0, 2.0)
        hitbox = Hitbox(_coordinate=coordinate, _width=3.0, _height=4.0)
        hitbox.x = 5.0
        hitbox.y = 6.0
        assert hitbox.x == 5.0
        assert hitbox.y == 6.0
        assert hitbox._coordinate == CartesianPoint(5.0, 6.0)

        zero_hitbox = Hitbox(_coordinate=CartesianPoint(0.0, 0.0), _width=0.0, _height=0.0)
        zero_hitbox.x = -1.0
        zero_hitbox.y = 1.0
        assert zero_hitbox.x == -1.0
        assert zero_hitbox.y == 1.0
        assert zero_hitbox._coordinate == CartesianPoint(-1.0, 1.0)

    def test_hitbox_is_touching(self):
        coordinate_pos = CartesianPoint(0.0, 0.0)
        hitbox_pos = Hitbox(_coordinate=coordinate_pos, _width=2.0, _height=2.0) # Center at (1, 1)
        assert hitbox_pos.is_touching(Vector(1.0, 1.0))
        assert hitbox_pos.is_touching(Vector(0.5, 0.5))
        assert hitbox_pos.is_touching(Vector(1.0, 1.0)) # Edge case
        assert not hitbox_pos.is_touching(Vector(1.1, 1.0))
        assert not hitbox_pos.is_touching(Vector(1.0, 1.1))

        coordinate_zero = CartesianPoint(0.0, 0.0)
        hitbox_zero = Hitbox(_coordinate=coordinate_zero, _width=0.0, _height=0.0) # Center at (0, 0)
        assert hitbox_zero.is_touching(Vector(0.0, 0.0))
        assert not hitbox_zero.is_touching(Vector(0.1, 0.0))
        assert not hitbox_zero.is_touching(Vector(0.0, 0.1))

        coordinate_neg_pos_dim = CartesianPoint(-1.0, -1.0)
        hitbox_neg_pos_dim = Hitbox(_coordinate=coordinate_neg_pos_dim, _width=2.0, _height=2.0) # Center at (0, 0)
        assert hitbox_neg_pos_dim.is_touching(Vector(0.0, 0.0))
        assert hitbox_neg_pos_dim.is_touching(Vector(0.5, -0.5))
        assert hitbox_neg_pos_dim.is_touching(Vector(0.0, 0.0)) # Center
        assert not hitbox_neg_pos_dim.is_touching(Vector(1.1, 0.0))
        assert not hitbox_neg_pos_dim.is_touching(Vector(0.0, 1.1))

class TestEggConfig:
    def test_egg_config_creation(self):
        coordinate = CartesianPoint(0.0, 0.0)
        hitbox = Hitbox(_coordinate=coordinate, _width=1.0, _height=1.0)
        config = EggConfig(
            hitbox=hitbox,
            movement_speed=2.0,
            max_health=50.0,
            base_damage=5.0,
            damage_hitbox_scale=1.2,
            invincibility_frames=15
        )
        assert config.hitbox == hitbox
        assert config.movement_speed == 2.0
        assert config.max_health == 50.0
        assert config.base_damage == 5.0
        assert config.damage_hitbox_scale == 1.2
        assert config.invincibility_frames == 15

        zero_config = EggConfig(
            hitbox=Hitbox(_coordinate=CartesianPoint(0.0, 0.0), _width=0.0, _height=0.0),
            movement_speed=0.0,
            max_health=0.0,
            base_damage=0.0,
            damage_hitbox_scale=1.0,
            invincibility_frames=0
        )
        assert config.hitbox == hitbox # Intentionally not checking the zero_config.hitbox instance
        assert zero_config.movement_speed == 0.0
        assert zero_config.max_health == 0.0
        assert zero_config.base_damage == 0.0
        assert zero_config.damage_hitbox_scale == 1.0
        assert zero_config.invincibility_frames == 0

class TestKeybinds:
    def test_keybinds_creation(self):
        keybinds = Keybinds(up=True, down=False, left=True, right=False, attack=True, restart=False, quit= False)
        assert keybinds.up is True
        assert keybinds.down is False
        assert keybinds.left is True
        assert keybinds.right is False
        assert keybinds.attack is True

        all_false = Keybinds(up=False, down=False, left=False, right=False, attack=False, restart=False, quit= False)
        assert not all_false.up
        assert not all_false.down
        assert not all_false.left
        assert not all_false.right
        assert not all_false.attack

        all_true = Keybinds(up=True, down=True, left=True, right=True, attack=True, restart=False, quit=False)
        assert all_true.up
        assert all_true.down
        assert all_true.left
        assert all_true.right
        assert all_true.attack

    def test_keybinds_y_one_pressed(self):
        assert Keybinds(up=True, down=False, left=False, right=False, attack=False, restart=False, quit= False).y_one_pressed is True
        assert Keybinds(up=False, down=True, left=False, right=False, attack=False, restart=False, quit= False).y_one_pressed is True
        assert Keybinds(up=True, down=True, left=False, right=False, attack=False, restart=False, quit= False).y_one_pressed is False
        assert Keybinds(up=False, down=False, left=False, right=False, attack=False, restart=False, quit= False).y_one_pressed is False
        assert Keybinds(up=True, down=True, left=True, right=True, attack=False, restart=False, quit= False).y_one_pressed is False
        assert Keybinds(up=True, down=False, left=True, right=False, attack=False, restart=False, quit= False).y_one_pressed is True
        assert Keybinds(up=True, down=False, left=True, right=True, attack=True, restart=False, quit= False).y_one_pressed is True
    def test_keybinds_x_one_pressed(self):
        
        assert Keybinds(up=False, down=False, left=True, right=False, attack=False, restart=False, quit= False).x_one_pressed is True
        assert Keybinds(up=False, down=False, left=False, right=True, attack=False, restart=False, quit= False).x_one_pressed is True
        assert Keybinds(up=False, down=False, left=True, right=True, attack=False, restart=False, quit= False).x_one_pressed is False
        assert Keybinds(up=False, down=False, left=False, right=False, attack=False, restart=False, quit= False).x_one_pressed is False
    

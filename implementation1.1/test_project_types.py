from project_types import Vector, Rectangle, EggnemyConfig, EntityConfig

class TestVector:

    def test_vector(self):
        v = Vector(1.0, 2.0)
        assert v.x_hat == 1.0
        assert v.y_hat == 2.0

        v = Vector(0.0, 0.0)
        assert v.x_hat == 0.0
        assert v.y_hat == 0.0

        v = Vector(-1.0, -2.0)
        assert v.x_hat == -1.0
        assert v.y_hat == -2.0

    def test_vector_addition(self):
        v1 = Vector(1.0, 2.0)
        v2 = Vector(3.0, 4.0)
        result = v1 + v2
        assert result == Vector(4.0, 6.0)

        v1 = Vector(0.0, 0.0)
        v2 = Vector(0.0, 0.0)
        result = v1 + v2
        assert result == Vector(0.0, 0.0)

        v1 = Vector(-1.0, -2.0)
        v2 = Vector(-3.0, -4.0)
        result = v1 + v2
        assert result == Vector(-4.0, -6.0)

        v1 = Vector(1.0, 2.0)
        v2 = Vector(-3.0, -4.0)
        result = v1 + v2
        assert result == Vector(-2.0, -2.0)

    def test_vector_subtraction(self):
        v1 = Vector(1.0, 2.0)
        v2 = Vector(3.0, 4.0)
        result = v1 - v2
        assert result == Vector(-2.0, -2.0)

        v1 = Vector(0.0, 0.0)
        v2 = Vector(0.0, 0.0)
        result = v1 + v2
        assert result == Vector(0.0, 0.0)

        v1 = Vector(-1.0, -2.0)
        v2 = Vector(-3.0, -4.0)
        result = v1 - v2
        assert result == Vector(2.0, 2.0)

        v1 = Vector(1.0, 2.0)
        v2 = Vector(-3.0, -4.0)
        result = v1 - v2
        assert result == Vector(4.0, 6.0)
    def test_vector_multiplication(self):
        v = Vector(1.0, 2.0)
        result = v * 3.0
        assert result == Vector(3.0, 6.0)

        v = Vector(1.0, 2.0)
        result = v * 0.0
        assert result == Vector(0.0, 0.0)

        v = Vector(1.0, 2.0)
        result = v * -3.0
        assert result == Vector(-3.0, -6.0)

        v = Vector(-1.0, -2.0)
        result = v * -3.0
        assert result == Vector(3.0, 6.0)

    def test_vector_true_division(self):
        v = Vector(6.0, 8.0)
        result = v / 2.0
        assert result == Vector(3.0, 4.0)

        v = Vector(0.0, 0.0)
        result = v / 2.0
        assert result == Vector(0.0, 0.0)
        
        v = Vector(-6.0, -8.0)
        result = v / 2.0
        assert result == Vector(-3.0, -4.0)

        v = Vector(-6.0, -8.0)
        result = v / -2.0
        assert result == Vector(3.0, 4.0)

    def test_vector_negation(self):
        v = Vector(1.0, -2.0)
        result = -v
        assert result == Vector(-1.0, 2.0)

        v = Vector(0.0, 0.0)
        result = -v
        assert result == Vector(0.0, 0.0)

    def test_vector_equality(self):
        v1 = Vector(1.0, 2.0)
        v2 = Vector(-1.0, -2.0)
        v3 = Vector(3.0, 4.0)
        v4 = Vector (2.0, 2.0)
        assert v1 == -v2
        assert v1 != v3
        assert v1 != (1.0, 2.0)
        assert v1 == v3 - v4

    def test_vector_absolute_value(self):
        v1 = Vector(3.0, 4.0)
        v2 = Vector(0.0, 0.0)
        v3 = Vector(-3.0, 4.0)
        assert abs(v1) == 5.0
        assert abs(v2) == 0.0
        assert abs(-v1) == 5.0
        assert abs(v3) == abs(v1)

    def test_vector_dot_product(self):
        v1 = Vector(1.0, 2.0)
        v2 = Vector(3.0, 4.0)
        v3 = Vector(0.0, 0.0)
        v4 = Vector(-1.0, -2.0)

        assert v1.dot_product(v2) == 11.0
        assert v2.dot_product(v2) == 25.0
        assert v3.dot_product(v4) == 0.0
        assert v4.dot_product(v2) == -11.0

    def test_vector_projection_onto(self):
        v1 = Vector(1.0, 2.0)
        v2 = Vector(3.0, 0.0)
        projection = v1.project_onto(v2)
        assert projection == Vector(1.0, 0.0)

        v3 = Vector(1.0, 1.0)
        v4 = Vector(0.0, 1.0)
        projection2 = v3.project_onto(v4)
        assert projection2 == Vector(0.0, 1.0)

class TestRectangle:
    def test_rectangle(self):
        rect = Rectangle(x=1.0, y=2.0, width=3.0, height=4.0)
        assert rect.x == 1.0
        assert rect.y == 2.0
        assert rect.width == 3.0
        assert rect.height == 4.0

        rect = Rectangle(x=0.0, y=0.0, width=3.0, height=4.0)
        assert rect.x == 0.0
        assert rect.y == 0.0
        assert rect.width == 3.0
        assert rect.height == 4.0

        rect = Rectangle(x=-1.0, y=-2.0, width=3.0, height=4.0)
        assert rect.x == -1.0
        assert rect.y == -2.0
        assert rect.width == 3.0
        assert rect.height == 4.0

    def test_rectangle_properties(self):
        rect = Rectangle(x=1.0, y=2.0, width=3.0, height=4.0)
        assert rect.top == 2.0
        assert rect.bottom == 6.0
        assert rect.left == 1.0
        assert rect.right == 4.0

        rect = Rectangle(x=0.0, y=0.0, width=3.0, height=4.0)
        assert rect.top == 0.0
        assert rect.bottom == 4.0
        assert rect.left == 0.0
        assert rect.right == 3.0

        rect = Rectangle(x=-1.0, y=-2.0, width=3.0, height=4.0)
        assert rect.top == -2.0
        assert rect.bottom == 2.0
        assert rect.left == -1.0
        assert rect.right == 2.0


    def test_rectangle_center_property(self):
        rect = Rectangle(x=1.0, y=2.0, width=3.0, height=4.0)
        center = rect.center
        assert center == Vector(2.5, 4.0)
        
        rect = Rectangle(x=0.0, y=0.0, width=3.0, height=4.0)
        center = rect.center
        assert center == Vector(1.5, 2.0)

        rect = Rectangle(x=-1.0, y=-2.0, width=3.0, height=4.0)
        center = rect.center
        assert center == Vector(0.5, 0.0)
        

class TestConfigs:
    def test_eggnemy_config(self):
        config = EggnemyConfig(width=10.0, height=20.0, movement_speed=5.0, base_health=100.0, base_damage=10.0)
        assert config.width == 10.0
        assert config.height == 20.0
        assert config.movement_speed == 5.0
        assert config.base_health == 100.0
        assert config.base_damage == 10.0

    def test_entity_config(self):
        config = EntityConfig(x=0.0, y=0.0, width=10.0, height=20.0, movement_speed=5.0, base_health=100.0, base_damage=10.0)
        assert config.x == 0.0
        assert config.y == 0.0
        assert config.width == 10.0
        assert config.height == 20.0
        assert config.movement_speed == 5.0
        assert config.base_health == 100.0
        assert config.base_damage == 10.0
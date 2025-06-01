from _egg_entities import Egg, EggEntity, Eggnemy, EggnemyList, EggnemyTag, EggnemyType, EggConfig, EggInfo
from _project_types import Hitbox, Vector, CartesianPoint
class TestEgg:
    def test_egg_creation(self):
        hitbox = Hitbox(CartesianPoint(0,0), 3, 4)
        egg_config = EggConfig(hitbox = hitbox,
                               movement_speed = 2.0,
                               max_health = 25,
                               base_damage = 1.0,
                               damage_hitbox_scale = 1.0,
                               invincibility_frames= 30)
        egg = Egg(egg_config)
        assert egg.hitbox == hitbox
        assert egg.movement_speed == 2.0
        assert egg.max_health == 25
        assert egg.base_damage == 1.0
        assert egg._damage_hitbox_scale == 1.0
        assert egg._invincibility_frames == 30
        assert egg._i_frame_counter == 0
        assert egg._center_to_corner_vector == Vector(1.5,2.0)
        
        new_reference_point = CartesianPoint(0.0, 0.0)
        new_width_height_vector = Vector(3.0, 4.0)
        assert egg._damage_hitbox == Hitbox(new_reference_point, new_width_height_vector.x_hat, new_width_height_vector.y_hat)
        assert egg.is_dead == False

    def test_egg_deal_damage(self):

        egghitbox = Hitbox(CartesianPoint(0,0), 3, 4)
        egg_config_attacker = EggConfig(hitbox = egghitbox,
                                       movement_speed = 2.0,
                                       max_health = 25.0,
                                       base_damage = 5.0,
                                       damage_hitbox_scale = 1.0,
                                       invincibility_frames= 30)
        attacker_egg = Egg(egg_config_attacker)

        eggentityhitbox = Hitbox(CartesianPoint(4,0), 3, 4)
        egg_config_target = EggConfig(hitbox = eggentityhitbox,
                                     movement_speed = 2.0,
                                     max_health = 20.0,
                                     base_damage = 1.0,
                                     damage_hitbox_scale = 1.0,
                                     invincibility_frames= 10)
        target_egg = Egg(egg_config_target)

        initial_target_health = target_egg.health
        attacker_egg.deal_damage(target_egg)

        #not overlapping
        assert target_egg.health == initial_target_health

        attacker_egg.hitbox._coordinate = CartesianPoint(1,0)
        attacker_egg.deal_damage(target_egg)

        assert target_egg.health < initial_target_health
        assert target_egg.health == initial_target_health - attacker_egg.base_damage
        assert target_egg._i_frame_counter == target_egg._invincibility_frames

        #invincibility frames
        target_egg._i_frame_counter = 5
        target_egg_health_invincibility = target_egg.health
        attacker_egg.deal_damage(target_egg)
        assert target_egg.health == target_egg_health_invincibility

        # Kill the target egg
        target_egg._health = 0
        health_before_dead_hit = target_egg.health
        attacker_egg.deal_damage(target_egg)
        assert target_egg.health == health_before_dead_hit

    def test_egg_take_damage(self):
        hitbox = Hitbox(CartesianPoint(0, 0), 3, 4)
        egg_config = EggConfig(hitbox=hitbox, movement_speed=2.0, max_health=25.0, base_damage=1.0, damage_hitbox_scale=1.0, invincibility_frames=2)
        egg = Egg(egg_config)

        initial_health = egg.health
        damage_amount = 10.0
        egg._take_damage(damage_amount)
        assert egg.health == initial_health - damage_amount
        assert egg._i_frame_counter == egg._invincibility_frames

        # Try to take damage while invincible
        egg._i_frame_counter = 1
        health_before_invincible = egg.health
        egg._take_damage(5.0)
        assert egg.health == health_before_invincible

        # Try to take damage when dead
        health_when_dead = egg.health
        egg._take_damage(5.0)
        assert egg.health == health_when_dead

    def test_egg_get_vector_to_hitbox(self):
        egg_hitbox = Hitbox(CartesianPoint(0, 0), 2, 2)
        egg_config = EggConfig(hitbox=egg_hitbox, movement_speed=1.0, max_health=10.0, base_damage=1.0, damage_hitbox_scale=1.0, invincibility_frames=0)
        egg = Egg(egg_config)

        other_hitbox_above = Hitbox(CartesianPoint(0, -3), 1, 1)
        vector_above = egg._get_vector_to_hitbox(other_hitbox_above)
    
        assert vector_above == Vector(0.0, -2.0)

        other_hitbox_below = Hitbox(CartesianPoint(0, 3), 1, 1)
        vector_below = egg._get_vector_to_hitbox(other_hitbox_below)
        assert vector_below == Vector(0.0, 1.0)

        other_hitbox_left = Hitbox(CartesianPoint(-3, 0), 1, 1)
        vector_left = egg._get_vector_to_hitbox(other_hitbox_left)
        assert vector_left == Vector(-2.0, 0.0)

        other_hitbox_right = Hitbox(CartesianPoint(3, 0), 1, 1)
        vector_right = egg._get_vector_to_hitbox(other_hitbox_right)
        assert vector_right == Vector(1.0, 0.0)

        other_hitbox_overlap = Hitbox(CartesianPoint(0, 0), 3, 3)
        vector_overlap = egg._get_vector_to_hitbox(other_hitbox_overlap)
        assert vector_overlap == Vector(0.0, 0.0)
    
    def test_egg_tick(self):
        hitbox = Hitbox(CartesianPoint(0, 0), 3, 4)
        egg_config = EggConfig(hitbox=hitbox, movement_speed=2.0, max_health=25.0, base_damage=1.0, damage_hitbox_scale=1.0, invincibility_frames=2)
        egg = Egg(egg_config)
        egg._i_frame_counter = 2
        egg.tick()
        assert egg._i_frame_counter == 1
        egg.tick()
        assert egg._i_frame_counter == 0
        egg.tick()
        assert egg._i_frame_counter == 0 # Should not go below zero

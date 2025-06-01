from abc import ABC
from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable
import itertools


from egg_rally.project_types import (EggConfig, Hitbox, EggEntity, EggInfo)
from egg_rally.helpers import (CartesianPoint, Vector)


class Egg(ABC):
    def __init__(self, egg_config: EggConfig, xp_threshold: int | None):
        self._hitbox: Hitbox = egg_config.hitbox
        self._movement_speed: float = egg_config.movement_speed
        self._max_health: float = egg_config.max_health
        self._health: float = egg_config.max_health
        self._base_damage: float = egg_config.base_damage
        self._damage_hitbox_scale: float = egg_config.damage_hitbox_scale
        self._invincibility_frames: int = egg_config.invincibility_frames
        self._i_frame_counter: int = 0
        # eggxperience shi
        self._eggxperience: int = 0
        self.xp_threshold = xp_threshold

        self._center_to_corner_vector: Vector = Vector(
            x_hat=self._hitbox.width / 2,
            y_hat=self._hitbox.height / 2
        )
        new_center_to_corner_vector: Vector = self._center_to_corner_vector * \
            self._damage_hitbox_scale
        new_reference_vector: Vector = self._hitbox.center.convert_to_vector() - \
            new_center_to_corner_vector
        new_reference_point: CartesianPoint = new_reference_vector.convert_to_point()
        new_width_height_vector: Vector = (
            self._center_to_corner_vector * 2) * self._damage_hitbox_scale

        self._damage_hitbox: Hitbox = Hitbox(
            _coordinate=new_reference_point,
            _width=new_width_height_vector.x_hat,
            _height=new_width_height_vector.y_hat,
        )
        print(self._damage_hitbox)
        print(self.hitbox)
        # breakpoint()
        self._is_dead: bool = False

    def deal_damage(self, egg_entity: EggEntity) -> None:
        """checks if the point on the target egg entity closest to current egg is within damage range

        Args:
            egg_entity (EggEntity): just put in an Egg 
            damage_value (float): damage value
        """
        if self.is_dead:
            print("is dead")
            return
        relative_vector_to_hitbox: Vector = self._get_vector_to_hitbox(
            egg_entity.hitbox)
        center_to_target: Vector = max(
            (Vector(i*self._center_to_corner_vector.x_hat, j*self._center_to_corner_vector.y_hat) + relative_vector_to_hitbox
             for i in [-1, 1]
             for j in [-1, 1]),
            key=lambda v: abs(v)
        )
        if self._damage_hitbox.is_touching(center_to_target):
            egg_entity._take_damage(self.base_damage)

    def _take_damage(self, damage_value: float) -> None:
        """takes in damage, and changes the health accordingly

        Args:
            damage_value (float): damage dealt to the current Egg
        """
        if self._i_frame_counter > 0 or self.is_dead:
            return

        self._health -= damage_value
        self._health = 0 if self.health < 0 else self._health
        self._i_frame_counter = self._invincibility_frames

        if self.health <= 0:
            self._is_dead = True

    def apply_egghancement(self, choice: int) -> None:
        """
            choice:
            1 - Increase max HP
            2 - Increase attack
            3 - Increase speed
        """
        hp_inc = self._egghancement_hp if choice == 1 else 0
        atk_inc = self._egghancement_atk if choice == 2 else 0
        spd_inc = self._egghancement_spd if choice == 3 else 0
        self._egg.apply_egghancement(choice, hp_inc, atk_inc, spd_inc)
        self._should_trigger_egghancement = False

    def _get_vector_to_hitbox(self, hitbox_target: Hitbox) -> Vector:
        """Simply get the x and y distance of the two objects and slap them on a vector.

        Args:
            other (HitboxfulObject): just anything with a hitbox

        Returns:
            Vector: A position vector that embeds distance and magnitude to another object
        """
        if self.is_dead:
            return Vector(0, 0)
        # delta y
        if self.hitbox.top > hitbox_target.bottom:
            delta_y: float = hitbox_target.bottom - self.hitbox.top
        elif hitbox_target.top > self.hitbox.bottom:
            delta_y = hitbox_target.top - self.hitbox.bottom
        else:
            delta_y = 0

        # delta x
        if self.hitbox.left > hitbox_target.right:
            delta_x: float = hitbox_target.right - self.hitbox.left
        elif hitbox_target.left > self.hitbox.right:
            delta_x = hitbox_target.left - self.hitbox.right
        else:
            delta_x = 0

        return Vector(delta_x, delta_y)

    def tick(self) -> None:
        self._i_frame_counter += -1 if self._i_frame_counter > 0 else 0
        print(self._i_frame_counter)

    def move(self, velocity_vector: Vector) -> None:
        pass

    def gain_eggxperience(self, amount: int = 1) -> None:
        self._eggxperience += amount

    @property
    def eggxperience(self) -> int:
        return self._eggxperience

    @eggxperience.setter
    def eggxperience(self, value):
        self._eggxperience = value

    @property
    def hitbox(self) -> Hitbox:
        return self._hitbox

    @property
    def movement_speed(self) -> float:
        return self._movement_speed

    @property
    def max_health(self) -> float:
        return self._max_health

    @property
    def health(self) -> float:
        return self._health

    @health.setter
    def health(self, val) -> None:
        self._health = val

    @property
    def base_damage(self) -> float:
        return self._base_damage

    @property
    def is_dead(self) -> bool:
        return self._is_dead


class Eggnemy(Egg):
    def __init__(self, egg_config: EggConfig, egg_target: EggEntity):
        super().__init__(egg_config, xp_threshold=None)
        self._target_egg: EggEntity = egg_target
        self.test_only_move_velocity = Vector(0, 0)

    def _get_tracking_vector(self) -> Vector:
        vector_to_egg: Vector = self._get_vector_to_hitbox(
            self._target_egg.hitbox)
        try:
            direction_vector = vector_to_egg / abs(vector_to_egg)
        except ZeroDivisionError:
            direction_vector = Vector(0, 0)
        return direction_vector * self._movement_speed

    def move(self, velocity_vector: Vector) -> None:
        if self.is_dead:
            return

        move_vector: Vector = velocity_vector + self._get_tracking_vector()

        self.test_only_move_velocity = self._get_tracking_vector()

        self._damage_hitbox.x += move_vector.x_hat
        self._damage_hitbox.y += move_vector.y_hat
        self._hitbox.x += move_vector.x_hat
        self._hitbox.y += move_vector.y_hat

    @property
    def track_vector(self) -> Vector:
        return self._get_tracking_vector()

    def get_vector_to_hitbox(self, hitbox_target: Hitbox) -> Vector:
        return super()._get_vector_to_hitbox(hitbox_target)


@dataclass(frozen=True)
class EggnemyTag(Enum):
    EGGNEMY = auto()
    BOSS_EGGNEMY = auto()


@dataclass(frozen=True)
class EggnemyType:
    eggnemy_tag: EggnemyTag
    eggnemy: Eggnemy


@dataclass
class EggnemyList():
    _eggnemy_list: dict[int, EggnemyType]
    _eggnemy_list_len: int = 0
    _count = itertools.count()

    def append(self, eggnemy: EggnemyType) -> None:
        self._eggnemy_list[next(self._count)] = eggnemy
        if eggnemy.eggnemy_tag == EggnemyTag.EGGNEMY:
            self._eggnemy_list_len += 1

    def pop(self, index: int) -> None:
        # self._eggnemy_list.pop(index)
        del self._eggnemy_list[index]
        if self._eggnemy_list[index].eggnemy_tag == EggnemyTag.EGGNEMY:
            self._eggnemy_list_len -= 1

    def len(self) -> int:
        return self._eggnemy_list_len

    def _clean_list(self) -> None:
        for key in self._eggnemy_list:
            if self._eggnemy_list[key].eggnemy.is_dead:
                self.pop(key)

    def update_list(self, updater: Callable) -> None:
        cleanup: list[int] = []
        for key in self._eggnemy_list:
            updater(self._eggnemy_list[key].eggnemy)
            if self._eggnemy_list[key].eggnemy.is_dead:
                cleanup.append(key)
                # self.pop(i)
        if cleanup:
            self._eggnemy_list = {
                key: self._eggnemy_list[key] for key in self._eggnemy_list if key not in cleanup}
            # self._eggnemy_list = [self.eggnemy_list[i] for i in range(self.len()) if i not in cleanup]
            self._eggnemy_list_len -= len(cleanup)
            # breakpoint()
        # self._clean_list()

    @property
    def eggnemy_list(self) -> dict[int, EggnemyType]:
        return {key: self._eggnemy_list[key] for key in self._eggnemy_list}

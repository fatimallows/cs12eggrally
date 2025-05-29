from abc import ABC, abstractmethod

from _project_types import (EggConfig, Hitbox, EggEntity, EggInfo)
from _helpers import (CartesianPoint, Vector)

class Egg(ABC):
    def __init__(self, egg_config: EggConfig):
        self._hitbox: Hitbox = egg_config.hitbox
        self._movement_speed: float = egg_config.movement_speed
        self._max_health: float = egg_config.max_health
        self._health: float =  egg_config.max_health
        self._base_damage: float = egg_config.base_damage
        self._damage_hitbox_scale: float = egg_config.damage_hitbox_scale
        self._invincibility_frames: int = egg_config.invincibility_frames

        center_to_corner_vector: Vector = Vector(
            x_hat=self._hitbox.width / 2,
            y_hat=self._hitbox.height / 2
            )
        new_center_to_corner_vector: Vector = center_to_corner_vector * self._damage_hitbox_scale / 2
        new_reference_vector: Vector = self._hitbox.center.convert_to_vector() + new_center_to_corner_vector
        new_reference_point: CartesianPoint = new_reference_vector.convert_to_point()
        new_width_height_vector: Vector = (center_to_corner_vector * 2) * self._damage_hitbox_scale
        
        self._damage_hitbox: Hitbox = Hitbox(
            _coordinate=new_reference_point,
            _width=new_width_height_vector.x_hat,
            _height=new_width_height_vector.y_hat,
        )
        self._is_dead: bool = False
        
    def deal_damage(self, egg_entity: EggEntity, damage_value: float) -> None:
        """checks if the point on the target egg entity closest to current egg is within damage range

        Args:
            egg_entity (EggEntity): just put in an Egg 
            damage_value (float): damage value
        """
        if self.is_dead:
            return
        vector_to_hitbox: Vector = self._get_vector_to_hitbox(egg_entity.hitbox)
        if self._damage_hitbox.is_touching(vector_to_hitbox.convert_to_point()):
            egg_entity._take_damage(damage_value)
        
    def _take_damage(self, damage_value: float) -> None:
        """takes in damage, and changes the health accordingly

        Args:
            damage_value (float): damage dealt to the current Egg
        """
        if self._invincibility_frames > 0 and self.is_dead:
            return 
        
        self._health -= damage_value
        
        if self.health <= 0:
            self._is_dead = True
        
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
            delta_x: float =  hitbox_target.right - self.hitbox.left
        elif hitbox_target.left > self.hitbox.right:
            delta_x = hitbox_target.left - self.hitbox.right
        else:
            delta_x = 0
            
        return Vector(delta_x, delta_y)

    @abstractmethod  
    def move(self, velocity_vector: Vector) -> None:
        raise NotImplementedError
        
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
    def is_dead(self) -> float:
        return self._base_damage
    

class Eggnemy(Egg):
    def __init__(self, egg_config: EggConfig, egg_target: EggEntity):
        super().__init__(egg_config)
        self._target_egg: EggEntity = egg_target
        
    def _get_tracking_vector(self) -> Vector:
        vector_to_egg: Vector = self._get_vector_to_hitbox(self._target_egg.hitbox)
        try:
            direction_vector = vector_to_egg / abs(vector_to_egg)
        except ZeroDivisionError:
            direction_vector = Vector(0, 0)
        return direction_vector * self._movement_speed
        
    def move(self, velocity_vector: Vector) -> None:
        if self.is_dead:
            return
        
        move_vector: Vector = velocity_vector + self._get_tracking_vector()
        
        self.hitbox.x += move_vector.x_hat
        self.hitbox.y += move_vector.y_hat
        
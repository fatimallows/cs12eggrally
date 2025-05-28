from abc import ABC, abstractmethod
from project_types import (
    Vector, HitboxfulObject, EntityConfig, 
)


class Entity(ABC):
    """Entities are any objects in the game that can move around, fight, and bleed.
    All entities have a rectangle hitbox, just so we can have freedom in what
    we can use as the sprite"""
    def __init__(self, entity_config: EntityConfig, fps: int, width: int, height: int) -> None:
        self._x = entity_config.x
        self._y = entity_config.y
        self._width = entity_config.width
        self._height = entity_config.height
        self._movement_speed = entity_config.movement_speed
        self.base_health = entity_config.base_health
        self.base_damage = entity_config.base_damage
        
        self._fps = fps
        self._model_width = width
        self._model_height = height
        
        self._is_dead = False
        
    @abstractmethod
    def move(self, positionVector: Vector) -> None:
        raise NotImplementedError
    
    def tick(self) -> None:
        """anything that requires to be done every frame is done here"""
        if self.base_health <= 0:
            self._is_dead = True
        
    def get_distance_vector_to(self, other: HitboxfulObject) -> Vector:
        """Simply get the x and y distance of the two objects and slap them on a vector.
        Let R be the object on the right
        Let L be the object on the left
        Let T be the top most object
        Let B be the object on the bottom
        <R.left - L.right, B.top - T.bottom>

        Args:
            other (HitboxfulObject): just anything with a hitbox

        Returns:
            Vector: A position vector that embeds distance and magnitude to another object
        """
        # delta y
        if self.top > other.bottom:
            delta_y: float = other.bottom - self.top
        elif other.top > self.bottom:
            delta_y = other.top - self.bottom
        else:
            delta_y = 0
            
        # delta x
        if self.left > other.right:
            delta_x: float =  other.right - self.left
        elif other.left > self.right:
            delta_x = other.left - self.right
        else:
            delta_x = 0
            
        return Vector(delta_x, delta_y)
        
    def get_distance_to(self, other: HitboxfulObject) -> float:
        """Takes the coordinates of the other guy and calculates their distance

        Args:
            other (Entity): Whoever we are checking

        Returns:
            float: The square distance
        """
        
            
        # may have weird floating point errors
        # if x and y gets too big, it may cause overflows
        
        distance_vector: Vector = self.get_distance_vector_to(other)
        distance: float = abs(distance_vector)

        return distance
    
    def is_in_collission(self, other: 'Entity') -> bool:
        """Checks if it is in collission with the other entity

        Args:
            other (Entity): _description_

        Returns:
            bool: _description_
        """
        return self.get_distance_vector_to(other) == Vector(0, 0)
    
    def take_damage(self, attacker: 'Entity') -> None:
        self.base_health -= attacker.base_damage
        
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    @property
    def top(self) -> float:
        return self._y
    
    @property
    def bottom(self) -> float:
        return self._y + self._height
    
    @property
    def left(self) -> float:
        return self._x
    
    @property
    def right(self) -> float:
        return self._x + self._width
    
    # a little rough (this calculation will be done every single time its called lawl)
    @property
    def center(self) -> Vector:
        return Vector(
            x_hat=(self.right - self.left),
            y_hat=(self.top - self.bottom),
        ) / 2
        
    @property
    def is_dead(self) -> bool:
        return self._is_dead
    

class EggEntity(Entity):
    def __init__(self, 
                 entity_config: EntityConfig, fps: int, width: int, heigth: int, 
                 attack_radius: float) -> None:
        super().__init__(entity_config, fps, width, heigth)
        self.attack_radius: float = attack_radius
        self.invincibility_timer: float = 0
        
    def take_damage(self, attacker: Entity) -> None:
        if self.invincibility_timer == 0:
            super().take_damage(attacker)
            self.invincibility_timer = self._fps
    
    def attack_eggnemy(self, target: 'EggnemyEntity') -> None:
        if self.get_distance_to(target) <= self.attack_radius:
            target.take_damage(self)
        
    def move(self, direction_vector: Vector) -> None:
        delta_x: float = direction_vector.x_hat * self._movement_speed
        delta_y: float = direction_vector.y_hat * self._movement_speed
        
        self._x += delta_x if 0 <= self.left + delta_x and self.right + delta_x < self._model_width else 0
        self._y += delta_y if 0 <= self.top + delta_y and self.bottom + delta_y < self._model_height else 0
    
    def _tick_invincibility_timer(self) -> None:
        self.invincibility_timer -= 1 if self.invincibility_timer > 0 else 0
        
    def tick(self) -> None:
        super().tick()
        self._tick_invincibility_timer()
    
    
class EggnemyEntity(Entity):
    def __init__(self, 
                 entity_config: EntityConfig, fps: int, width: int, height: int, 
                 target_egg: EggEntity) -> None:
        super().__init__(entity_config, fps, width, height)   
        self.target_egg = target_egg
        
    def attack_egg(self, target: EggEntity) -> None:
        if self.is_in_collission(target):
            target.take_damage(self)
            
    def move(self, vector_to_egg: Vector) -> None:
        try:
            direction_vector: Vector = vector_to_egg / abs(vector_to_egg)
        except:
            direction_vector = Vector(0,0)
        velocity_vector: Vector = direction_vector * self._movement_speed
        self._x += velocity_vector.x_hat
        self._y += velocity_vector.y_hat
        
    def tick(self) -> None:
        super().tick()
        if self._is_dead:
            return
        vector_to_egg: Vector = self.get_distance_vector_to(self.target_egg)
        self.attack_egg(self.target_egg)
        self.move(vector_to_egg)
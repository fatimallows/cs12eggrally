from dataclasses import dataclass
from typing import Protocol
 
 
class UpdateHandler(Protocol):
    def update(self):
        ...
 
 
class DrawHandler(Protocol):
    def draw(self):
        ...
 
 
# @dataclass(frozen=True)
# class Rectangle:
#     x: float
#     y: float
#     width: float
#     height: float
 
#     @property
#     def top(self):
#         return self.y
 
#     @property
#     def bottom(self):
#         return self.y + self.height
 
#     @property
#     def left(self):
#         return self.x
 
#     @property
#     def right(self):
#         return self.x + self.width
 
 
# class PipePairInfo(Protocol):
#     @property
#     def top_pipe(self) -> Rectangle:
#         ...
 
#     @property
#     def bottom_pipe(self) -> Rectangle:
#         ...
 
 
# class BirdInfo(Protocol):
#     @property
#     def x(self) -> float:
#         ...
 
#     @property
#     def y(self) -> float:
#         ...
 
#     @property
#     def radius(self) -> float:
#         ...
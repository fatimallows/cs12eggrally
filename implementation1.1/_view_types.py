from __future__ import annotations
from abc import ABC
from typing import Protocol, Literal, Callable, Sequence

import itertools

type ObjectNode = ObjectBox | None
type Dimensions = Literal['x'] | Literal['y']
type ObjectType = (
    Literal['RootObject'] |
    Literal['DivObject'] |
    Literal['FloatObject'] |
    Literal['ContentObject']
)

# div is lowkey useless but i do not have the experience nor the luxyury of time to fix it sooo

# begs for a better desing but i am pressed on time soo
UNIQUE_IDENTIFIER = itertools.count()

"""
Invariant: parent dimensions >= child dimensions
"""


class ObjectBox(ABC):
    def __init__(self, x: int, y: int, width: int, height: int, parent: ObjectNode | None):
        self._object_x: int = x
        self._object_y: int = y
        self._object_width: int = width
        self._object_height: int = height

        self._parent: ObjectNode | None = parent
        self._children: Children = Children()

        self._tags: set[str] = set()

    def add_tag(self, tag: str) -> None:
        self._tags.add(tag)

    def add_tags(self, tags: Sequence[str]) -> None:
        for tag in tags:
            self.add_tag(tag)

    def remove_tag(self, tag: str) -> None:
        self._tags.remove(tag)

    @property
    def reference_point(self) -> dict[Dimensions, int]:
        return {
            'x': self._object_x,
            'y': self._object_y
        }

    @property
    def dimensions(self) -> dict[Dimensions, int]:
        return {
            'x': self._object_width,
            'y': self._object_height
        }

    @property
    def left(self) -> int:
        return self._object_x

    @property
    def right(self) -> int:
        return self._object_x + self._object_width

    @property
    def top(self) -> int:
        return self._object_y

    @property
    def bottom(self) -> int:
        return self._object_y + self._object_height

    @property
    def height(self) -> int:
        return self._object_height

    @property
    def width(self) -> int:
        return self._object_width

    @property
    def parent(self) -> ObjectNode:
        return self._parent

    @property
    def children(self) -> Children:
        return self._children

    def add_child(self, idstr: str, child: ObjectBox) -> None:
        self._children.add_child(idstr, child)

    @property
    def tags(self) -> set[str]:
        return self._tags


class Children:
    def __init__(self) -> None:
        self._children: dict[str, ObjectBox] = {}

    def add_child(self, idstr: str, child: ObjectBox) -> None:
        self._children[idstr] = child

    def remove_child(self, idstr: str) -> None:
        del self._children[idstr]

    def no_children(self) -> bool:
        return len(self._children.values()) == 0

    @property
    def children(self) -> dict[str, ObjectBox]:
        return {idstr: self._children[idstr] for idstr in self._children}


class ChildrenInfo(Protocol):
    @property
    def children(self) -> dict[str, ObjectBox]:
        ...


class RootObject(ObjectBox):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, None)
        self._tags.add('RootObject')


class DivObject(ObjectBox):
    def __init__(self, height: int, parent: ObjectBox):
        super().__init__(
            parent.reference_point['x'], parent.reference_point['y'], parent.dimensions['x'], height, parent)
        self._tags.add('DivObject')


class FloatObject(ObjectBox):
    def __init__(self, width: int, height: int, parent: ObjectBox):
        super().__init__(
            parent.reference_point['x'], parent.reference_point['y'], width, height, None)
        self._parent: ObjectBox = parent  # to appease the type checking gods
        self._tags.add('FloatingObject')

    def align_left(self) -> None:
        self._object_x = self._parent.reference_point['x']

    def align_right(self) -> None:
        self._object_x = self._parent.reference_point['x'] + \
            self._parent._object_width - self._object_width

    def align_horizontal_center(self) -> None:
        self._object_x = self._parent.reference_point['x'] + (
            self._parent._object_width - self._object_width) // 2

    def align_up(self) -> None:
        self._object_y = self._parent.reference_point['y']

    def align_down(self) -> None:
        self._object_y = self._parent.reference_point['y'] + \
            self._parent._object_height - self._object_height

    def align_vertical_center(self) -> None:
        self._object_y = self._parent.reference_point['y'] + (
            self._parent._object_height - self._object_height) // 2

    def align_true_center(self) -> None:
        self.align_vertical_center()
        self.align_horizontal_center()

    def float_to(self, x: int, y: int) -> None:
        self._object_x = x
        self._object_y = y


class ContentObject(DivObject):
    def __init__(self, content: Callable, parent: ObjectBox):
        super().__init__(parent._object_height, parent)
        self._tags = {'ContentObject'}
        self._content = content

    def draw_content(self):
        self._content()


class PyxelObjectModel:
    def __init__(self, screen_width: int, screen_height: int):
        self._root: RootObject = RootObject(
            x=0,
            y=0,
            width=screen_width,
            height=screen_height,
        )
        self.current_object: ObjectBox = self._root

    def go_to_node_with_tag(self, tag: str) -> None:
        self.current_object = self._root
        test = self._go_to_node_with_tag(tag, self._root)
        self.current_object = test if test is not None else self._root

    def _go_to_node_with_tag(self, tag: str, current_node: ObjectBox) -> ObjectBox | None:
        if tag in current_node.tags:
            return current_node

        if current_node.children.no_children():
            return None

        results = []
        for idstr in current_node.children.children:
            results.append(self._go_to_node_with_tag(
                tag, current_node.children.children[idstr]))

        for result in results:
            if result is not None:
                return result

        return None

    def add_child_current_object(self, object_box: ObjectBox) -> None:
        self.current_object.add_child(str(next(UNIQUE_IDENTIFIER)), object_box)

    def generate_div_object(self, height: int, parent: ObjectBox | Literal['self'], tags: Sequence[str]) -> DivObject:
        if parent == 'self':
            obj = DivObject(height, self.current_object)
        else:
            obj = DivObject(height, parent)
        obj.add_tags(tags)
        return obj

    def generate_float_object(self, width: int, height: int, parent: DivObject | Literal['self'], tags: Sequence[str]) -> FloatObject:
        if parent == 'self':
            obj = FloatObject(width, height, self.current_object)
        else:
            obj = FloatObject(width, height, parent)
        obj.add_tags(tags)
        return obj

    def generate_content_object(self, content: Callable, parent: ObjectBox | Literal['self'], tags: Sequence[str]) -> ContentObject:
        if parent == 'self':
            obj = ContentObject(content, self.current_object)
        else:
            obj = ContentObject(content, parent)
        obj.add_tags(tags)
        return obj

    @property
    def root(self) -> ObjectBox:
        return self._root

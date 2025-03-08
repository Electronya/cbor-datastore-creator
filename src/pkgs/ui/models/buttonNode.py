from dataclasses import dataclass, field
from .baseNode import BaseNode, NodeType


@dataclass
class ButtonData:
    """
    The button node data.
    """
    longPressTime: 3000
    inactiveTime: 6000


class ButtonNode(BaseNode):
    """
    The button node class.
    """
    def __init__(self, name: str, data: ButtonData, parent: BaseNode):
        super().__init__(name, NodeType.BUTTON, parent=parent)
        self._data = data


@dataclass
class ButtonArrayElement:
    """
    The button array element.
    """
    name: str


@dataclass
class ButtonArrayData:
    """
    The button array node data.
    """
    longPressTime: int = 3000
    inactiveTime: int = 6000
    elements: list[ButtonArrayElement] = field(default_factory=list)


class ButtonArrayNode(BaseNode):
    """
    The button array node class.
    """
    def __init__(self, name: str, data: ButtonArrayData, parent: BaseNode):
        super().__init__(name, NodeType.BUTTON_ARRAY, parent=parent)
        self._data = data

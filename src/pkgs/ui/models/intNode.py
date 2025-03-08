from dataclasses import dataclass, field
from .baseNode import BaseNode, NodeType


@dataclass
class IntData:
    """
    The int node data.
    """
    min: int
    max: int
    default: int


class IntNode(BaseNode):
    """
    The int node class.
    """
    def __init__(self, name: str, data: IntData, parent: BaseNode):
        super().__init__(name, NodeType.INT, parent=parent)
        self._data = data


@dataclass
class IntArrayElement:
    """
    The int array element.
    """
    name: str
    min: int
    max: int
    default: int


@dataclass
class IntArrayData:
    """
    The int array node data.
    """
    inNvm: bool = False
    elements: list[IntArrayElement] = field(default_factory=list)


class IntArrayNode(BaseNode):
    """
    The int array node class.
    """
    def __init__(self, name: str, data: IntArrayData, parent: BaseNode):
        super().__init__(name, NodeType.INT_ARRAY, parent=parent)
        self._data = data

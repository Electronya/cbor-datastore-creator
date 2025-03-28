from dataclasses import dataclass, field
from .baseNode import BaseNode, NodeType


@dataclass
class IntData:
    """
    The int node data.
    """
    min: int = 0
    max: int = 0
    default: int = 0


class IntNode(BaseNode):
    """
    The int node class.
    """
    def __init__(self, name: str, data: IntData, parent: BaseNode = None):
        super().__init__(name, NodeType.INT, parent=parent)
        self._data = data


@dataclass
class IntArrayElement:
    """
    The int array element.
    """
    name: str
    min: int = 0
    max: int = 0
    default: int = 0


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
    def __init__(self, name: str, data: IntArrayData, parent: BaseNode = None):
        super().__init__(name, NodeType.INT_ARRAY, parent=parent)
        self._data = data

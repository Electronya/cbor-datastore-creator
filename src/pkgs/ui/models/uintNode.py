from dataclasses import dataclass, field
from .baseNode import BaseNode, NodeType


@dataclass
class UintData:
    """
    The uint node data.
    """
    min: int
    max: int
    default: int


class UintNode(BaseNode):
    """
    The uint node class.
    """
    def __init__(self, name: str, data: UintData, parent: BaseNode = None):
        super().__init__(name, NodeType.UINT, parent=parent)
        self._data = data


@dataclass
class UintArrayElement:
    """
    The uint array element.
    """
    name: str
    min: int
    max: int
    default: int


@dataclass
class UintArrayData:
    """
    The uint array node data.
    """
    inNvm: bool = False
    elements: list[UintArrayElement] = field(default_factory=list)


class UintArrayNode(BaseNode):
    """
    The uint array node class.
    """
    def __init__(self, name: str, data: UintArrayData,
                 parent: BaseNode = None):
        super().__init__(name, NodeType.UINT_ARRAY, parent=parent)
        self._data = data

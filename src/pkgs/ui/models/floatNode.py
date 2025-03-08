from dataclasses import dataclass, field
from .baseNode import BaseNode, NodeType


@dataclass
class FloatData:
    """
    The float node data.
    """
    min: float
    max: float
    default: float


class FloatNode(BaseNode):
    """
    The float node class.
    """
    def __init__(self, name: str, data: FloatData, parent: BaseNode):
        super().__init__(name, NodeType.FLOAT, parent=parent)
        self._data = data


@dataclass
class FloatArrayElement:
    """
    The float array element.
    """
    name: str
    min: float
    max: float
    default: float


@dataclass
class FloatArrayData:
    """
    The float array node data.
    """
    inNvm: bool = False
    elements: list[FloatArrayElement] = field(default_factory=list)


class FloatArrayNode(BaseNode):
    """
    The float array node class.
    """
    def __init__(self, name: str, data: FloatArrayData, parent: BaseNode):
        super().__init__(name, NodeType.FLOAT_ARRAY, parent=parent)
        self._data = data

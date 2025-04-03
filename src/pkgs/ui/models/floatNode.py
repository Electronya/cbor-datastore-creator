from dataclasses import dataclass, field
from .baseNode import BaseNode, NodeType


@dataclass
class FloatData:
    """
    The float node data.
    """
    min: float = 0.0
    max: float = 0.0
    default: float = 0.0


class FloatNode(BaseNode):
    """
    The float node class.
    """
    def __init__(self, name: str, data: FloatData, parent: BaseNode = None):
        super().__init__(name, NodeType.FLOAT, parent=parent)
        self._data = data

    def getMinimum(self) -> float:
        """
        Get the minimum value.

        Return
            The minimum value of the float.
        """
        return self._data.min

    def setMinimum(self, min: float) -> None:
        """
        Set the minimum value.

        Param
            min: The minimum value of the float.
        """
        self._data.min = min

    def getMaximum(self) -> float:
        """
        Get the maximum value.

        Return
            The maximum value of the float.
        """
        return self._data.max

    def setMaximum(self, max: float) -> None:
        """
        Set the maximum value.

        Param
            min: The maximum value of the float.
        """
        self._data.max = max

    def getDefault(self) -> float:
        """
        Get the default value.

        Return
            The default value of the float.
        """
        return self._data.default

    def setDefault(self, default: float) -> None:
        """
        Set the default value.

        Param
            min: The default value of the float.
        """
        self._data.default = default


@dataclass
class FloatArrayElement:
    """
    The float array element.
    """
    name: str
    min: float = 0.0
    max: float = 0.0
    default: float = 0.0


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
    def __init__(self, name: str, data: FloatArrayData,
                 parent: BaseNode = None):
        super().__init__(name, NodeType.FLOAT_ARRAY, parent=parent)
        self._data = data

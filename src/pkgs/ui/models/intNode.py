from dataclasses import dataclass, field
from .baseNode import BaseNode, NodeType


@dataclass
class IntData:
    """
    The int node data.
    """
    min: int = -1000000
    max: int = 1000000
    default: int = 0


class IntNode(BaseNode):
    """
    The int node class.
    """
    def __init__(self, name: str, data: IntData, parent: BaseNode = None):
        super().__init__(name, NodeType.INT, parent=parent)
        self._data = data

    def getMinimum(self) -> int:
        """
        Get the minimum value.

        Return
            The minimum value of the int.
        """
        return self._data.min

    def setMinimum(self, min: int) -> None:
        """
        Set the minimum value.

        Param
            min: The minimum value of the int.
        """
        self._data.min = min

    def getMaximum(self) -> int:
        """
        Get the maximum value.

        Return
            The maximum value of the int.
        """
        return self._data.max

    def setMaximum(self, max: int) -> None:
        """
        Set the maximum value.

        Param
            min: The maximum value of the int.
        """
        self._data.max = max

    def getDefault(self) -> int:
        """
        Get the default value.

        Return
            The default value of the int.
        """
        return self._data.default

    def setDefault(self, default: int) -> None:
        """
        Set the default value.

        Param
            min: The default value of the int.
        """
        self._data.default = default


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

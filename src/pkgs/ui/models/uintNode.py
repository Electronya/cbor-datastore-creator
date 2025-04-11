from dataclasses import dataclass, field
from .baseNode import BaseNode, NodeType


@dataclass
class UintData:
    """
    The uint node data.
    """
    min: int = 0
    max: int = 1000000
    default: int = 0


class UintNode(BaseNode):
    """
    The uint node class.
    """
    def __init__(self, name: str, data: UintData, parent: BaseNode = None):
        super().__init__(name, NodeType.UINT, parent=parent)
        self._data = data

    def getMinimum(self) -> int:
        """
        Get the minimum value.

        Return
            The minimum value of the uint.
        """
        return self._data.min

    def setMinimum(self, min: int) -> None:
        """
        Set the minimum value.

        Param
            min: The minimum value of the uint.
        """
        self._data.min = min

    def getMaximum(self) -> int:
        """
        Get the maximum value.

        Return
            The maximum value of the uint.
        """
        return self._data.max

    def setMaximum(self, max: int) -> None:
        """
        Set the maximum value.

        Param
            min: The maximum value of the uint.
        """
        self._data.max = max

    def getDefault(self) -> int:
        """
        Get the default value.

        Return
            The default value of the uint.
        """
        return self._data.default

    def setDefault(self, default: int) -> None:
        """
        Set the default value.

        Param
            min: The default value of the uint.
        """
        self._data.default = default

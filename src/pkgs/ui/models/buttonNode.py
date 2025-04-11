from dataclasses import dataclass, field
from .baseNode import BaseNode, NodeType


@dataclass
class ButtonData:
    """
    The button node data.
    """
    longPressTime: int = 3000
    inactiveTime: int = 6000


class ButtonNode(BaseNode):
    """
    The button node class.
    """
    def __init__(self, name: str, data: ButtonData, parent: BaseNode = None):
        super().__init__(name, NodeType.BUTTON, parent=parent)
        self._data = data

    def getLongPressTime(self) -> int:
        """
        Get the button long press time.

        Return
            The button long press time.
        """
        return self._data.longPressTime

    def setLongPressTime(self, time: int) -> None:
        """
        Set the button long press time.

        Param
            time: The button long press time.
        """
        self._data.longPressTime = time

    def getInactiveTime(self) -> int:
        """
        Get the button inactive time.

        Return
            The button inactive time.
        """
        return self._data.inactiveTime

    def setInactiveTime(self, time: int) -> None:
        """
        Set the button inactive time.

        Param
            time: The button inactive time.
        """
        self._data.inactiveTime = time

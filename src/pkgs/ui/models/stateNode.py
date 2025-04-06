import logging

from PySide6.QtCore import Qt

from .baseNode import BaseNode


class StateNode(object):
    """
    The state node for the multi-state object.
    """
    def __init__(self, name: str, value: int, parent: BaseNode = None):
        """
        Constructor.

        Param
            name: The state name.
            value: The state value.
            parent: The node parent.
        """
        self._logger = logging.getLogger(f"app.datastoreModel.MULTI_STATE."
                                         f"state.{name}")
        self._name = name
        self._value = value

    def getName(self) -> str:
        """
        Get the state name.

        Return
            The state name.
        """
        return self._name

    def setName(self, name: str) -> None:
        """
        Set the state name.

        Param
            name: The state name.
        """
        self._name = name

    def getValue(self) -> int:
        """
        Get the state value.

        Return
            The state value.
        """
        return self._value

    def setValue(self, value: int) -> None:
        """
        Set the state value.

        Param
            value: The state value.
        """
        self._value = value

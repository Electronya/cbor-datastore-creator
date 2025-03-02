from enum import Enum
from PySide6.QtCore import Qt
from typing import Protocol


class DatastoreProto(Protocol):
    """
    The datastore object protocol.
    """
    def getName(self) -> str:
        pass

    def setName(self, name: str) -> None:
        pass


class DatastoreNodeType(Enum):
    """
    The node type enum
    """
    STORE = 1
    OBJ_LIST = 2
    OBJECT = 3


class DatastoreNode(object):
    """
    The datastore tree node class.

    Param
        type: The node type.
        data: The node data.
        name: The node name.
        parent: The node parent.
    """
    def __init__(self, type: DatastoreNodeType, data: DatastoreProto = None,
                 name: str = None, parent: 'DatastoreNode' = None) -> None:
        self._type = type
        self._data = data
        self._name: str = name
        self._parent: 'DatastoreNode' = parent
        self._children: list['DatastoreNode'] = []

        if parent is not None:
            self._parent.addChild(self)

    def getName(self) -> str:
        """
        Get the node name.

        Return
            The node name.
        """
        if self._type != DatastoreNodeType.OBJ_LIST:
            return self._data.getName()
        return self._name

    def setName(self, name: str) -> None:
        """
        Set the node name.

        Param
            name: the node name.
        """
        if self._type != DatastoreNodeType.OBJ_LIST:
            self._data.setName(name)

    def getChildCount(self) -> int:
        """
        Get the node child count.

        Return
            The node child count.
        """
        return len(self._children)

    def getChild(self, row: int) -> 'DatastoreNode':
        """
        Get the child at the given row.

        Param
            row: The row of the child.

        Return
            The child.
        """
        if self._type != DatastoreNodeType.OBJECT:
            return self._children[row]

    def addChild(self, child: 'DatastoreNode') -> None:
        """
        Add a child to the node.

        Param
            child: The child to add.
        """
        self._children.append(child)

    def getParent(self) -> 'DatastoreNode':
        """
        Get the node parent.

        Return
            The node parent.
        """
        return self._parent

    def getRow(self) -> int:
        """
        Get the node row.

        Return
            The node row.
        """
        if self._parent is not None:
            return self._parent._children.index(self)

    def getData(self) -> DatastoreProto:
        """
        Get the node data.

        Return
            The node data.
        """
        return self._data

    def getFlags(self) -> int:
        """
        Get the node Qt flags.

        Return
            The node Qt flag.
        """
        flags = Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        if self._type != DatastoreNodeType.OBJ_LIST:
            flags |= Qt.ItemFlag.ItemIsEditable
        return flags

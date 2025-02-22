from typing import Protocol, runtime_checkable
from PySide6.QtCore import QModelIndex, Qt


class DatastoreProto(Protocol):
    """
    The datastore object protocol.
    """
    def getName(self) -> str:
        pass


class DatastoreNode(object):
    """
    The datastore tree node class.

    Param
        data: The node data.
        name: The node name.
        parent: The node parent.
    """
    def __init__(self, data: DatastoreProto = None,
                 name: str = None, parent: QModelIndex = None) -> None:
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
        if self._name is None:
            return self._data.getName()
        return self._name

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
        if self._parent is None:
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemFlag.ItemIsSelectable

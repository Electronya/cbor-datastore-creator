from enum import Enum
from logging import getLogger
from PySide6.QtCore import Qt


class NodeType(Enum):
    """
    The node type enum
    """
    STORE = 1
    OBJ_LIST = 2
    BUTTON = 3
    BUTTON_ARRAY = 4
    FLOAT = 5
    FLOAT_ARRAY = 6
    INT = 7
    INT_ARRAY = 8
    MULTI_STATE = 9
    UINT = 10
    UINT_ARRAY = 11


class BaseNode(object):
    """
    Datastore base tree node.
    """
    def __init__(self, name: str, type: NodeType,
                 parent: 'BaseNode' = None) -> None:
        """
        Base datastore tree node.
        """
        self._logger = getLogger(f"app.datastoreModel.{type.name}.{name}")
        self._name = name
        self._type = type
        self._parent = parent
        self._children: list['BaseNode'] = []
        if parent is not None:
            parent.addChild(self)

    def getName(self) -> str:
        """
        Get the node name.

        Return
            The node name.
        """
        return self._name

    def setName(self, name: str) -> None:
        """
        Set the node name.

        Param
            name: The node name.
        """
        self._name = name

    def getType(self) -> NodeType:
        """
        Get the node type.

        Return
            The node type.
        """
        return self._type

    def getChildCount(self) -> int:
        """
        Get the node child count.

        Return
            The node child count.
        """
        return len(self._children)

    def getChild(self, row: int) -> 'BaseNode':
        """
        Get the node child node at the given row.

        Param
            row: The row of the requested child.

        Return
            The child node at the given row.
        """
        if row < len(self._children):
            return self._children[row]
        return None

    def addChild(self, child: 'BaseNode') -> None:
        """
        Add a child to the node.

        Param
            child: The child to add.
        """
        self._children.append(child)
        child._parent = self

    def addChildAt(self, row: int, child: 'BaseNode') -> bool:
        """
        Add a child at the given row.

        Param
            row: The insertion row.
            child: The child to add.

        Return
            True if successful, false otherwise.
        """
        if row >= 0 and row <= len(self._children):
            self._logger.info(f"adding child at {row}")
            self._children.insert(row, child)
            child._parent = self
            return True
        return False

    def removeChildAt(self, row: int) -> bool:
        """
        Remove the child at the given row.

        Param
            row: The row of the child node to remove.

        Return
            True fi successful, false otherwise.
        """
        if row >= 0 and row < len(self._children):
            self._children.pop(row)
            return True
        return False

    def getParent(self) -> 'BaseNode':
        """
        Get the parent.

        Return
            The node parent.
        """
        return self._parent

    def getRow(self) -> int | None:
        """
        Get the node row.

        Return
            The row of the node if it has a parent, none otherwise.
        """
        if self._parent is not None:
            return self._parent._children.index(self)
        return None

    def getFlags(self) -> int:
        """
        Get the node item flags.

        Return
            The node item flags.
        """
        flags = Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        if self._type != NodeType.OBJ_LIST:
            flags |= Qt.ItemFlag.ItemIsEditable
        return flags

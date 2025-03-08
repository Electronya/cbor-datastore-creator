from PySide6 import QtCore as qtc

from .baseNode import BaseNode, NodeType
from .buttonNode import ButtonArrayData, ButtonArrayNode, \
    ButtonData, ButtonNode
from .floatNode import FloatArrayData, FloatArrayNode, FloatData, FloatNode
from .intNode import IntArrayData, IntArrayNode, IntData, IntNode
from .multiStateNode import MultiStateData, MultiStateNode
from .uintNode import UintArrayData, UintArrayNode, UintData, UintNode


class DatastoreModel(qtc.QAbstractItemModel):
    """
    The datastore model class.
    """
    def __init__(self, root: BaseNode, parent: qtc.QObject = None):
        super(DatastoreModel, self).__init__(parent)
        self._root = root

    def _appendButtonNode(self, buttonList: BaseNode) -> None:
        """
        Append a button node.

        Param
            buttonList: The button list node.
        """
        node = ButtonNode('NEW_BUTTON', ButtonData())
        buttonList.addChild(node)

    def rowCount(self, index: qtc.QModelIndex) -> int:
        """
        Get the row count.

        Param
            index: the index of the node.

        Return
            The row count.
        """
        node = self._root
        if index.isValid():
            node = index.internalPointer()
        return node.getChildCount()

    def columnCount(self, index: qtc.QModelIndex) -> int:
        """
        Get the column count.

        Param
            index the index of the node.

        Return
            The column count.
        """
        return 1

    def data(self, index: qtc.QModelIndex, role: int) -> str:
        """
        Get the display data of the node at the given index.

        Param
            index: The index of the node.
            role: The role used to call this method.

        Return
            The display data of the node.
        """
        node = self._root
        if index.isValid():
            node = index.internalPointer()
        if role == qtc.Qt.ItemDataRole.DisplayRole or \
                role == qtc.Qt.ItemDataRole.EditRole:
            return node.getName()

    def setData(self, index: qtc.QModelIndex, data: str, role: int) -> bool:
        """
        Set the display data of the noe at the given index.

        Param
            index: The index of the node.
            data: The display data.
            role: The role used to call this method.

        Return
            True if the operation succeeded, false otherwise.
        """
        if index.isValid() and role == qtc.Qt.ItemDataRole.EditRole:
            node = index.internalPointer()
            node.setName(data)
            return True
        return False

    def headerData(self, section: int, orientation: qtc.Qt.Orientation,
                   role: int) -> str:
        """
        Get the header display data.

        Param
            section: The header section index.
            orientation: The header orientation.
            role: The role used to call this method.

        Return
            The display data for the header.
        """
        pass

    def flags(self, index: qtc.QModelIndex) -> int:
        """
        Get the flags of the node at the given index.

        Param
            index: The index of the node.

        Return
            The flags of the node.
        """
        node = self._root
        if index.isValid():
            node = index.internalPointer()
        return node.getFlags()

    def parent(self, index: qtc.QModelIndex) -> qtc.QModelIndex:
        """
        Get the node at the given index the parent index.

        Param
            index: The index of the node.

        Return
            The index of the parent.
        """
        node = index.internalPointer()
        parent = node.getParent()
        if parent == self._root:
            return qtc.QModelIndex()
        return self.createIndex(parent.getRow(), 0, parent)

    def index(self, row: int, column: int,
              index: qtc.QModelIndex) -> qtc.QModelIndex:
        """
        Get the node index at the given row and column.

        Param
            row: The node row.
            column: The node column.
            parent: The node parent.

        Return
            The node index.
        """
        node = self._root
        if index.isValid():
            node = index.internalPointer()

        child = node.getChild(row)

        if child is None:
            return qtc.QModelIndex()
        return self.createIndex(row, column, child)

    def insertRow(self, row: int, parent: qtc.QModelIndex) -> bool:
        """
        Insert a row.

        Param
            row: The new row position.
            parent: The parent node to which add a row.

        Return
            True if the operation succeeds, false otherwise.
        """
        node = self._root
        if parent.isValid():
            node = parent.internalPointer()
        self.beginInsertRows(parent, row, row + 1)
        self.endInsertRows()

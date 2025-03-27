from logging import getLogger
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
        self._logger = getLogger('app.datastoreModel')
        self._root = root

    def _insertButtonNode(self, list: BaseNode, row: int) -> None:
        """
        Insert a button node.

        Param
            list: The button list.
            row: The insertion row.
        """
        self._logger.info(f"inserting a new button at index {row}")
        node = ButtonNode('NEW_BUTTON', ButtonData())
        list.addChildAt(row, node)

    def _insertButtonArrayNode(self, list: BaseNode, row: int) -> None:
        """
        Insert a button array node.

        Param
            list: The button array list node.
            row: The insertion row.
        """
        node = ButtonArrayNode('NEW_BUTTON_ARRAY', ButtonArrayData())
        list.addChildAt(row, node)

    def _insertFloatNode(self, list: BaseNode, row: int) -> None:
        """
        Insert a float node.

        Param
            list: The float list node.
            row: The insertion row.
        """
        node = FloatNode('NEW_FLOAT', FloatData())
        list.addChildAt(row, node)

    def _insertFloatArrayNode(self, list: BaseNode, row: int) -> None:
        """
        Insert a float array node.

        Param
            list: The float array list node.
            row: The insertion row.
        """
        node = FloatArrayNode('NEW_FLOAT_ARRAY', FloatArrayData())
        list.addChildAt(row, node)

    def _insertIntNode(self, list: BaseNode, row: int) -> None:
        """
        Insert a int node.

        Param
            list: The int list node.
            row: The insertion row.
        """
        node = IntNode('NEW_INT', IntData())
        list.addChildAt(row, node)

    def _insertIntArrayNode(self, list: BaseNode, row: int) -> None:
        """
        Insert a int array node.

        Param
            list: The int array list node.
            row: The insertion row.
        """
        node = IntArrayNode('NEW_INT_ARRAY', IntArrayData())
        list.addChildAt(row, node)

    def _insertMultiStateNode(self, list: BaseNode, row: int) -> None:
        """
        Insert a multi-state node.

        Param
            list: The multi-state list node.
            row: The insertion row.
        """
        node = MultiStateNode('NEW_MULTI_STATE', MultiStateData())
        list.addChildAt(row, node)

    def _insertUintNode(self, list: BaseNode, row: int) -> None:
        """
        Insert a uint node.

        Param
            list: The uint list node.
            row: The insertion row.
        """
        node = UintNode('NEW_UINT', UintData())
        list.addChildAt(row, node)

    def _insertUintArrayNode(self, list: BaseNode, row: int) -> None:
        """
        Insert a uint array node.

        Param
            list: The uint array list node.
            row: The insertion row.
        """
        node = UintArrayNode('NEW_UINT_ARRAY', UintArrayData())
        list.addChildAt(row, node)

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
            parent: The index of the node in which to insert a row.

        Return
            True if the operation succeeds, false otherwise.
        """
        if not parent.isValid():
            return False
        node = parent.internalPointer()
        result = True
        self.beginInsertRows(parent, row, row + 1)
        self._logger.debug(f"new object type: {node.getName()}")
        match node.getName():
            case NodeType.BUTTON.name:
                self._insertButtonNode(node, row)
            case NodeType.BUTTON_ARRAY.name:
                self._insertButtonArrayNode(node, row)
            case NodeType.FLOAT.name:
                self._insertFloatNode(node, row)
            case NodeType.FLOAT_ARRAY.name:
                self._insertFloatArrayNode(node, row)
            case NodeType.INT.name:
                self._insertIntNode(node, row)
            case NodeType.INT_ARRAY.name:
                self._insertIntArrayNode(node, row)
            case NodeType.MULTI_STATE.name:
                self._insertMultiStateNode(node, row)
            case NodeType.UINT.name:
                self._insertUintNode(node, row)
            case NodeType.UINT_ARRAY.name:
                self._insertUintArrayNode(node, row)
            case _:
                result = False
        self.endInsertRows()
        return result

    def removeRow(self, row: int, parent: qtc.QModelIndex) -> bool:
        """
        Remove a row.

        Param
            row: The row to remove.
            parent: The index of the node in which to remove the row.

        Return
            True if successful, false otherwise.
        """
        if not parent.isValid():
            return False
        node = parent.internalPointer()
        result = True
        self.beginRemoveRows(parent, row, row + 1)
        match node.getName():
            case NodeType.BUTTON.name | NodeType.BUTTON_ARRAY.name | \
                    NodeType.FLOAT.name | NodeType.FLOAT_ARRAY.name | \
                    NodeType.INT.name | NodeType.INT_ARRAY.name | \
                    NodeType.MULTI_STATE.name | NodeType.UINT.name | \
                    NodeType.UINT_ARRAY.name:
                node.removeChildAt(row)
            case _:
                result = False
        self.endRemoveRows()
        return result

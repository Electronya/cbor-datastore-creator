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

    def _appendButtonNode(self, list: BaseNode) -> None:
        """
        Append a button node.

        Param
            list: The button list node.
        """
        node = ButtonNode('NEW_BUTTON', ButtonData())
        list.addChild(node)

    def _insertButtonNode(self, list: BaseNode, row: int) -> None:
        """
        Insert a button node.

        Param
            list: The button list.
            row: The insertion row.
        """
        node = ButtonNode('NEW_BUTTON', ButtonData())
        list.addChildAt(row, node)

    def _appendButtonArrayNode(self, list: BaseNode) -> None:
        """
        Append a button array node.

        Param
            list: The button array list node.
        """
        node = ButtonArrayNode('NEW_BUTTON_ARRAY', ButtonArrayData())
        list.addChild(node)

    def _insertButtonArrayNode(self, list: BaseNode, row: int) -> None:
        """
        Insert a button array node.

        Param
            list: The button array list node.
            row: The insertion row.
        """
        node = ButtonArrayNode('NEW_BUTTON_ARRAY', ButtonArrayData())
        list.addChildAt(row, node)

    def _appendFloatNode(self, list: BaseNode) -> None:
        """
        Append a float node.

        Param
            list: The float list node.
        """
        node = FloatNode('NEW_FLOAT', FloatData())
        list.addChild(node)

    def _insertFloatNode(self, list: BaseNode, row: int) -> None:
        """
        Insert a float node.

        Param
            list: The float list node.
            row: The insertion row.
        """
        node = FloatNode('NEW_FLOAT', FloatData())
        list.addChildAt(row, node)

    def _appendFloatArrayNode(self, list: BaseNode) -> None:
        """
        Append a float array node.

        Param
            list: The float array list node.
        """
        node = FloatArrayNode('NEW_FLOAT_ARRAY', FloatArrayData())
        list.addChild(node)

    def _insertFloatArrayNode(self, list: BaseNode, row: int) -> None:
        """
        Insert a float array node.

        Param
            list: The float array list node.
            row: The insertion row.
        """
        node = FloatArrayNode('NEW_FLOAT_ARRAY', FloatArrayData())
        list.addChildAt(row, node)

    def _appendIntNode(self, list: BaseNode) -> None:
        """
        Append a int node.

        Param
            list: The int list node.
        """
        node = IntNode('NEW_INT', IntData())
        list.addChild(node)

    def _insertIntNode(self, list: BaseNode, row: int) -> None:
        """
        Insert a int node.

        Param
            list: The int list node.
            row: The insertion row.
        """
        node = IntNode('NEW_INT', IntData())
        list.addChildAt(row, node)

    def _appendIntArrayNode(self, list: BaseNode) -> None:
        """
        Append a int array node.

        Param
            list: The int array list node.
        """
        node = IntArrayNode('NEW_INT_ARRAY', IntArrayData())
        list.addChild(node)

    def _insertIntArrayNode(self, list: BaseNode, row: int) -> None:
        """
        Insert a int array node.

        Param
            list: The int array list node.
            row: The insertion row.
        """
        node = IntArrayNode('NEW_INT_ARRAY', IntArrayData())
        list.addChildAt(row, node)

    def _appendMultiStateNode(self, list: BaseNode) -> None:
        """
        Append a multi-state node.

        Param
            list: The multi-state list node.
        """
        node = MultiStateNode('NEW_MULTI_STATE', MultiStateData())
        list.addChild(node)

    def _insertMultiStateNode(self, list: BaseNode, row: int) -> None:
        """
        Insert a multi-state node.

        Param
            list: The multi-state list node.
            row: The insertion row.
        """
        node = MultiStateNode('NEW_MULTI_STATE', MultiStateData())
        list.addChildAt(row, node)

    def _appendUintNode(self, list: BaseNode) -> None:
        """
        Append a uint node.

        Param
            list: The uint list node.
        """
        node = UintNode('NEW_UINT', UintData())
        list.addChild(node)

    def _insertUintNode(self, list: BaseNode, row: int) -> None:
        """
        Insert a uint node.

        Param
            list: The uint list node.
            row: The insertion row.
        """
        node = UintNode('NEW_UINT', UintData())
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
            parent: The parent node to which add a row.

        Return
            True if the operation succeeds, false otherwise.
        """
        node = self._root
        if parent.isValid():
            node = parent.internalPointer()
        self.beginInsertRows(parent, row, row + 1)
        self.endInsertRows()

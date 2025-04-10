import logging

from PySide6 import QtCore as qtc

from .stateNode import StateNode


class StateListModel(qtc.QAbstractTableModel):
    """
    The state list model.
    """
    def __init__(self, states: list[StateNode] = [],
                 parent: qtc.QObject = None) -> None:
        """
        Constructor.

        Param
            states: The list of state.
            parent: The parent of the model.
        """
        super(StateListModel, self).__init__(parent)
        self._logger = logging.getLogger('app.datastoreModel.MULTI_STATE.'
                                         'stateList')
        self._states = states

    def rowCount(self, parent: qtc.QModelIndex) -> int:
        """
        Get the model row count.

        Param
            The index of the parent.

        Return
            The model row count.
        """
        return len(self._states)

    def columnCount(self, parent: qtc.QModelIndex):
        """
        Get the model column count.

        Param
            parent: The index of the parent.

        Return
            The model column count.
        """
        return 2

    def data(self, index: qtc.QModelIndex, role: int) -> str | int:
        """
        Get the node display data.

        Param:
            index: The node index.
            role: The data role.

        Return
            The state display data.
        """
        if role == qtc.Qt.ItemDataRole.DisplayRole:
            return self._states[index.row()].getName() if index.column() == 0 \
                else self._states[index.row()].getValue()

    def headerData(self, section: int,
                   orientation: qtc.Qt.Orientation, role: int) -> str:
        """
        Get the header display data.

        Param
            section: The header section.
            orientation: The header orientation.
            role: The data role.

        Return
            The header display data.
        """
        headers = ['Name', 'Value']
        if role == qtc.Qt.ItemDataRole.DisplayRole and \
                orientation == qtc.Qt.Orientation.Horizontal:
            return headers[section]

    def flags(self, index: qtc.QModelIndex) -> qtc.Qt.ItemFlag:
        """
        Get the node flags.

        Param
            index: The node index.

        Return
            The node flags.
        """
        return qtc.Qt.ItemFlag.ItemIsSelectable | \
            qtc.Qt.ItemFlag.ItemIsEnabled | qtc.Qt.ItemFlag.ItemIsEditable

    def setData(self, index: qtc.QModelIndex, value: str | int,
                role: int = qtc.Qt.ItemDataRole.EditRole) -> bool:
        """
        Set the node data.

        Param
            index: The node index.
            value: The new value.
            role: The data role.

        Return
            True if successful, false otherwise.
        """
        if role == qtc.Qt.ItemDataRole.EditRole:
            if index.column() == 0:
                self._states[index.row()].setName(value)
            else:
                self._states[index.row()].setValue(value)
            return True
        return False

    def insertRow(self, row: int, parent: qtc.QModelIndex) -> bool:
        """
        Insert a new state at row.

        Param:
            row: The insertion row.
            parent: The index of the parent node.

        Return
            True.
        """
        self.beginInsertRows(qtc.QModelIndex(), row, row + 1)
        self._states.insert(row, StateNode(f"STATE_{row}", row))
        self.endInsertRows()
        self.layoutChanged.emit()
        return True

    def removeRow(self, row: int, parent: qtc.QModelIndex) -> bool:
        """
        Remove the given row.

        Param
            row: The row to remove.
            parent: The index of the parent node.

        Return
            True if successful, false otherwise.
        """
        if row >= 0 and row < len(self._states):
            self.beginRemoveRows(qtc.QModelIndex(), row, row + 1)
            self._states.pop(row)
            self.endRemoveRows()
            self.layoutChanged.emit()
            return True
        return False

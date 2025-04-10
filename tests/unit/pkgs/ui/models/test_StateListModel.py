from PySide6 import QtCore as qtc
from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.models import StateListModel                       # noqa: E402


class TestStateListModel(TestCase):
    """
    The StateListModel test cases.
    """
    def setUp(self) -> None:
        self._loggingMod = 'pkgs.ui.models.stateListModel.logging'
        self._BaseCls = 'pkgs.ui.models.stateListModel.qtc.QAbstractTableModel'
        self._IndexCls = 'pkgs.ui.models.stateListModel.qtc.QModelIndex'
        self._StateNodeCls = 'pkgs.ui.models.stateListModel.StateNode'
        self._states = [Mock(), Mock(), Mock(), Mock()]
        with patch(f"{self._BaseCls}.__init__"), patch(self._loggingMod):
            self._uut = StateListModel(states=self._states)
            self._uut.layoutChanged = Mock()

    def test_constructorBaseClassInit(self) -> None:
        """
        The constructor must initialize the model base class.
        """
        parent = Mock()
        with patch(f"{self._BaseCls}.__init__") as mockedBaseCls, \
                patch(self._loggingMod):
            StateListModel(parent=parent)
            mockedBaseCls.assert_called_once_with(parent)

    def test_ConstructorGetLogger(self) -> None:
        """
        The constructor must get the logger.
        """
        with patch(f"{self._BaseCls}.__init__"), \
                patch(self._loggingMod) as mockedLogging:
            StateListModel()
            mockedLogging.getLogger \
                .assert_called_once_with('app.datastoreModel.MULTI_STATE.'
                                         'stateList')

    def test_constructorSaveStateList(self) -> None:
        """
        The constructor must save the state list.
        """
        states = [Mock(), Mock(), Mock()]
        with patch(f"{self._BaseCls}.__init__"), patch(self._loggingMod):
            uut = StateListModel(states=states)
            self.assertEqual(states, uut._states)

    def test_rowCountReturnRowCount(self) -> None:
        """
        The rwoCount method must return the model row count.
        """
        self.assertEqual(len(self._states), self._uut.rowCount(Mock()))

    def test_columnCountReturnColumnCount(self) -> None:
        """
        The columnCount method must return the model column count.
        """
        self.assertEqual(2, self._uut.columnCount(Mock()))

    def test_dataReturnName(self) -> None:
        """
        The data method must return the state name when the role is the display
        one and the column is 0.
        """
        role = qtc.Qt.ItemDataRole.DisplayRole
        index = Mock()
        row = 1
        column = 0
        name = 'test node'
        index.row.return_value = row
        index.column.return_value = column
        self._states[row].getName.return_value = name
        self.assertEqual(name, self._uut.data(index, role))

    def test_dataReturnValue(self) -> None:
        """
        The data method must return the state value when the role is the
        display one and the column is 1.
        """
        role = qtc.Qt.ItemDataRole.DisplayRole
        index = Mock()
        row = 1
        column = 1
        value = 2
        index.row.return_value = row
        index.column.return_value = column
        self._states[row].getValue.return_value = value
        self.assertEqual(value, self._uut.data(index, role))

    def test_headerDataDisplayRoleNameSectionHorizontal(self) -> None:
        """
        The headerData method must return 'Name' when the called with the
        display role, the state name section and the horizontal orientation.
        """
        section = 0
        orientation = qtc.Qt.Orientation.Horizontal
        role = qtc.Qt.ItemDataRole.DisplayRole
        self.assertEqual('Name',
                         self._uut.headerData(section, orientation, role))

    def test_headerDataDisplayRoleValueSectionHorizontal(self) -> None:
        """
        The headerData method must return 'Value' when the called with the
        display role, the state value section and the horizontal orientation.
        """
        section = 1
        orientation = qtc.Qt.Orientation.Horizontal
        role = qtc.Qt.ItemDataRole.DisplayRole
        self.assertEqual('Value',
                         self._uut.headerData(section, orientation, role))

    def test_flagsReturnFlag(self) -> None:
        """
        The flags method must return the selectable, enabled and editable
        flags.
        """
        index = Mock()
        flags = qtc.Qt.ItemFlag.ItemIsSelectable | \
            qtc.Qt.ItemFlag.ItemIsEnabled | qtc.Qt.ItemFlag.ItemIsEditable
        self.assertEqual(flags, self._uut.flags(index))

    def test_setDataBadRole(self) -> None:
        """
        The setData method must return false if the role is not the edit role.
        """
        index = Mock()
        value = 'name'
        role = qtc.Qt.ItemDataRole.DisplayRole
        self.assertFalse(self._uut.setData(index, value, role))

    def test_setDataSaveName(self) -> None:
        """
        The setData method must save the new node name when the column is 0
        and return true whe the operation succeeds.
        """
        index = Mock()
        value = 'name'
        row = 2
        column = 0
        index.row.return_value = row
        index.column.return_value = column
        self.assertTrue(self._uut.setData(index, value))
        self._states[row].setName.assert_called_once_with(value)

    def test_setDataSaveValue(self) -> None:
        """
        The setData method must save the new node value when the column is 1
        and return true whe the operation succeeds.
        """
        index = Mock()
        value = 12
        row = 2
        column = 1
        index.column.return_value = column
        index.row.return_value = row
        self.assertTrue(self._uut.setData(index, value))
        self._states[row].setValue.assert_called_once_with(value)

    def test_insertRowInsertNewNode(self) -> None:
        """
        The insertRow method must insert a new node at the given row and
        return true when operation succeeds.
        """
        row = 2
        index = Mock()
        node = Mock()
        states = list(self._states)
        states.insert(row, node)
        with patch.object(StateListModel, 'beginInsertRows') as mockedBegin, \
                patch(self._IndexCls) as mockedIndexCls, \
                patch.object(StateListModel, 'endInsertRows') as mockedEnd, \
                patch(self._StateNodeCls) as mockedStateNode:
            mockedIndexCls.return_value = index
            mockedStateNode.return_value = node
            self.assertTrue(self._uut.insertRow(row, Mock()))
            mockedBegin.assert_called_once_with(index, row, row + 1)
            mockedStateNode.assert_called_once_with(f"STATE_{row}", row)
            mockedEnd.assert_called_once_with()
            self._uut.layoutChanged.emit.assert_called_once_with()
            self.assertEqual(len(states), len(self._uut._states))
            self.assertEqual(states, self._uut._states)

    def test_removeRowRowOutOfRange(self) -> None:
        """
        The removeRow method must return false if the row to remove is
        out of range.
        """
        rows = [-1, len(self._states)]
        parent = Mock()
        states = list(self._states)
        for row in rows:
            with patch.object(StateListModel, 'beginRemoveRows') \
                    as mockedBegin, \
                    patch.object(StateListModel, 'endRemoveRows') as mockedEnd:
                self.assertFalse(self._uut.removeRow(row, parent))
                mockedBegin.assert_not_called()
                mockedEnd.assert_not_called()
                self._uut.layoutChanged.emit.assert_not_called()
                self.assertEqual(len(states), len(self._uut._states))
                self.assertEqual(states, self._uut._states)

    def test_removeRowRemove(self) -> None:
        """
        The removeRow method must remove the given row and return true when
        the operation succeeds.
        """
        row = 2
        parent = Mock()
        states = list(self._states)
        states.pop(row)
        with patch.object(StateListModel, 'beginRemoveRows') as mockedBegin, \
                patch(self._IndexCls) as mockedIndexCls, \
                patch.object(StateListModel, 'endRemoveRows') as mockedEnd:
            mockedIndexCls.return_value = parent
            self.assertTrue(self._uut.removeRow(row, parent))
            mockedBegin.assert_called_once_with(parent, row, row + 1)
            mockedEnd.assert_called_once_with()
            self._uut.layoutChanged.emit.assert_called_once_with()
            self.assertEqual(len(states), len(self._uut._states))
            self.assertEqual(states, self._uut._states)

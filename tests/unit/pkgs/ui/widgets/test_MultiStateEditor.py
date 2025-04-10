from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.widgets import MultiStateEditor                    # noqa: E402


class TestMultiStateEditor(TestCase):
    """
    MultiStateEditor widget test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self._QWidget = 'pkgs.ui.widgets.multiStateEditor.qtw.QWidget.__init__'
        self._loggingMod = 'pkgs.ui.widgets.multiStateEditor.logging'
        self._StateListModelCls = 'pkgs.ui.widgets.multiStateEditor.' \
            'StateListModel'
        self._logger = Mock()
        self._multiState = Mock()
        with patch(self._loggingMod) as mockedLoggingMod, \
                patch(self._QWidget), \
                patch.object(MultiStateEditor, 'setupUi'), \
                patch.object(MultiStateEditor, '_initUi'):
            mockedLoggingMod.getLogger.return_value = self._logger
            self._uut = MultiStateEditor(self._multiState)
            self._uut.tvStateList = Mock()
            self._uut.cbDefaultState = Mock()
            self._uut.pbAddState = Mock()
            self._uut.pbDeleteState = Mock()

    def test_constructorGetLogger(self) -> None:
        """
        The constructor must get the button editor widget logger.
        """
        multiState = Mock()
        with patch(self._loggingMod) as mockedLoggingMod, \
                patch(self._QWidget), \
                patch.object(MultiStateEditor, 'setupUi'), \
                patch.object(MultiStateEditor, '_initUi'):
            MultiStateEditor(multiState)
            mockedLoggingMod.getLogger \
                .assert_called_once_with('app.windows.main.multiStateEditor')

    def test_constructorSetupUi(self) -> None:
        """
        The constructor must setup the UI.
        """
        multiState = Mock()
        with patch(self._loggingMod), patch(self._QWidget), \
                patch.object(MultiStateEditor, 'setupUi') as mockedSetupUi, \
                patch.object(MultiStateEditor, '_initUi'):
            uut = MultiStateEditor(multiState)
            mockedSetupUi.assert_called_once_with(uut)
            self.assertEqual(multiState, uut._multiState)

    def test_initUiInitAndConnect(self) -> None:
        """
        The _initUi method must initialize the state model, initialize the
        table view and the combo box and connect the button clicked signals.
        """
        states = Mock()
        defaultState = Mock()
        model = Mock()
        with patch(self._StateListModelCls) as mockedModel:
            mockedModel.return_value = model
            self._multiState.getStateList.return_value = states
            self._multiState.getDefaultIndex.return_value = defaultState
            self._uut._initUi()
            mockedModel.assert_called_once_with(states)
            self._uut.tvStateList.setModel.assert_called_once_with(model)
            self._uut.tvStateList.selectionModel().selectionChanged \
                .connect.assert_called_once_with(self._uut._newStateSelection)
            self._uut.cbDefaultState.setModel.assert_called_once_with(model)
            self._uut.cbDefaultState.setCurrentIndex \
                .assert_called_once_with(defaultState)
            self._uut.cbDefaultState.currentIndexChanged.connect \
                .assert_called_once_with(self._uut._selectNewDefault)
            self._uut.pbAddState.clicked.connect(self._uut._addState)
            self._uut.pbDeleteState.clicked.connect(self._uut._deleteState)

    def test_newStateSelectionEnableDeleteButton(self) -> None:
        """
        The _newStateSelection method must enable the delete state button.
        """
        self._uut._newStateSelection()
        self._uut.pbDeleteState.setEnabled.assert_called_once_with(True)

    def test_selectNewDefaultSaveNewDefaultIndex(self) -> None:
        """
        The _selectNewDefault method must save the new default index.
        """
        index = 6
        self._uut._selectNewDefault(index)
        self._multiState.setDefaultIndex.assert_called_once_with(index)

    def test_addStateAddWithNoSelection(self) -> None:
        """
        The _addState method must add a new state at the beginning of the list
        when no state is selected.
        """
        index = Mock()
        model = Mock()
        self._uut.tvStateList.model.return_value = model
        self._uut.tvStateList.currentIndex.return_value = index
        index.isValid.return_value = False
        self._uut._addState()
        model.insertRow.assert_called_once_with(0, index)

    def test_addStateAddWithSelection(self) -> None:
        """
        The _addState method must add a new state after the selected state when
        a state is selected.
        """
        row = 2
        index = Mock()
        model = Mock()
        self._uut.tvStateList.model.return_value = model
        self._uut.tvStateList.currentIndex.return_value = index
        index.isValid.return_value = True
        index.row.return_value = row
        self._uut._addState()
        model.insertRow.assert_called_once_with(row + 1, index)

    def test_deleteStateDelete(self) -> None:
        """
        The _deleteState method must delete the selected state..
        """
        row = 2
        index = Mock()
        model = Mock()
        self._uut.tvStateList.model.return_value = model
        self._uut.tvStateList.currentIndex.return_value = index
        index.isValid.return_value = True
        index.row.return_value = row
        self._uut._deleteState()
        model.removeRow.assert_called_once_with(row, index)

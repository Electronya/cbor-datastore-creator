from freezegun import freeze_time
from unittest import TestCase
from unittest.mock import call, Mock, patch

from PySide6.QtWidgets import QMessageBox

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.windows import AppWindow                       # noqa: E402
from pkgs.ui.models import NodeType                         # noqa: E402


class TestAppWindow(TestCase):
    """
    AppWindow test cases.
    """
    def setUp(self) -> None:
        self._QMainWindow = 'pkgs.ui.windows.appWindow.qtw.QMainWindow.' \
            '__init__'
        self._QMsgBoxCls = 'pkgs.ui.windows.appWindow.qtw.QMessageBox'
        self._DatastoreNodeCls = 'pkgs.ui.windows.appWindow.DatastoreNode'
        self._ObjectListNodeCls = 'pkgs.ui.windows.appWindow.ObjectListNode'
        self._DatastoreModelCls = 'pkgs.ui.windows.appWindow.DatastoreModel'
        self._ButtonEditorCls = 'pkgs.ui.windows.appWindow.ButtonEditor'
        self._FloatEditorCls = 'pkgs.ui.windows.appWindow.FloatEditor'
        self._IntEditorCls = 'pkgs.ui.windows.appWindow.IntEditor'
        self._loggingMod = 'pkgs.ui.windows.appWindow.logging'
        self._mockedLogger = Mock()
        with patch(self._loggingMod) as mockedLoggingMod, \
                patch(self._QMainWindow), patch.object(AppWindow, 'setupUi'), \
                patch.object(AppWindow, '_initUi'):
            mockedLoggingMod.getLogger.return_value = self._mockedLogger
            self._uut = AppWindow()
        self._setUpMockedWidgets()
        self._mockedLogger.reset_mock()

    def _setUpMockedWidgets(self):
        """
        Setup the mocked widgets.
        """
        self._uut._storeRoot = Mock()
        self._uut.actionNew = Mock()
        self._uut.pbAddObject = Mock()
        self._uut.tvObjectList = Mock()
        self._uut.pbDeleteObject = Mock()
        self._uut.vlEditor = Mock()

    def test_constructorGetLogger(self) -> None:
        """
        The constructor must get the main window logger.
        """
        with patch(self._loggingMod) as mockedLoggingMod, \
                patch(self._QMainWindow), patch.object(AppWindow, 'setupUi'), \
                patch.object(AppWindow, '_initUi'):
            AppWindow()
            mockedLoggingMod.getLogger \
                .assert_called_once_with('app.windows.main')

    def test_constructorSetupUi(self) -> None:
        """
        The constructor must setup the UI.
        """
        with patch(self._QMainWindow), \
                patch.object(AppWindow, 'setupUi') as mockedSetupUi, \
                patch.object(AppWindow, '_initUi'):
            testAppWindow = AppWindow()
            mockedSetupUi.assert_called_once_with(testAppWindow)

    def test_constructorInitUi(self) -> None:
        """
        The constructor must initialize the UI.
        """
        with patch(self._QMainWindow), \
                patch(self._QMainWindow), patch.object(AppWindow, 'setupUi'), \
                patch.object(AppWindow, '_initUi') as mockedInitUi:
            AppWindow()
            mockedInitUi.assert_called_once()

    def test_initUiConnectEventsAndSlotsCreateEditors(self) -> None:
        """
        The _initUi method must connect all the window events to there
        corresponding slots, and create and hide editors.
        """
        root = Mock()
        with patch(self._ObjectListNodeCls) as mockedObjectListNode:
            mockedObjectListNode.return_value = root
            self._uut._initUi()
            self.assertEqual(root, self._uut._storeRoot)
            self._uut.actionNew.triggered.connect \
                .assert_called_once_with(self._uut._createNewStore)
            self._uut.pbAddObject.clicked.connect \
                .assert_called_once_with(self._uut._createNewObject)
            self._uut.pbDeleteObject.clicked.connect \
                .assert_called_once_with(self._uut._deleteObject)

    def test_displayEditorButton(self) -> None:
        """
        The _displayEditor method must create the button editor when the
        selected node is a button object.
        """
        selected = Mock()
        type = NodeType.BUTTON
        objectEditor = Mock()
        with patch(self._ButtonEditorCls) as mockedEditorCls:
            selected.getType.return_value = type
            mockedEditorCls.return_value = objectEditor
            self._uut._displayEditor(selected)
            mockedEditorCls.assert_called_once_with(selected)
            self._uut.vlEditor.insertWidget \
                .assert_called_once_with(0, objectEditor)
            self.assertEqual(objectEditor, self._uut._objectEditor)

    def test_displayEditorFloat(self) -> None:
        """
        The _displayEditor method must create the float editor when the
        selected node is a float object.
        """
        selected = Mock()
        type = NodeType.FLOAT
        objectEditor = Mock()
        with patch(self._FloatEditorCls) as mockedEditorCls:
            selected.getType.return_value = type
            mockedEditorCls.return_value = objectEditor
            self._uut._displayEditor(selected)
            mockedEditorCls.assert_called_once_with(selected)
            self._uut.vlEditor.insertWidget \
                .assert_called_once_with(0, objectEditor)
            self.assertEqual(objectEditor, self._uut._objectEditor)

    def test_displayEditorInt(self) -> None:
        """
        The _displayEditor method must create the int editor when the
        selected node is a int object.
        """
        selected = Mock()
        type = NodeType.INT
        objectEditor = Mock()
        with patch(self._IntEditorCls) as mockedEditorCls:
            selected.getType.return_value = type
            mockedEditorCls.return_value = objectEditor
            self._uut._displayEditor(selected)
            mockedEditorCls.assert_called_once_with(selected)
            self._uut.vlEditor.insertWidget \
                .assert_called_once_with(0, objectEditor)
            self.assertEqual(objectEditor, self._uut._objectEditor)

    def test_hideEditorRemoveEditor(self) -> None:
        """
        The _hideEditor method must remove the object editor and the array
        editor when they are present.
        """
        editors = [{'object': None, 'array': None},
                   {'object': Mock(), 'array': None},
                   {'object': None, 'array': Mock()},
                   {'object': Mock(), 'array': Mock()}]
        calls = []
        for editor in editors:
            self._uut._objectEditor = editor['object']
            self._uut._arrayEditor = editor['array']
            self._uut._hideEditor()
            if editor['object'] is not None:
                calls.append(call(editor['object']))
                editor['object'].setParent.assert_called_once_with(None)
                editor['object'].deleteLater.assert_called_once_with()
                editor['object'].setParent.reset_mock()
                editor['object'].deleteLater.reset_mock()
            if editor['array'] is not None:
                calls.append(call(editor['array']))
                editor['array'].setParent.assert_called_once_with(None)
                editor['array'].deleteLater.assert_called_once_with()
                editor['array'].setParent.reset_mock()
                editor['array'].deleteLater.reset_mock()
            if editor['object'] is not None or editor['array'] is not None:
                self._uut.vlEditor.removeWidget.assert_has_calls(calls)
                self._uut.vlEditor.removeWidget.reset_mock()
                calls = []

    @freeze_time('Jan 14th, 2025')
    def test_createNewStoreCreateNewStore(self) -> None:
        """
        The _createNewStore method must create a new empty datastore and create
        the tree view model based on it.
        """
        datastoreNode = Mock()
        model = Mock()
        with patch(self._DatastoreNodeCls) as mockedDatastoreNode, \
                patch(self._DatastoreModelCls) as mockedDatastoreModel:
            mockedDatastoreNode.createNewStore.return_value = datastoreNode
            mockedDatastoreModel.return_value = model
            self._uut._createNewStore()
            self._mockedLogger.info \
                .assert_called_once_with('creating new datastore')
            mockedDatastoreNode.createNewStore \
                .assert_called_once_with(self._uut._storeRoot)
            mockedDatastoreModel.assert_called_once_with(self._uut._storeRoot)
            self._uut.tvObjectList.setModel.assert_called_once_with(model)
            self._uut.tvObjectList.selectionModel().selectionChanged.connect \
                .assert_called_once_with(self._uut._newStoreSelection)
            self._uut.tvObjectList.expandAll.assert_called_once_with()

    def test_newStoreSelectionStoreSelected(self) -> None:
        """
        The _newStoreSelection must disable the add new object and the delete
        object buttons when the selected node is the store.
        """
        selected = Mock()
        type = NodeType.STORE
        with patch.object(AppWindow, '_hideEditor') as mockedHideEditor, \
                patch.object(AppWindow, '_displayEditor') \
                as mockedDisplayEditor:
            self._uut.tvObjectList.currentIndex().internalPointer \
                .return_value = selected
            selected.getType.return_value = type
            self._uut._newStoreSelection()
            mockedHideEditor.assert_called_once_with()
            mockedDisplayEditor.assert_not_called()
            self._uut.pbAddObject.setEnabled.assert_called_once_with(False)
            self._uut.pbDeleteObject.setEnabled.assert_called_once_with(False)

    def test_newStoreSelectionListSelected(self) -> None:
        """
        The _newStoreSelection must enable the add new object and disable the
        delete object buttons when the selected node is an object list.
        """
        selected = Mock()
        type = NodeType.OBJ_LIST
        with patch.object(AppWindow, '_hideEditor') as mockedHideEditor, \
                patch.object(AppWindow, '_displayEditor') \
                as mockedDisplayEditor:
            self._uut.tvObjectList.currentIndex().internalPointer \
                .return_value = selected
            selected.getType.return_value = type
            self._uut._newStoreSelection()
            mockedHideEditor.assert_called_once_with()
            mockedDisplayEditor.assert_not_called()
            self._uut.pbAddObject.setEnabled.assert_called_once_with(True)
            self._uut.pbDeleteObject.setEnabled.assert_called_once_with(False)

    def test_newStoreSelectionObjectSelected(self) -> None:
        """
        The _newStoreSelection must enable the add new object and the
        delete object buttons when the selected node is an object.
        """
        selected = Mock()
        types = [NodeType.BUTTON, NodeType.BUTTON_ARRAY, NodeType.FLOAT,
                 NodeType.FLOAT_ARRAY, NodeType.INT, NodeType.INT_ARRAY,
                 NodeType.MULTI_STATE, NodeType.UINT, NodeType.UINT_ARRAY]
        for type in types:
            self._uut.tvObjectList.currentIndex().internalPointer \
                .return_value = selected
            selected.getType.return_value = type
            with patch.object(AppWindow, '_hideEditor') as mockedHideEditor, \
                    patch.object(AppWindow, '_displayEditor') \
                    as mockedDisplayEditor:
                self._uut._newStoreSelection()
                mockedHideEditor.assert_called_once_with()
                mockedDisplayEditor.assert_called_once_with(selected)
                self._uut.pbAddObject.setEnabled.assert_called_once_with(True)
                self._uut.pbDeleteObject.setEnabled \
                    .assert_called_once_with(True)
                mockedHideEditor.reset_mock()
                mockedDisplayEditor.reset_mock()
                self._uut.pbAddObject.setEnabled.reset_mock()
                self._uut.pbDeleteObject.setEnabled.reset_mock()

    def test_createNewObjectNewObjectInList(self) -> None:
        """
        The _createNewObject method must get the selected node of the store,
        gets its type and insert a new object at the end of the list if the
        selected node is an object list.
        """
        row = 3
        model = Mock()
        selected = Mock()
        node = Mock()
        self._uut.tvObjectList.model.return_value = model
        self._uut.tvObjectList.currentIndex.return_value = selected
        selected.internalPointer.return_value = node
        node.getType.return_value = NodeType.OBJ_LIST
        node.getChildCount.return_value = row
        self._uut._createNewObject()
        model.insertRow.assert_called_once_with(row, selected)

    def test_createNewObjectNewObjectAfterSelected(self) -> None:
        """
        The _createNewObject method must get the selected node of the store,
        gets its type and insert a new object after it if the selected node is
        an object.
        """
        types = [NodeType.BUTTON, NodeType.BUTTON_ARRAY, NodeType.FLOAT,
                 NodeType.FLOAT_ARRAY, NodeType.INT, NodeType.INT_ARRAY,
                 NodeType.MULTI_STATE, NodeType.UINT, NodeType.UINT_ARRAY]
        row = 3
        model = Mock()
        selected = Mock()
        node = Mock()
        parent = Mock()
        for type in types:
            self._uut.tvObjectList.model.return_value = model
            self._uut.tvObjectList.currentIndex.return_value = selected
            selected.internalPointer.return_value = node
            node.getType.return_value = type
            selected.row.return_value = row
            model.parent.return_value = parent
            self._uut._createNewObject()
            model.parent.assert_called_once_with(selected)
            model.insertRow.assert_called_once_with(row + 1, parent)
            model.parent.reset_mock()
            model.insertRow.reset_mock()

    def test_deleteObjectDeleteSelected(self) -> None:
        """
        The _deleteObject method must get the selected node get its parent and
        row, and delete the selected node when it's an object.
        """
        types = [NodeType.BUTTON, NodeType.BUTTON_ARRAY, NodeType.FLOAT,
                 NodeType.FLOAT_ARRAY, NodeType.INT, NodeType.INT_ARRAY,
                 NodeType.MULTI_STATE, NodeType.UINT, NodeType.UINT_ARRAY]
        row = 3
        model = Mock()
        selected = Mock()
        node = Mock()
        parent = Mock()
        for type in types:
            self._uut.tvObjectList.model.return_value = model
            self._uut.tvObjectList.currentIndex.return_value = selected
            selected.internalPointer.return_value = node
            node.getType.return_value = type
            selected.row.return_value = row
            model.parent.return_value = parent
            self._uut._deleteObject()
            model.parent.assert_called_once_with(selected)
            model.removeRow.assert_called_once_with(row, parent)
            model.parent.reset_mock()
            model.removeRow.reset_mock()

    def test_createErrorMsgBoxNewMsgBox(self) -> None:
        """
        The _createErrorMsgBox method must create the new message box.
        """
        mockedMsgBox = Mock()
        testLvl = QMessageBox.Warning
        testException = Exception('test error')
        with patch(self._QMsgBoxCls) as mockedMsgBoxCls:
            mockedMsgBoxCls.return_value = mockedMsgBox
            self._uut._createErrorMsgBox(testLvl, testException)
            mockedMsgBoxCls.assert_called_once_with(self._uut)
            mockedMsgBox.setWindowTitle.assert_called_once_with('Error!!')
            mockedMsgBox.setText.assert_called_once_with(str(testException))
            mockedMsgBox.setIcon.assert_called_once_with(testLvl)

    def test_createErrorMsgBoxCriticalQuit(self) -> None:
        """
        The _createErrorMsgBox method must connect the button clicked signal
        to the application quit slot when the level is critical.
        """
        mockedMsgBox = Mock()
        testException = Exception('test error')
        with patch(self._QMsgBoxCls) as mockedMsgBoxCls:
            mockedMsgBoxCls.return_value = mockedMsgBox
            testLvls = [mockedMsgBoxCls.Warning, mockedMsgBoxCls.Critical]
            for testLvl in testLvls:
                self._uut._createErrorMsgBox(testLvl, testException)
            mockedMsgBox.buttonClicked.connect.assert_called_once()

    def test_createErrorMsgBoxExec(self) -> None:
        """
        The _createErrorMsgBox method must execute the created message box.
        """
        mockedMsgBox = Mock()
        testLvl = QMessageBox.Warning
        testException = Exception('test error')
        with patch(self._QMsgBoxCls) as mockedMsgBoxCls:
            mockedMsgBoxCls.return_value = mockedMsgBox
            self._uut._createErrorMsgBox(testLvl, testException)
            mockedMsgBox.exec_.assert_called_once()

import logging
import sys

import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw

from .appWindow_ui import Ui_appWindow
from ..models import DatastoreModel, DatastoreNode, NodeType, ObjectListNode


class AppWindow(qtw.QMainWindow, Ui_appWindow):
    """
    The application main window.
    """
    def __init__(self) -> None:
        """
        Constructor.
        """
        super(AppWindow, self).__init__()
        self._logger = logging.getLogger('app.windows.main')
        self._logger.info('loading UI...')
        self._storeRoot = None
        self.setupUi(self)
        self._initUi()

    def _initUi(self) -> None:
        """
        Initialize the UI models and events.
        """
        self._storeRoot = ObjectListNode('', None)
        self.actionNew.triggered.connect(self._createNewStore)
        self.pbAddObject.clicked.connect(self._createNewObject)

    @qtc.Slot()
    def _createNewStore(self) -> None:
        """
        Create a new datastore.
        """
        self._logger.info('creating new datastore')
        DatastoreNode.createNewStore(self._storeRoot)
        model = DatastoreModel(self._storeRoot)
        self.tvObjectList.setModel(model)
        self.tvObjectList.expandAll()

    @qtc.Slot()
    def _createNewObject(self) -> None:
        """
        Create a new object in the datastore.
        """
        model = self.tvObjectList.model()
        selected = self.tvObjectList.currentIndex()
        selectedNode = selected.internalPointer()
        selectedType = selectedNode.getType()
        if selectedType == NodeType.OBJ_LIST:
            self._logger.info(f"creating a new {selectedType.name}")
            model.insertRow(selectedNode.getChildCount(), selected)
        elif selectedType != NodeType.STORE:
            parent = model.parent(selected)
            parentType = parent.internalPointer().getType()
            self._logger.info(f"creating a new {parentType.name}")
            model.insertRow(selected.row() + 1, parent)

    @qtc.Slot(qtw.QMessageBox.Icon, Exception)
    def _createErrorMsgBox(self, lvl: qtw.QMessageBox.Icon,
                           error: Exception) -> None:
        """
        Create a error message box.
        """
        self._logger.error(f"error: {str(error)}")
        msgBox = qtw.QMessageBox(self)
        msgBox.setWindowTitle('Error!!')
        msgBox.setText(str(error))
        msgBox.setIcon(lvl)
        if lvl == qtw.QMessageBox.Critical:
            self._logger.debug('connecting to button clicked for critical')
            msgBox.buttonClicked.connect(lambda i: sys.exit(1))
        msgBox.exec_()

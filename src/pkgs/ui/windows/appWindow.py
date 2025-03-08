import logging
import sys

import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw

from .appWindow_ui import Ui_appWindow
# from ..models import DatastoreModel, DatastoreNode, DatastoreNodeType
# from ...datastore import Datastore, DatastoreData


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
        self.setupUi(self)
        self._initUi()

    def _initUi(self) -> None:
        """
        Initialize the UI models.
        """
        self.actionNew.triggered.connect(self._createNewStore)

    @qtc.Slot()
    def _createNewStore(self) -> None:
        """
        Create a new datastore.
        """
        # self._logger.info('creating new datastore')
        # data = DatastoreData('datastore',
        #                      qtc.QDate.currentDate().toString('yyyy-mm-dd'))
        # self._datastore = Datastore(data)
        # root = DatastoreNode(DatastoreNodeType.OBJ_LIST, name='')
        # store = DatastoreNode(DatastoreNodeType.STORE,
        #                       metaData=self._datastore, parent=root)
        # DatastoreNode(DatastoreNodeType.OBJ_LIST, name='Buttons', parent=store)
        # DatastoreNode(DatastoreNodeType.OBJ_LIST,
        #               name='Button Arrays', parent=store)
        # DatastoreNode(DatastoreNodeType.OBJ_LIST, name='Floats', parent=store)
        # DatastoreNode(DatastoreNodeType.OBJ_LIST,
        #               name='Float Arrays', parent=store)
        # DatastoreNode(DatastoreNodeType.OBJ_LIST,
        #               name='Multi-States', parent=store)
        # DatastoreNode(DatastoreNodeType.OBJ_LIST,
        #               name='Signed Integers', parent=store)
        # DatastoreNode(DatastoreNodeType.OBJ_LIST,
        #               name='Signed Integer Arrays', parent=store)
        # DatastoreNode(DatastoreNodeType.OBJ_LIST,
        #               name='Unsigned Integers', parent=store)
        # DatastoreNode(DatastoreNodeType.OBJ_LIST,
        #               name='Unsigned Integer Arrays', parent=store)
        # model = DatastoreModel(root)
        # self.tvObjectList.setModel(model)
        # self.tvObjectList.expandAll()

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

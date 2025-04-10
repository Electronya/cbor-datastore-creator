import logging

import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw

from .multiStateEditor_ui import Ui_MultiStateEditor
from ..models import MultiStateNode, StateListModel


class MultiStateEditor(qtw.QWidget, Ui_MultiStateEditor):
    """
    The button editor widget.
    """
    def __init__(self, multiState: MultiStateNode,
                 parent: qtw.QWidget = None) -> None:
        """
        Constructor.
        """
        super(MultiStateEditor, self).__init__(parent)
        self._logger = logging.getLogger('app.windows.main.multiStateEditor')
        self._logger.info('creating int editor widget')
        self._multiState = multiState
        self.setupUi(self)
        self._initUi()

    def _initUi(self) -> None:
        """
        Initialize the UI connecting signals and slots.
        """
        model = StateListModel(self._multiState.getStateList())
        self.tvStateList.setModel(model)
        self.tvStateList.selectionModel().selectionChanged \
            .connect(self._newStateSelection)
        self.cbDefaultState.setModel(model)
        self.cbDefaultState.setCurrentIndex(self._multiState.getDefaultIndex())
        self.cbDefaultState.currentIndexChanged.connect(self._selectNewDefault)
        self.pbAddState.clicked.connect(self._addState)
        self.pbDeleteState.clicked.connect(self._deleteState)

    @qtc.Slot()
    def _newStateSelection(self) -> None:
        """
        Manage add and delete button enable state.
        """
        self.pbDeleteState.setEnabled(True)

    @qtc.Slot()
    def _selectNewDefault(self, default: int) -> None:
        """
        Select a new default state.

        Param
            default: The new default index.
        """
        self._multiState.setDefaultIndex(default)

    @qtc.Slot()
    def _addState(self) -> None:
        """
        Add a new state.
        """
        model = self.tvStateList.model()
        index = self.tvStateList.currentIndex()
        if index.isValid():
            model.insertRow(index.row() + 1, index)
        else:
            model.insertRow(0, index)

    @qtc.Slot()
    def _deleteState(self) -> None:
        """
        Delete the selected state.
        """

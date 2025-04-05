import logging

import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw

from .multiStateEditor_ui import Ui_MultiStateEditor
from ..models import MultiStateNode


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

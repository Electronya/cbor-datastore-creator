import logging

import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw

from .buttonEditor_ui import Ui_ButtonEditor
from ..models import ButtonNode


class ButtonEditor(qtw.QWidget, Ui_ButtonEditor):
    """
    The button editor widget.
    """
    def __init__(self, button: ButtonNode, parent: qtw.QWidget = None) -> None:
        """
        Constructor.
        """
        super(ButtonEditor, self).__init__(parent)
        self._logger = logging.getLogger('app.windows.main.buttonEditor')
        self._logger.info('creating button editor widget')
        self._button = button
        self.setupUi(self)
        self._initUi()

    def _initUi(self) -> None:
        """
        Initialize the UI.
        """
        self.spLongPressTime.setValue(self._button.getLongPressTime())
        self.spInactiveTime.setValue(self._button.getInactiveTime())

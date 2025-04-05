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
        self.sbLongPressTime.setValue(self._button.getLongPressTime())
        self.sbLongPressTime.valueChanged.connect(self._saveLongPressTime)
        self.sbInactiveTime.setValue(self._button.getInactiveTime())
        self.sbInactiveTime.valueChanged.connect(self._saveInactiveTime)

    @qtc.Slot()
    def _saveLongPressTime(self, longPressTime: int) -> None:
        """
        Save the long press time.

        Param
            longPressTime: The long press time to save.
        """
        self._logger.info(f"{self._button.getName()} save new long press time "
                          f"{longPressTime}")
        self._button.setLongPressTime(longPressTime)

    @qtc.Slot()
    def _saveInactiveTime(self, inactiveTime: int) -> None:
        """
        Save the inactive time.

        Param
            inactiveTime: The inactive time to save.
        """
        self._logger.info(f"{self._button.getName()} save new inactive time "
                          f"{inactiveTime}")
        self._button.setInactiveTime(inactiveTime)

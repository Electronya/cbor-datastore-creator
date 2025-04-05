import logging

import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw

from .intEditor_ui import Ui_IntEditor
from ..models import UintNode


class UintEditor(qtw.QWidget, Ui_IntEditor):
    """
    The button editor widget.
    """
    def __init__(self, uint: UintNode, parent: qtw.QWidget = None) -> None:
        """
        Constructor.
        """
        super(UintEditor, self).__init__(parent)
        self._logger = logging.getLogger('app.windows.main.uintEditor')
        self._logger.info('creating int editor widget')
        self._uint = uint
        self.setupUi(self)
        self._initUi()

    def _initUi(self) -> None:
        """
        Initialize the UI connecting signals and slots.
        """
        min = self._uint.getMinimum()
        max = self._uint.getMaximum()
        default = self._uint.getDefault()
        self.sbDefaultValue.setMinimum(min)
        self.sbDefaultValue.setMaximum(max)
        self.sbDefaultValue.setValue(default)
        self.sbDefaultValue.setKeyboardTracking(False)
        self.sbDefaultValue.valueChanged.connect(self._saveDefaultValue)
        self.sbMinValue.setMinimum(0)
        self.sbMinValue.setMaximum(max - 1.0)
        self.sbMinValue.setValue(min)
        self.sbMinValue.setKeyboardTracking(False)
        self.sbMinValue.valueChanged.connect(self._saveMinValue)
        self.sbMaxValue.setMinimum(min + 1.0)
        self.sbMaxValue.setMaximum(2 ** 31 - 1)
        self.sbMaxValue.setValue(max)
        self.sbMaxValue.setKeyboardTracking(False)
        self.sbMaxValue.valueChanged.connect(self._saveMaxValue)

    @qtc.Slot()
    def _saveDefaultValue(self, default: int) -> None:
        """
        Save the new default value.

        Param
            default: The new default value.
        """
        self._uint.setDefault(default)

    @qtc.Slot()
    def _saveMinValue(self, min: int) -> None:
        """
        Save the new minimum value.

        Param
            min: The new minimum value.
        """
        self._uint.setMinimum(min)
        self.sbDefaultValue.setMinimum(min)
        self.sbMaxValue.setMinimum(min + 1)

    @qtc.Slot()
    def _saveMaxValue(self, max: int) -> None:
        """
        Save the new maximum value.

        Param
            max: The new maximum value.
        """
        self._uint.setMaximum(max)
        self.sbDefaultValue.setMaximum(max)
        self.sbMinValue.setMaximum(max - 1)

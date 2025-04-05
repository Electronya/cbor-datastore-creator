import logging
import sys

import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw

from .floatEditor_ui import Ui_FloatEditor
from ..models import FloatNode


class FloatEditor(qtw.QWidget, Ui_FloatEditor):
    """
    The float object editor widget.
    """
    def __init__(self, floatObj: FloatNode,
                 parent: qtw.QWidget = None) -> None:
        """
        Constructor.
        """
        super(FloatEditor, self).__init__(parent)
        self._logger = logging.getLogger('app.windows.main.floatEditor')
        self._logger.info('creating float editor widget')
        self._float = floatObj
        self.setupUi(self)
        self._initUi()

    def _initUi(self) -> None:
        """
        Initialize the UI connecting signals and slots.
        """
        min = self._float.getMinimum()
        max = self._float.getMaximum()
        default = self._float.getDefault()
        self.dsbDefaultValue.setValue(default)
        self.dsbDefaultValue.setMinimum(min)
        self.dsbDefaultValue.setMaximum(max)
        self.dsbDefaultValue.setKeyboardTracking(False)
        self.dsbDefaultValue.valueChanged.connect(self._saveDefaultValue)
        self.dsbMinValue.setValue(min)
        self.dsbMinValue.setMinimum(-sys.float_info.max)
        self.dsbMinValue.setMaximum(max - 1.0)
        self.dsbMinValue.setKeyboardTracking(False)
        self.dsbMinValue.valueChanged.connect(self._saveMinValue)
        self.dsbMaxValue.setValue(max)
        self.dsbMaxValue.setMinimum(min + 1.0)
        self.dsbMaxValue.setMaximum(sys.float_info.max)
        self.dsbMaxValue.setKeyboardTracking(False)
        self.dsbMaxValue.valueChanged.connect(self._saveMaxValue)

    @qtc.Slot()
    def _saveDefaultValue(self, default: float) -> None:
        """
        Save the new default value.

        Param
            default: The new default value.
        """
        self._float.setDefault(default)

    @qtc.Slot()
    def _saveMinValue(self, min: float) -> None:
        """
        Save the new minimum value.

        Param
            min: The new minimum value.
        """
        self._float.setMinimum(min)
        self.dsbDefaultValue.setMinimum(min)
        self.dsbMaxValue.setMinimum(min + 1.0)

    @qtc.Slot()
    def _saveMaxValue(self, max: float) -> None:
        """
        Save the new maximum value.

        Param
            max: The new maximum value.
        """
        self._float.setMaximum(max)
        self.dsbDefaultValue.setMaximum(max)
        self.dsbMinValue.setMaximum(max - 1.0)

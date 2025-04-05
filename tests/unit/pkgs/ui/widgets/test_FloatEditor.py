from unittest import TestCase
from unittest.mock import Mock, patch

from PySide6.QtWidgets import QMessageBox

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.widgets import FloatEditor                         # noqa: E402


class TestFloatEditor(TestCase):
    """
    floatEditor widget test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self._QWidget = 'pkgs.ui.widgets.floatEditor.qtw.QWidget.__init__'
        self._loggingMod = 'pkgs.ui.widgets.floatEditor.logging'
        self._logger = Mock()
        self._float = Mock()
        with patch(self._loggingMod) as mockedLoggingMod, \
                patch(self._QWidget), patch.object(FloatEditor, 'setupUi'), \
                patch.object(FloatEditor, '_initUi'):
            mockedLoggingMod.getLogger.return_value = self._logger
            self._uut = FloatEditor(self._float)
            self._uut.dsbDefaultValue = Mock()
            self._uut.dsbMinValue = Mock()
            self._uut.dsbMaxValue = Mock()

    def test_constructorGetLogger(self) -> None:
        """
        The constructor must get the button editor widget logger.
        """
        floatObj = Mock()
        with patch(self._loggingMod) as mockedLoggingMod, \
                patch(self._QWidget), patch.object(FloatEditor, 'setupUi'), \
                patch.object(FloatEditor, '_initUi'):
            FloatEditor(floatObj)
            mockedLoggingMod.getLogger \
                .assert_called_once_with('app.windows.main.floatEditor')

    def test_constructorSetupUi(self) -> None:
        """
        The constructor must setup the UI.
        """
        floatObj = Mock()
        with patch(self._loggingMod), patch(self._QWidget), \
                patch.object(FloatEditor, 'setupUi') as mockedSetupUi, \
                patch.object(FloatEditor, '_initUi'):
            uut = FloatEditor(floatObj)
            mockedSetupUi.assert_called_once_with(uut)
            self.assertEqual(floatObj, uut._float)

    def test_constructorInitUi(self) -> None:
        """
        The constructor must initialize the UI.
        """
        floatObj = Mock()
        with patch(self._loggingMod), patch(self._QWidget), \
                patch.object(FloatEditor, 'setupUi'), \
                patch.object(FloatEditor, '_initUi') as mockedInitUi:
            FloatEditor(floatObj)
            mockedInitUi.assert_called_once_with()

    def test_initUiInitInput(self) -> None:
        """
        The _initUi method must initialize the input value from the float
        data.
        """
        minValue = -1.0
        maxValue = 10.0
        defaultValue = 1.0
        self._float.getMinimum.return_value = minValue
        self._float.getMaximum.return_value = maxValue
        self._float.getDefault.return_value = defaultValue
        self._uut._initUi()
        self._uut.dsbDefaultValue.setValue \
            .assert_called_once_with(defaultValue)
        self._uut.dsbDefaultValue.setMinimum.assert_called_once_with(minValue)
        self._uut.dsbDefaultValue.setMaximum.assert_called_once_with(maxValue)
        self._uut.dsbDefaultValue.setKeyboardTracking \
            .assert_called_once_with(False)
        self._uut.dsbDefaultValue.valueChanged.connect \
            .assert_called_once_with(self._uut._saveDefaultValue)
        self._uut.dsbMinValue.setValue.assert_called_once_with(minValue)
        self._uut.dsbMinValue.setMinimum \
            .assert_called_once_with(-sys.float_info.max)
        self._uut.dsbMinValue.setMaximum \
            .assert_called_once_with(maxValue - 1.0)
        self._uut.dsbMinValue.setKeyboardTracking \
            .assert_called_once_with(False)
        self._uut.dsbMinValue.valueChanged.connect \
            .assert_called_once_with(self._uut._saveMinValue)
        self._uut.dsbMaxValue.setValue.assert_called_once_with(maxValue)
        self._uut.dsbMaxValue.setMinimum \
            .assert_called_once_with(minValue + 1.0)
        self._uut.dsbMaxValue.setMaximum \
            .assert_called_once_with(sys.float_info.max)
        self._uut.dsbMaxValue.setKeyboardTracking \
            .assert_called_once_with(False)
        self._uut.dsbMaxValue.valueChanged.connect \
            .assert_called_once_with(self._uut._saveMaxValue)

    def test_saveDefaultValueSaveDefault(self) -> None:
        """
        The _saveDefaultValue method must save the new default value.
        """
        default = 12.0
        self._uut._saveDefaultValue(default)
        self._uut._float.setDefault.assert_called_once_with(default)

    def test_saveMinValueSaveMin(self) -> None:
        """
        The _saveMinValue method must save the new minimum, update the default
        minimum value and update the maximum input field minimum value with it
        plus 1.
        """
        min = -12.0
        self._uut._saveMinValue(min)
        self._uut._float.setMinimum.assert_called_once_with(min)
        self._uut.dsbDefaultValue.setMinimum.assert_called_once_with(min)
        self._uut.dsbMaxValue.setMinimum.assert_called_once_with(min + 1.0)

    def test_saveMaxValueSaveMax(self) -> None:
        """
        The _saveMaxValue method must save the new maximum, update the default
        maximum value and update the maximum input field maximum value with it
        minus 1.
        """
        max = 12.0
        self._uut._saveMaxValue(max)
        self._uut._float.setMaximum.assert_called_once_with(max)
        self._uut.dsbDefaultValue.setMaximum.assert_called_once_with(max)
        self._uut.dsbMinValue.setMaximum.assert_called_once_with(max - 1.0)

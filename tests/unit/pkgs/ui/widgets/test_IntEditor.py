from unittest import TestCase
from unittest.mock import Mock, patch

from PySide6.QtWidgets import QMessageBox

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.widgets import IntEditor                         # noqa: E402


class TestIntEditor(TestCase):
    """
    IntEditor widget test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self._QWidget = 'pkgs.ui.widgets.intEditor.qtw.QWidget.__init__'
        self._loggingMod = 'pkgs.ui.widgets.intEditor.logging'
        self._logger = Mock()
        self._int = Mock()
        with patch(self._loggingMod) as mockedLoggingMod, \
                patch(self._QWidget), patch.object(IntEditor, 'setupUi'), \
                patch.object(IntEditor, '_initUi'):
            mockedLoggingMod.getLogger.return_value = self._logger
            self._uut = IntEditor(self._int)
            self._uut.sbDefaultValue = Mock()
            self._uut.sbMinValue = Mock()
            self._uut.sbMaxValue = Mock()

    def test_constructorGetLogger(self) -> None:
        """
        The constructor must get the button editor widget logger.
        """
        floatObj = Mock()
        with patch(self._loggingMod) as mockedLoggingMod, \
                patch(self._QWidget), patch.object(IntEditor, 'setupUi'), \
                patch.object(IntEditor, '_initUi'):
            IntEditor(floatObj)
            mockedLoggingMod.getLogger \
                .assert_called_once_with('app.windows.main.intEditor')

    def test_constructorSetupUi(self) -> None:
        """
        The constructor must setup the UI.
        """
        floatObj = Mock()
        with patch(self._loggingMod), patch(self._QWidget), \
                patch.object(IntEditor, 'setupUi') as mockedSetupUi, \
                patch.object(IntEditor, '_initUi'):
            uut = IntEditor(floatObj)
            mockedSetupUi.assert_called_once_with(uut)
            self.assertEqual(floatObj, uut._int)

    def test_initUiInitInput(self) -> None:
        """
        The _initUi method must initialize the input value from the float
        data.
        """
        minValue = -1
        maxValue = 10
        defaultValue = 1
        self._int.getMinimum.return_value = minValue
        self._int.getMaximum.return_value = maxValue
        self._int.getDefault.return_value = defaultValue
        self._uut._initUi()
        self._uut.sbDefaultValue.setValue \
            .assert_called_once_with(defaultValue)
        self._uut.sbDefaultValue.setMinimum.assert_called_once_with(minValue)
        self._uut.sbDefaultValue.setMaximum.assert_called_once_with(maxValue)
        self._uut.sbDefaultValue.setKeyboardTracking \
            .assert_called_once_with(False)
        self._uut.sbDefaultValue.valueChanged.connect \
            .assert_called_once_with(self._uut._saveDefaultValue)
        self._uut.sbMinValue.setValue.assert_called_once_with(minValue)
        self._uut.sbMinValue.setMinimum \
            .assert_called_once_with(-(2 ** 31) + 1)
        self._uut.sbMinValue.setMaximum \
            .assert_called_once_with(maxValue - 1)
        self._uut.sbMinValue.setKeyboardTracking \
            .assert_called_once_with(False)
        self._uut.sbMinValue.valueChanged.connect \
            .assert_called_once_with(self._uut._saveMinValue)
        self._uut.sbMaxValue.setValue.assert_called_once_with(maxValue)
        self._uut.sbMaxValue.setMinimum \
            .assert_called_once_with(minValue + 1)
        self._uut.sbMaxValue.setMaximum \
            .assert_called_once_with(2 ** 31 - 1)
        self._uut.sbMaxValue.setKeyboardTracking \
            .assert_called_once_with(False)
        self._uut.sbMaxValue.valueChanged.connect \
            .assert_called_once_with(self._uut._saveMaxValue)

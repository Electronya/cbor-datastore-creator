from unittest import TestCase
from unittest.mock import Mock, patch

from PySide6.QtWidgets import QMessageBox

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.widgets import ButtonEditor                        # noqa: E402


class TestButtonEditor(TestCase):
    """
    ButtonEditor widget test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self._QWidget = 'pkgs.ui.widgets.buttonEditor.qtw.QWidget.__init__'
        self._loggingMod = 'pkgs.ui.widgets.buttonEditor.logging'
        self._logger = Mock()
        self._button = Mock()
        with patch(self._loggingMod) as mockedLoggingMod, \
                patch(self._QWidget), patch.object(ButtonEditor, 'setupUi'), \
                patch.object(ButtonEditor, '_initUi'):
            mockedLoggingMod.getLogger.return_value = self._logger
            self._uut = ButtonEditor(self._button)
            self._uut.sbLongPressTime = Mock()
            self._uut.sbInactiveTime = Mock()

    def test_constructorGetLogger(self) -> None:
        """
        The constructor must get the button editor widget logger.
        """
        button = Mock()
        with patch(self._loggingMod) as mockedLoggingMod, \
                patch(self._QWidget), patch.object(ButtonEditor, 'setupUi'), \
                patch.object(ButtonEditor, '_initUi'):
            ButtonEditor(button)
            mockedLoggingMod.getLogger \
                .assert_called_once_with('app.windows.main.buttonEditor')

    def test_constructorSetupUi(self) -> None:
        """
        The constructor must setup the UI.
        """
        button = Mock()
        with patch(self._loggingMod), patch(self._QWidget), \
                patch.object(ButtonEditor, 'setupUi') as mockedSetupUi, \
                patch.object(ButtonEditor, '_initUi'):
            uut = ButtonEditor(button)
            mockedSetupUi.assert_called_once_with(uut)
            self.assertEqual(button, uut._button)

    def test_constructorInitUi(self) -> None:
        """
        The constructor must initialize the UI.
        """
        button = Mock()
        with patch(self._loggingMod), patch(self._QWidget), \
                patch.object(ButtonEditor, 'setupUi'), \
                patch.object(ButtonEditor, '_initUi') as mockedInitUi:
            ButtonEditor(button)
            mockedInitUi.assert_called_once_with()

    def test_initUiInitInput(self) -> None:
        """
        The _initUi method must initialize the button setting inputs
        with the button current value.
        """
        longPressTime = 3000
        inactiveTime = 6000
        self._button.getLongPressTime.return_value = longPressTime
        self._button.getInactiveTime.return_value = inactiveTime
        self._uut._initUi()
        self._uut.sbLongPressTime.setValue \
            .assert_called_once_with(longPressTime)
        self._uut.sbLongPressTime.valueChanged \
            .connect.assert_called_once_with(self._uut._saveLongPressTime)
        self._uut.sbInactiveTime.setValue.assert_called_once_with(inactiveTime)
        self._uut.sbInactiveTime.valueChanged \
            .connect.assert_called_once_with(self._uut._saveInactiveTime)

    def test_saveLongPressTimeSaveNewTime(self) -> None:
        """
        The _saveLongPressTime method must save the new long press time.
        """
        longPressTime = 6000
        self._uut._saveLongPressTime(longPressTime)
        self._button.setLongPressTime.assert_called_once_with(longPressTime)

    def test_saveInactiveTimeSaveNewTime(self) -> None:
        """
        The _saveInactiveTime method must save the new inactive time.
        """
        inactiveTime = 8000
        self._uut._saveInactiveTime(inactiveTime)
        self._button.setInactiveTime.assert_called_once_with(inactiveTime)

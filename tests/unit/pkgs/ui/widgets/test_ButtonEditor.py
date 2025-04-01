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
            self._uut = ButtonEditor(self._button, Mock())
            self._uut.spLongPressTime = Mock()
            self._uut.spInactiveTime = Mock()

    def test_constructorGetLogger(self) -> None:
        """
        The constructor must get the button editor widget logger.
        """
        button = Mock()
        parent = Mock()
        with patch(self._loggingMod) as mockedLoggingMod, \
                patch(self._QWidget), patch.object(ButtonEditor, 'setupUi'), \
                patch.object(ButtonEditor, '_initUi'):
            ButtonEditor(button, parent)
            mockedLoggingMod.getLogger \
                .assert_called_once_with('app.windows.main.buttonEditor')

    def test_constructorSetupUi(self) -> None:
        """
        The constructor must setup the UI.
        """
        button = Mock()
        parent = Mock()
        with patch(self._loggingMod), patch(self._QWidget), \
                patch.object(ButtonEditor, 'setupUi') as mockedSetupUi, \
                patch.object(ButtonEditor, '_initUi'):
            uut = ButtonEditor(button, parent)
            mockedSetupUi.assert_called_once_with(uut)

    def test_constructorInitUi(self) -> None:
        """
        The constructor must initialize the UI.
        """
        button = Mock()
        parent = Mock()
        with patch(self._loggingMod), patch(self._QWidget), \
                patch.object(ButtonEditor, 'setupUi'), \
                patch.object(ButtonEditor, '_initUi') as mockedInitUi:
            ButtonEditor(button, parent)
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
        self._uut.spLongPressTime.setValue \
            .assert_called_once_with(longPressTime)
        self._uut.spInactiveTime.setValue.assert_called_once_with(inactiveTime)

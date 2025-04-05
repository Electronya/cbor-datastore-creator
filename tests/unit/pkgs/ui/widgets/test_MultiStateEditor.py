from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.widgets import MultiStateEditor                    # noqa: E402


class TestMultiStateEditor(TestCase):
    """
    MultiStateEditor widget test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self._QWidget = 'pkgs.ui.widgets.multiStateEditor.qtw.QWidget.__init__'
        self._loggingMod = 'pkgs.ui.widgets.multiStateEditor.logging'
        self._logger = Mock()
        self._multiState = Mock()
        with patch(self._loggingMod) as mockedLoggingMod, \
                patch(self._QWidget), \
                patch.object(MultiStateEditor, 'setupUi'), \
                patch.object(MultiStateEditor, '_initUi'):
            mockedLoggingMod.getLogger.return_value = self._logger
            self._uut = MultiStateEditor(self._multiState)

    def test_constructorGetLogger(self) -> None:
        """
        The constructor must get the button editor widget logger.
        """
        multiState = Mock()
        with patch(self._loggingMod) as mockedLoggingMod, \
                patch(self._QWidget), \
                patch.object(MultiStateEditor, 'setupUi'), \
                patch.object(MultiStateEditor, '_initUi'):
            MultiStateEditor(multiState)
            mockedLoggingMod.getLogger \
                .assert_called_once_with('app.windows.main.multiStateEditor')

    def test_constructorSetupUi(self) -> None:
        """
        The constructor must setup the UI.
        """
        multiState = Mock()
        with patch(self._loggingMod), patch(self._QWidget), \
                patch.object(MultiStateEditor, 'setupUi') as mockedSetupUi, \
                patch.object(MultiStateEditor, '_initUi'):
            uut = MultiStateEditor(multiState)
            mockedSetupUi.assert_called_once_with(uut)
            self.assertEqual(multiState, uut._multiState)

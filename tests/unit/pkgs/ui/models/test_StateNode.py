from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.models import StateNode                            # noqa: E402


class TestStateNode(TestCase):
    """
    The StateNode class test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self._loggingMod = 'pkgs.ui.models.stateNode.logging'
        self._name = 'test state node'
        self._value = 12
        with patch(self._loggingMod):
            self._uut = StateNode(self._name, self._value)

    def test_constructorGetLogger(self) -> None:
        """
        The constructor must get and save the state logger.
        """
        name = 'test node'
        value = 12000
        with patch(self._loggingMod) as mockedLogging:
            StateNode(name, value)
            mockedLogging.getLogger \
                .assert_called_once_with(f"app.datastoreModel.MULTI_STATE."
                                         f"state.{name}")

    def test_constructorSaveNameAndValue(self) -> None:
        name = 'test node'
        value = 12000
        with patch(self._loggingMod):
            uut = StateNode(name, value)
            self.assertEqual(name, uut._name)
            self.assertEqual(value, uut._value)

    def test_getNameReturnName(self) -> None:
        """
        The getName method must return the state name.
        """
        self.assertEqual(self._name, self._uut.getName())

    def test_setNameSaveNewName(self) -> None:
        """
        The setName method must save the state new name.
        """
        name = 'new name'
        self._uut.setName(name)
        self.assertEqual(name, self._uut._name)

    def test_getValueReturnValue(self) -> None:
        """
        The getValue method must return the state value.
        """
        self.assertEqual(self._value, self._uut.getValue())

    def test_setValueSaveNewValue(self) -> None:
        """
        The setValue method must save the state new value.
        """
        value = 0
        self._uut.setValue(value)
        self.assertEqual(value, self._uut._value)

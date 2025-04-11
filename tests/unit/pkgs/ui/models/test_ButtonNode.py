from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.models import ButtonData, ButtonNode, NodeType     # noqa: E402


class TestButtonNode(TestCase):
    """
    ButtonNode class test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self._BaseNodeCls = 'pkgs.ui.models.buttonNode.BaseNode'
        with patch(f"{self._BaseNodeCls}.__init__"):
            self._data = ButtonData(30000, 40000)
            self._uut = ButtonNode('test button', self._data)

    def test_constructorBaseClassInitAndSaveData(self) -> None:
        """
        The constructor must call the base class constructor save the button
        array object data.
        """
        name = 'test node'
        data = Mock()
        parent = Mock()
        with patch(f"{self._BaseNodeCls}.__init__") as mockedBaseNode:
            uut = ButtonNode(name, data, parent)
            mockedBaseNode.assert_called_once_with(name, NodeType.BUTTON,
                                                   parent=parent)
            self.assertEqual(data, uut._data)

    def test_getLongPressTimeReturnTime(self) -> None:
        """
        The getLongPressTime method must return the long press time.
        """
        self.assertEqual(self._data.longPressTime,
                         self._uut.getLongPressTime())

    def test_setLongPressTimeSaveTime(self) -> None:
        """
        The setLongPress method must save the new long press time.
        """
        time = 3000
        self._uut.setLongPressTime(time)
        self.assertEqual(time, self._uut._data.longPressTime)

    def test_getInactiveTimeReturnTime(self) -> None:
        """
        The getInactiveTime method must return the inactive time.
        """
        self.assertEqual(self._data.inactiveTime,
                         self._uut.getInactiveTime())

    def test_setInactiveTimeSaveTime(self) -> None:
        """
        The setInactive method must save the new inactive time.
        """
        time = 6000
        self._uut.setInactiveTime(time)
        self.assertEqual(time, self._uut._data.inactiveTime)

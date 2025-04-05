from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.models import IntArrayData, IntArrayElement, \
    IntArrayNode, IntData, IntNode, NodeType                    # noqa: E402


class TestIntNode(TestCase):
    """
    IntNode class test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self._BaseNodeCls = 'pkgs.ui.models.intNode.BaseNode'
        with patch(f"{self._BaseNodeCls}.__init__"):
            self._data = IntData(0, 10, 1)
            self._uut = IntNode('test node', self._data)

    def test_constructorBaseClassInitAndSaveData(self) -> None:
        """
        The constructor must call the base class constructor save the int
        object data.
        """
        name = 'test node'
        data = Mock()
        parent = Mock()
        with patch(f"{self._BaseNodeCls}.__init__") as mockedBaseNode:
            uut = IntNode(name, data, parent)
            mockedBaseNode.assert_called_once_with(name, NodeType.INT,
                                                   parent=parent)
            self.assertEqual(data, uut._data)

    def test_getMinimumReturnMin(self) -> None:
        """
        The getMinimum method must return the minimum value of the int.
        """
        self.assertEqual(self._data.min, self._uut.getMinimum())

    def test_setMinimumSaveMin(self) -> None:
        """
        The setMinimum method must save the minimum value of the int.
        """
        min = -12
        self._uut.setMinimum(min)
        self.assertEqual(min, self._uut._data.min)

    def test_getMaximumReturnMax(self) -> None:
        """
        The getMaximum method must return the maximum value of the int.
        """
        self.assertEqual(self._data.max, self._uut.getMaximum())

    def test_setMaximumSaveMax(self) -> None:
        """
        The setMaximum method must save the maximum value of the int.
        """
        max = 12
        self._uut.setMaximum(max)
        self.assertEqual(max, self._uut._data.max)

    def test_getDefaultReturnDefault(self) -> None:
        """
        The getDefault method must return the default value of the int.
        """
        self.assertEqual(self._data.default, self._uut.getDefault())

    def test_setDefaultSaveDefault(self) -> None:
        """
        The setDefault method must save the default value of the int.
        """
        default = 6
        self._uut.setDefault(default)
        self.assertEqual(default, self._uut._data.default)


class TestIntArrayNode(TestCase):
    """
    IntArrayNode class test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self._BaseNodeCls = 'pkgs.ui.models.intNode.BaseNode'

    def test_constructorBaseClassInitAndSaveData(self) -> None:
        """
        The constructor must call the base class constructor save the int array
        object data.
        """
        name = 'test node'
        data = Mock()
        parent = Mock()
        with patch(f"{self._BaseNodeCls}.__init__") as mockedBaseNode:
            uut = IntArrayNode(name, data, parent)
            mockedBaseNode.assert_called_once_with(name, NodeType.INT_ARRAY,
                                                   parent=parent)
            self.assertEqual(data, uut._data)

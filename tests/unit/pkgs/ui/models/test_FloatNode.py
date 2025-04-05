from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.models import FloatArrayData, FloatArrayElement, \
    FloatArrayNode, FloatData, FloatNode, NodeType              # noqa: E402


class TestFloatNode(TestCase):
    """
    FloatNode class test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self._BaseNodeCls = 'pkgs.ui.models.intNode.BaseNode'
        with patch(f"{self._BaseNodeCls}.__init__"):
            self._data = FloatData(0.0, 10.0, 1.0)
            self._uut = FloatNode('test node', self._data)

    def test_constructorBaseClassInitAndSaveData(self) -> None:
        """
        The constructor must call the base class constructor save the float
        object data.
        """
        name = 'test node'
        data = Mock()
        parent = Mock()
        with patch(f"{self._BaseNodeCls}.__init__") as mockedBaseNode:
            uut = FloatNode(name, data, parent)
            mockedBaseNode.assert_called_once_with(name, NodeType.FLOAT,
                                                   parent=parent)
            self.assertEqual(data, uut._data)

    def test_getMinimumReturnMin(self) -> None:
        """
        The getMinimum method must return the minimum value of the float.
        """
        self.assertEqual(self._data.min, self._uut.getMinimum())

    def test_setMinimumSaveMin(self) -> None:
        """
        The setMinimum method must save the minimum value of the float.
        """
        min = -12.0
        self._uut.setMinimum(min)
        self.assertEqual(min, self._uut._data.min)

    def test_getMaximumReturnMax(self) -> None:
        """
        The getMaximum method must return the maximum value of the float.
        """
        self.assertEqual(self._data.max, self._uut.getMaximum())

    def test_setMaximumSaveMax(self) -> None:
        """
        The setMaximum method must save the maximum value of the float.
        """
        max = 12.0
        self._uut.setMaximum(max)
        self.assertEqual(max, self._uut._data.max)

    def test_getDefaultReturnDefault(self) -> None:
        """
        The getDefault method must return the default value of the float.
        """
        self.assertEqual(self._data.default, self._uut.getDefault())

    def test_setDefaultSaveDefault(self) -> None:
        """
        The setDefault method must save the default value of the float.
        """
        default = 6.0
        self._uut.setDefault(default)
        self.assertEqual(default, self._uut._data.default)


class TestFloatArrayNode(TestCase):
    """
    FloatArrayNode class test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self._BaseNodeCls = 'pkgs.ui.models.intNode.BaseNode'

    def test_constructorBaseClassInitAndSaveData(self) -> None:
        """
        The constructor must call the base class constructor save the float
        array object data.
        """
        name = 'test node'
        data = Mock()
        parent = Mock()
        with patch(f"{self._BaseNodeCls}.__init__") as mockedBaseNode:
            uut = FloatArrayNode(name, data, parent)
            mockedBaseNode.assert_called_once_with(name, NodeType.FLOAT_ARRAY,
                                                   parent=parent)
            self.assertEqual(data, uut._data)

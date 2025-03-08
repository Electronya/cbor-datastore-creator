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

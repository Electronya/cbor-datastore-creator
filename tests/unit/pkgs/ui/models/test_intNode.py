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

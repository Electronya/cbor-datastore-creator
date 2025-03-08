from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.models import UintArrayData, UintArrayElement, \
    UintArrayNode, UintData, UintNode, NodeType                 # noqa: E402


class TestUintNode(TestCase):
    """
    UintNode class test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self._BaseNodeCls = 'pkgs.ui.models.uintNode.BaseNode'

    def test_constructorBaseClassInitAndSaveData(self) -> None:
        """
        The constructor must call the base class constructor save the uint
        object data.
        """
        name = 'test node'
        data = Mock()
        parent = Mock()
        with patch(f"{self._BaseNodeCls}.__init__") as mockedBaseNode:
            uut = UintNode(name, data, parent)
            mockedBaseNode.assert_called_once_with(name, NodeType.UINT,
                                                   parent=parent)
            self.assertEqual(data, uut._data)


class TestUintArrayNode(TestCase):
    """
    UintArrayNode class test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self._BaseNodeCls = 'pkgs.ui.models.datastoreNode.BaseNode'

    def test_constructorBaseClassInitAndSaveData(self) -> None:
        """
        The constructor must call the base class constructor save the uint
        array object data.
        """
        name = 'test node'
        data = Mock()
        parent = Mock()
        with patch(f"{self._BaseNodeCls}.__init__") as mockedBaseNode:
            uut = UintArrayNode(name, data, parent)
            mockedBaseNode.assert_called_once_with(name, NodeType.UINT_ARRAY,
                                                   parent=parent)
            self.assertEqual(data, uut._data)

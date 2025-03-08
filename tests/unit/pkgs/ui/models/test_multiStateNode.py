from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.models import MultiStateData, MultiStateNode, NodeType     # noqa: E402 E501


class TestMultiStateNode(TestCase):
    """
    IntNode class test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self._BaseNodeCls = 'pkgs.ui.models.multiStateNode.BaseNode'

    def test_constructorBaseClassInitAndSaveData(self) -> None:
        """
        The constructor must call the base class constructor save the int
        object data.
        """
        name = 'test node'
        data = Mock()
        parent = Mock()
        with patch(f"{self._BaseNodeCls}.__init__") as mockedBaseNode:
            uut = MultiStateNode(name, data, parent)
            mockedBaseNode.assert_called_once_with(name, NodeType.MULTI_STATE,
                                                   parent=parent)
            self.assertEqual(data, uut._data)

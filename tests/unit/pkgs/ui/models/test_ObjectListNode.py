from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.models import NodeType, ObjectListNode             # noqa: E402


class TestObjectList(TestCase):
    """
    ObjectListNode class test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self._BaseNodeCls = 'pkgs.ui.models.objectListNode.BaseNode'

    def test_constructorBaseClassInit(self) -> None:
        """
        The constructor must call the base class constructor.
        """
        name = 'test node'
        parent = Mock()
        with patch(f"{self._BaseNodeCls}.__init__") as mockedBaseNode:
            ObjectListNode(name, parent)
            mockedBaseNode.assert_called_once_with(name, NodeType.OBJ_LIST,
                                                   parent=parent)

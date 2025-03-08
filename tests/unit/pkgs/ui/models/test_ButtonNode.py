from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.models import ButtonArrayData, ButtonArrayElement, \
    ButtonArrayNode, ButtonData, ButtonNode, NodeType     # noqa: E402


class TestButtonNode(TestCase):
    """
    ButtonNode class test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self._BaseNodeCls = 'pkgs.ui.models.datastoreNode.BaseNode'

    def test_constructorBaseClassInitAndSaveData(self) -> None:
        """
        The constructor must call the base class constructor save the button
        object data.
        """
        name = 'test node'
        data = Mock()
        parent = Mock()
        with patch(f"{self._BaseNodeCls}.__init__") as mockedBaseNode:
            uut = ButtonNode(name, data, parent)
            mockedBaseNode.assert_called_once_with(name, NodeType.BUTTON,
                                                   parent=parent)
            self.assertEqual(data, uut._data)


class TestButtonArrayNode(TestCase):
    """
    ButtonArrayNode class test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self._BaseNodeCls = 'pkgs.ui.models.datastoreNode.BaseNode'

    def test_constructorBaseClassInitAndSaveData(self) -> None:
        """
        The constructor must call the base class constructor save the button
        object data.
        """
        name = 'test node'
        data = Mock()
        parent = Mock()
        with patch(f"{self._BaseNodeCls}.__init__") as mockedBaseNode:
            uut = ButtonArrayNode(name, data, parent)
            mockedBaseNode.assert_called_once_with(name, NodeType.BUTTON_ARRAY,
                                                   parent=parent)
            self.assertEqual(data, uut._data)

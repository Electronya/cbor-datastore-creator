from unittest import TestCase
from unittest.mock import Mock

from PySide6.QtCore import Qt

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.models import BaseNode, NodeType                   # noqa: E402


class TestBaseNode(TestCase):
    """
    BaseNode test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self._testName = 'test node'
        self._testType = NodeType.BUTTON_ARRAY
        self._testParent = Mock()
        self._testChildren = [Mock(), Mock(), Mock()]
        self._uut = BaseNode(self._testName, self._testType,
                             parent=self._testParent)
        self._uut._children = self._testChildren

    def test_constructorSaveDataAddToParent(self) -> None:
        """
        The constructor must save the node name and type, create an empty
        children list and add itself to the parent children if a parent is
        given.
        """
        datasets = [{'name': 'node 1', 'type': NodeType.STORE, 'parent': None},
                    {'name': 'node 2', 'type': NodeType.INT, 'parent': Mock()}]
        for dataset in datasets:
            uut = BaseNode(dataset['name'], dataset['type'],
                           parent=dataset['parent'])
            self.assertEqual(dataset['name'], uut._name)
            self.assertEqual(dataset['type'], uut._type)
            self.assertEqual(dataset['parent'], uut._parent)
            if dataset['parent'] is not None:
                dataset['parent'].addChild.assert_called_once_with(uut)

    def test_getNameReturnNodeName(self) -> None:
        """
        The getName method must return the node name.
        """
        self.assertEqual(self._testName, self._uut.getName())

    def test_setNameSaveNewName(self) -> None:
        """
        The setName method must save the new node name.
        """
        name = 'new name'
        self._uut.setName(name)
        self.assertEqual(name, self._uut._name)

    def test_getChildCountReturnCount(self) -> None:
        """
        The getChildCount must return the node child count.
        """
        self.assertEqual(len(self._testChildren), self._uut.getChildCount())

    def test_getChildDoesNotExist(self) -> None:
        """
        The getChild method must return None if the given row does not exists.
        """
        row = len(self._testChildren)
        self.assertIsNone(self._uut.getChild(row))

    def test_getChildExists(self) -> None:
        """
        The getChild method must return the node child at the given row.
        """
        row = len(self._testChildren) - 1
        self.assertEqual(self._testChildren[row], self._uut.getChild(row))

    def test_addChildAppendNewChild(self) -> None:
        newChildCount = len(self._uut._children) + 1
        newChild = Mock()
        self._uut.addChild(newChild)
        self.assertEqual(newChildCount, len(self._uut._children))
        self.assertEqual(newChild, self._uut._children[-1])
        self.assertEqual(self._uut, newChild._parent)

    def test_addChildAtRowOutOfRange(self) -> None:
        """
        The addChildAt must return false if the row is not valid.
        """
        length = len(self._uut._children)
        rows = [-1, length]
        child = Mock()
        for row in rows:
            self.assertFalse(self._uut.addChildAt(row, child))
            self.assertEqual(length, len(self._uut._children))

    def test_addChildInsertChild(self) -> None:
        """
        The addChildAt must insert the new child and return true when the
        operation succeeds.
        """
        newLength = len(self._uut._children) + 1
        row = len(self._uut._children) - 2
        child = Mock()
        self.assertTrue(self._uut.addChildAt(row, child))
        self.assertEqual(newLength, len(self._uut._children))
        self.assertEqual(child, self._uut._children[row])
        self.assertEqual(self._uut, child._parent)

    def test_removeChildAtRowOutOfRange(self) -> None:
        """
        The removeChildAt method must return false if the row is not valid.
        """
        length = len(self._uut._children)
        rows = [-1, length]
        for row in rows:
            self.assertFalse(self._uut.removeChildAt(row))
            self.assertEqual(length, len(self._uut._children))

    def test_removeChildAtRemoveChild(self) -> None:
        """
        The removeChildAt must remove the child at the given row and return
        true when the operation succeeds.
        """
        length = len(self._uut._children) - 1
        row = length - 1
        removedChild = self._uut._children[row]
        self.assertTrue(self._uut.removeChildAt(row))
        self.assertEqual(length, len(self._uut._children))
        self.assertFalse(removedChild in self._uut._children)

    def test_getParent(self) -> None:
        """
        The getParent method must return the node parent.
        """
        self.assertEqual(self._testParent, self._uut.getParent())

    def test_getRowNoParent(self) -> None:
        """
        The getRow must return none if the node has no parent.
        """
        self._uut._parent = None
        self.assertIsNone(self._uut.getRow())

    def test_getRowWithParent(self) -> None:
        """
        The getRow must return the node row when it has a parent.
        """
        row = 3
        self._testParent._children.index.return_value = row
        self.assertEqual(row, self._uut.getRow())

    def test_getFlagsObjectList(self) -> None:
        """
        The getFlags method must return the only the selectable and enabled
        item flags when the node is of object list type.
        """
        self._uut._type = NodeType.OBJ_LIST
        flags = Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        self.assertEqual(flags, self._uut.getFlags())

    def test_getFlagsNotObjectList(self) -> None:
        """
        The getFlags method must return the selectable, enabled and editable
        flags when the node is not of the object list type.
        """
        flags = Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | \
            Qt.ItemFlag.ItemIsEditable
        for type in NodeType:
            if type != NodeType.OBJ_LIST:
                self._uut._type = type
                self.assertEqual(flags, self._uut.getFlags())

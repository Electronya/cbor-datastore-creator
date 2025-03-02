from unittest import TestCase
from unittest.mock import Mock

from PySide6.QtCore import Qt

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.models import DatastoreNode, DatastoreNodeType     # noqa: E402


class TestDatastoreNode(TestCase):
    """
    DatastoreNode test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self._mockedChildren = []
        for i in range(10):
            self._mockedChildren.append(Mock())

        self._mockedStoreData = Mock()
        self._uutStore = DatastoreNode(DatastoreNodeType.STORE,
                                       data=self._mockedStoreData)
        self._uutStore._children = self._mockedChildren

        self._listName = 'list name'
        self._mockedListParent = Mock()
        self._uutObjList = DatastoreNode(DatastoreNodeType.OBJ_LIST,
                                         name=self._listName,
                                         parent=self._mockedListParent)
        self._uutObjList._children = self._mockedChildren

        self._mockedObjParent = Mock()
        self._mockedObjData = Mock()
        self._uutObj = DatastoreNode(DatastoreNodeType.OBJECT,
                                     self._mockedObjData,
                                     parent=self._mockedObjParent)

        self._uuts = [self._uutStore, self._uutObjList, self._uutObj]

    def test_constructorSaveDataAddToParent(self) -> None:
        """
        The constructor must save the node data and name, and add himself
        to the parent child when one is given.
        """
        testDatasets = [
            {'type': DatastoreNodeType.STORE,
             'data': None, 'parent': None, 'name': None},
            {'type': DatastoreNodeType.OBJ_LIST,
             'data': None, 'parent': Mock(), 'name': 'test name'},
            {'type': DatastoreNodeType.OBJECT,
             'data': Mock(), 'parent': Mock(), 'name': None}
        ]
        for testDataset in testDatasets:
            uut = DatastoreNode(testDataset['type'],
                                data=testDataset['data'],
                                name=testDataset['name'],
                                parent=testDataset['parent'])
            self.assertEqual(testDataset['data'], uut._data)
            self.assertEqual(testDataset['name'], uut._name)
            self.assertEqual(testDataset['parent'], uut._parent)
            if testDataset['parent'] is not None:
                testDataset['parent'].addChild.assert_called_once()

    def test_getNameReturnName(self) -> None:
        """
        The getName method must return the saved name when the type is object
        list or the contained data name otherwise.
        """
        for uut in self._uuts:
            if uut._type != DatastoreNodeType.OBJ_LIST:
                name = 'object name'
                uut._data.getName.return_value = name
                self.assertEqual(name, uut.getName())
            else:
                self.assertEqual(uut._name, uut.getName())

    def test_setNameSaveNewName(self) -> None:
        """
        The setName method must save the new name in the node internal data
        when the node is of store or object type. If the node is of object list
        type, nothing is done.
        """
        name = 'new name'
        for uut in self._uuts:
            uut.setName(name)
            if uut._type == DatastoreNodeType.OBJ_LIST:
                self.assertEqual(self._listName, uut._name)
            else:
                uut._data.setName.assert_called_once_with(name)

    def test_getChildCountReturnCount(self) -> None:
        """
        The getChildCount method must return the node child count.
        """
        for uut in self._uuts:
            self.assertEqual(len(uut._children), uut.getChildCount())

    def test_getChildReturnChildAtRow(self) -> None:
        """
        The getChild must return the child present at the given row if children
        are present, none otherwise.
        """
        rows = [0, int(len(self._mockedChildren) / 2),
                len(self._mockedChildren) - 1]
        for uut in self._uuts:
            for row in rows:
                if uut._type == DatastoreNodeType.OBJECT:
                    self.assertEqual(None, uut.getChild(row))
                else:
                    self.assertEqual(self._mockedChildren[row],
                                     uut.getChild(row))

    def test_addChildAppendChild(self) -> None:
        """
        The addChild method must append the new child in the list.
        """
        for uut in self._uuts:
            newChild = Mock()
            expectedChildCount = len(uut._children) + 1
            uut.addChild(newChild)
            self.assertEqual(newChild, uut._children[-1])
            self.assertEqual(expectedChildCount, len(uut._children))

    def test_addChildAtIndexOutOfRange(self) -> None:
        """
        The addChildAt must return false when the given index is out of range.
        """
        child = Mock()
        for uut in self._uuts:
            indexes = [-1, len(uut._children) + 1]
            for index in indexes:
                self.assertFalse(uut.addChildAt(index, child))

    def test_addChildAtInsertNewChild(self) -> None:
        """
        The addChildAt must return true and insert the .
        """
        index = 0
        child = Mock()
        for uut in self._uuts:
            self.assertTrue(uut.addChildAt(index, child))
            self.assertEqual(uut, child._parent)
            self.assertEqual(child, uut._children[index])

    def test_removeChildAtIndexOutOfRange(self) -> None:
        """
        The removeChildAt must return false when the given index is out of
        range.
        """
        for uut in self._uuts:
            indexes = [-1, len(uut._children) + 1]
            for index in indexes:
                self.assertFalse(uut.removeChildAt(index))

    def test_removeChildAtNoChildren(self) -> None:
        """
        The removeChildAt must return false when the node has no children.
        """
        self.assertFalse(self._uutObj.removeChildAt(0))

    def test_removeChildAtRemoveChild(self) -> None:
        """
        The removeChildAt must return false when the given index is out of
        range.
        """
        index = 0
        for uut in self._uuts:
            if len(uut._children) > 0:
                newLength = len(uut._children) - 1
                self.assertTrue(uut.removeChildAt(index))
                self.assertEqual(newLength, len(uut._children))

    def test_getParentReturnParent(self) -> None:
        """
        The getParent method must return the node parent if it exist, none
        otherwise.
        """
        for uut in self._uuts:
            self.assertEqual(uut._parent, uut.getParent())

    def test_getRowReturnRowFromParent(self) -> None:
        """
        The getRow method must return the row of the node from its parent when
        the node has a parent, none otherwise.
        """
        row = 12
        for uut in self._uuts:
            if uut._type == DatastoreNodeType.STORE:
                self.assertEqual(None, uut.getRow())
            else:
                uut._parent._children.index.return_value = row
                self.assertEqual(row, uut.getRow())

    def test_getDataReturnData(self) -> None:
        """
        The getData method must return the node data if its present, none
        otherwise.
        """
        for uut in self._uuts:
            if uut._type == DatastoreNodeType.OBJ_LIST:
                self.assertEqual(None, uut.getData())
            else:
                self.assertEqual(uut._data, uut.getData())

    def test_getFlagsReturnSelectableOrNoFlag(self) -> None:
        """
        The getFlags method must return the selectable, editable and enabled
        flag if it a store or an object node, or the selectable and enabled
        flag otherwise.
        """
        for uut in self._uuts:
            if uut._type == DatastoreNodeType.OBJ_LIST:
                flags = Qt.ItemFlag.ItemIsSelectable | \
                    Qt.ItemFlag.ItemIsEnabled
                self.assertEqual(flags, uut.getFlags())
            else:
                flags = Qt.ItemFlag.ItemIsSelectable | \
                    Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled
                self.assertEqual(flags, uut.getFlags())

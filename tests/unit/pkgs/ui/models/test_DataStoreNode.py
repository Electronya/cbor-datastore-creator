from unittest import TestCase
from unittest.mock import Mock, patch

from PySide6.QtCore import Qt

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.models import DatastoreNode                        # noqa: E402


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

        self._listName = 'list name'
        self._uutObjList = DatastoreNode(name=self._listName)
        self._uutObjList._children = self._mockedChildren

        self._mockedParent = Mock()
        self._mockedData = Mock()
        self._uutObj = DatastoreNode(self._mockedData,
                                     parent=self._mockedParent)

    def test_constructorSaveDataAddToParent(self) -> None:
        """
        The constructor must save the node data and name, and add himself
        to the parent child when one is given.
        """
        testDatasets = [
            {'data': None, 'parent': None, 'name': None},
            {'data': Mock(), 'parent': Mock(), 'name': 'test name'}
        ]
        for testDataset in testDatasets:
            uut = DatastoreNode(data=testDataset['data'],
                                name=testDataset['name'],
                                parent=testDataset['parent'])
            self.assertEqual(testDataset['data'], uut._data)
            self.assertEqual(testDataset['name'], uut._name)
            self.assertEqual(testDataset['parent'], uut._parent)
            if testDataset['parent'] is not None:
                testDataset['parent'].addChild.assert_called_once()

    def test_getNameAsListOfObject(self) -> None:
        """
        The getName method must return the node save name when the node
        is an object list.
        """
        self.assertEqual(self._listName, self._uutObjList.getName())

    def test_getNameAsObject(self) -> None:
        """
        The getName method must return the contained object name as the node
        name when the node is an object.
        """
        name = 'object name'
        self._mockedData.getName.return_value = name
        self.assertEqual(name, self._uutObj.getName())

    def test_getChildCountReturnCount(self) -> None:
        """
        The getChildCount method must return the node child count.
        """
        self.assertEqual(len(self._mockedChildren),
                         self._uutObjList.getChildCount())
        self.assertEqual(0, self._uutObj.getChildCount())

    def test_getChildReturnChildAtRow(self) -> None:
        """
        The getChild must return the child present at the given row.
        """
        rows = [0, int(len(self._mockedChildren) / 2),
                len(self._mockedChildren) - 1]
        for row in rows:
            self.assertEqual(self._mockedChildren[row],
                             self._uutObjList.getChild(row))

    def test_addChildAppendChild(self) -> None:
        """
        The addChild method must append the new child in the list.
        """
        newChild = Mock()
        expectedChildCount = len(self._mockedChildren) + 1
        self._uutObjList.addChild(newChild)
        self.assertEqual(newChild, self._mockedChildren[-1])
        self.assertEqual(expectedChildCount, len(self._mockedChildren))

    def test_getParentReturnParentOrNone(self) -> None:
        """
        The getParent method must return the node parent if it exist, none
        otherwise.
        """
        self.assertEqual(None, self._uutObjList.getParent())
        self.assertEqual(self._mockedParent, self._uutObj.getParent())

    def test_getRowReturnRowFromParentOrNone(self) -> None:
        """
        The getRow method must return the row of the node from its parent when
        the node has a parent, none otherwise.
        """
        self.assertEqual(None, self._uutObjList.getRow())
        row = 12
        self._mockedParent._children.index.return_value = row
        self.assertEqual(row, self._uutObj.getRow())

    def test_getDataReturnDataOrNone(self) -> None:
        """
        The getData method must return the node data if its present, none
        otherwise.
        """
        self.assertEqual(None, self._uutObjList.getData())
        self.assertEqual(self._mockedData, self._uutObj.getData())

    def test_getFlagsReturnSelectableOrNoFlag(self) -> None:
        """
        The getFlags method must return the selectable flag if it has a parent
        or the none flag otherwise.
        """
        self.assertEqual(Qt.ItemFlag.NoItemFlags, self._uutObjList.getFlags())
        self.assertEqual(Qt.ItemFlag.ItemIsSelectable, self._uutObj.getFlags())

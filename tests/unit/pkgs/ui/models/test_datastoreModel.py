from unittest import TestCase
from unittest.mock import Mock, patch

from PySide6.QtCore import Qt

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.models import DatastoreModel       # noqa: E402


class TestDatastoreModel(TestCase):
    """
    DatastoreModel test cases.
    """
    def setUp(self) -> None:
        self._QAbstractItemModelCls = 'pkgs.ui.models.datastoreModel.qtc.' \
            'QAbstractItemModel'
        self._QModelIndexCls = 'pkgs.ui.models.datastoreModel.qtc.QModelIndex'
        self._ButtonDataCls = 'pkgs.ui.models.datastoreModel.ButtonData'
        self._ButtonNodeCls = 'pkgs.ui.models.datastoreModel.ButtonNode'
        self._mockedRoot = Mock()
        with patch(f"{self._QAbstractItemModelCls}.__init__"):
            self._uut = DatastoreModel(self._mockedRoot)

    def test_constructorSetup(self) -> None:
        """
        The constructor must call the base class constructor and save the
        datastore and save the root node.
        """
        parent = 10
        with patch(f"{self._QAbstractItemModelCls}.__init__") as mockedBaseCls:
            uut = DatastoreModel(self._mockedRoot, parent=parent)
            mockedBaseCls.assert_called_once_with(parent)
        self.assertEqual(self._mockedRoot, uut._root)

    def test_appendButtonNode(self) -> None:
        """
        The _appendButtonNode method must create a new button node and append
        it the given button list.
        """
        name = 'NEW_BUTTON'
        buttonData = Mock()
        buttonNode = Mock()
        buttonList = Mock()
        with patch(self._ButtonDataCls) as mockedButtonData, \
                patch(self._ButtonNodeCls) as mockedButtonNode:
            mockedButtonData.return_value = buttonData
            mockedButtonNode.return_value = buttonNode
            self._uut._appendButtonNode(buttonList)
            mockedButtonData.assert_called_once_with()
            mockedButtonNode.assert_called_once_with(name, buttonData)
            buttonList.addChild.assert_called_once_with(buttonNode)

    def test_rowCountReturnRowCount(self) -> None:
        """
        The rowCount method must return the given node child count if the
        index is valid, otherwise return the child count of the root node.
        """
        validFlags = [True, False]
        nodeIdx = Mock()
        node = Mock()
        rowCount = 10
        for validFlag in validFlags:
            if validFlag:
                nodeIdx.internalPointer.return_value = node
                node.getChildCount.return_value = rowCount
            else:
                self._mockedRoot.getChildCount.return_value = rowCount
            result = self._uut.rowCount(nodeIdx)
            if validFlag:
                nodeIdx.internalPointer.assert_called_once_with()
                node.getChildCount.assert_called_once_with()
            else:
                self._mockedRoot.getChildCount.asset_called_once_with()
            self.assertEqual(rowCount, result)

    def test_columnCountReturnColumnCount(self) -> None:
        """
        The column count must return 1.
        """
        nodeIdx = Mock()
        self.assertEqual(1, self._uut.columnCount(nodeIdx))

    def test_dataDisplayRoleReturnNodeName(self) -> None:
        """
        The data method must return, when the role is the display one, the node
        name if the index is valid, otherwise return the root node name.
        """
        validFlags = [True, False]
        nodeIdx = Mock()
        node = Mock()
        name = 'test node'
        role = Qt.ItemDataRole.DisplayRole
        for validFlag in validFlags:
            if validFlag:
                nodeIdx.internalPointer.return_value = node
                node.getName.return_value = name
            else:
                self._mockedRoot.getName.return_value = name
            result = self._uut.data(nodeIdx, role)
            if validFlag:
                nodeIdx.internalPointer.assert_called_once_with()
                node.getName.assert_called_once_with()
            else:
                self._mockedRoot.getName.asset_called_once_with()
            self.assertEqual(name, result)

    def test_dataEditRoleReturnNodeName(self) -> None:
        """
        The data method must return, when the role is the edit one, the node
        name if the index is valid, otherwise return the root node name.
        """
        validFlags = [True, False]
        nodeIdx = Mock()
        node = Mock()
        name = 'test node'
        role = Qt.ItemDataRole.EditRole
        for validFlag in validFlags:
            if validFlag:
                nodeIdx.internalPointer.return_value = node
                node.getName.return_value = name
            else:
                self._mockedRoot.getName.return_value = name
            result = self._uut.data(nodeIdx, role)
            if validFlag:
                nodeIdx.internalPointer.assert_called_once_with()
                node.getName.assert_called_once_with()
            else:
                self._mockedRoot.getName.asset_called_once_with()
            self.assertEqual(name, result)

    def test_setDataInvalidNode(self) -> None:
        """
        The setData method must return false and do nothing if the node is
        invalid.
        """
        name = 'new name'
        nodeIdx = Mock()
        nodeIdx.isValid.return_value = False
        self.assertFalse(self._uut.setData(nodeIdx, name,
                                           Qt.ItemDataRole.EditRole))
        nodeIdx.internalPointer.assert_not_called()

    def test_setDataNotEditRole(self) -> None:
        """
        The setData method must return false do nothing if the node is valid
        and the role is not the edit one.
        """
        name = 'new name'
        nodeIdx = Mock()
        nodeIdx.isValid.return_value = True
        self.assertFalse(self._uut.setData(nodeIdx, name,
                                           Qt.ItemDataRole.DisplayRole))
        nodeIdx.internalPointer.assert_not_called()

    def test_setDataUpdateNodeName(self) -> None:
        """
        The setData method must update the node name if the node is valid and
        the role is the edit one.
        """
        name = 'new name'
        node = Mock()
        nodeIdx = Mock()
        nodeIdx.isValid.return_value = True
        nodeIdx.internalPointer.return_value = node
        self.assertTrue(self._uut.setData(nodeIdx, name,
                                          Qt.ItemDataRole.EditRole))
        nodeIdx.internalPointer.assert_called_once_with()
        node.setName.assert_called_once_with(name)

    def test_flagsReturnNodeFlags(self) -> None:
        """
        The flags method must return the given node flags if the index is
        valid, otherwise return the root node flags.
        """
        validFlags = [True, False]
        nodeIdx = Mock()
        node = Mock()
        flags = 10
        for validFlag in validFlags:
            if validFlag:
                nodeIdx.internalPointer.return_value = node
                node.getFlags.return_value = flags
            else:
                self._mockedRoot.getFlags.return_value = flags
            result = self._uut.flags(nodeIdx)
            if validFlag:
                nodeIdx.internalPointer.assert_called_once_with()
                node.getFlags.assert_called_once_with()
            else:
                self._mockedRoot.getFlags.asset_called_once_with()
            self.assertEqual(flags, result)

    def test_parentReturnNodeParent(self) -> None:
        """
        The parent method must return the index of the parent of the node at
        the given index if the node has a parent, otherwise return an invalid
        index.
        """
        parents = [Mock(), self._mockedRoot]
        mockedParentIndex = Mock()
        index = Mock()
        node = Mock()
        row = 10
        for parent in parents:
            index.internalPointer.return_value = node
            node.getParent.return_value = parent
            parent.getRow.return_value = row
            with patch(self._QModelIndexCls) as mockedIndexCls, \
                    patch.object(DatastoreModel, 'createIndex') \
                    as mockedCreateIdx:
                mockedIndexCls.return_value = mockedParentIndex
                mockedCreateIdx.return_value = mockedParentIndex
                result = self._uut.parent(index)
                if parent == self._mockedRoot:
                    mockedIndexCls.assert_called_once_with()
                else:
                    mockedCreateIdx.assert_called_once_with(row, 0, parent)
            self.assertEqual(mockedParentIndex, result)

    def test_indexInvalidParent(self) -> None:
        """
        The index method must use the root node if the given parent index is
        invalid and return either the child index at the given row and column
        when found or an invalid index if no child was found.
        """
        parent = Mock()
        parentNode = Mock()
        childIndex = Mock()
        children = [Mock(), None]
        row = 2
        column = 10
        for child in children:
            parent.isValid.return_value = False
            self._mockedRoot.getChild.return_value = child
            with patch(self._QModelIndexCls) as mockedIndexCls, \
                    patch.object(DatastoreModel, 'createIndex') \
                    as mockedCreateIdx:
                mockedIndexCls.return_value = childIndex
                mockedCreateIdx.return_value = childIndex
                parentNode.getChild.return_value = child
                result = self._uut.index(row, column, parent)
                if child is None:
                    mockedIndexCls.assert_called_once_with()
                else:
                    mockedCreateIdx.assert_called_once_with(row, column, child)
                parent.internalPointer.assert_not_called()
                self.assertEqual(childIndex, result)

    def test_indexValidParent(self) -> None:
        """
        The index method must use the parent node if the given parent index is
        valid and return either the child index at the given row and column
        when found or an invalid index if no child was found.
        """
        nodeIdx = Mock()
        node = Mock()
        childIndex = Mock()
        children = [Mock(), None]
        row = 2
        column = 10
        for child in children:
            nodeIdx.isValid.return_value = True
            nodeIdx.internalPointer.return_value = node
            node.getChild.return_value = child
            with patch(self._QModelIndexCls) as mockedIndexCls, \
                    patch.object(DatastoreModel, 'createIndex') \
                    as mockedCreateIdx:
                mockedIndexCls.return_value = childIndex
                mockedCreateIdx.return_value = childIndex
                node.getChild.return_value = child
                result = self._uut.index(row, column, nodeIdx)
                if child is None:
                    mockedIndexCls.assert_called_once_with()
                else:
                    mockedCreateIdx.assert_called_once_with(row, column, child)
                nodeIdx.internalPointer.assert_called_once_with()
                self.assertEqual(childIndex, result)
            nodeIdx.reset_mock()

    def test_insertRowAddRootSuccess(self) -> None:
        """
        The insertRow method must add the new child to the root node when the
        given index is invalid and return true when the operation succeeds.
        """

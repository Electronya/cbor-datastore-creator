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
        self._ButtonArrayDataCls = 'pkgs.ui.models.datastoreModel.' \
            'ButtonArrayData'
        self._ButtonArrayNodeCls = 'pkgs.ui.models.datastoreModel.' \
            'ButtonArrayNode'
        self._FloatDataCls = 'pkgs.ui.models.datastoreModel.FloatData'
        self._FloatNodeCls = 'pkgs.ui.models.datastoreModel.FloatNode'
        self._FloatArrayDataCls = 'pkgs.ui.models.datastoreModel.' \
            'FloatArrayData'
        self._FloatArrayNodeCls = 'pkgs.ui.models.datastoreModel.' \
            'FloatArrayNode'
        self._IntDataCls = 'pkgs.ui.models.datastoreModel.IntData'
        self._IntNodeCls = 'pkgs.ui.models.datastoreModel.IntNode'
        self._IntArrayDataCls = 'pkgs.ui.models.datastoreModel.' \
            'IntArrayData'
        self._IntArrayNodeCls = 'pkgs.ui.models.datastoreModel.' \
            'IntArrayNode'
        self._MultiStateDataCls = 'pkgs.ui.models.datastoreModel.' \
            'MultiStateData'
        self._MultiStateNodeCls = 'pkgs.ui.models.datastoreModel.' \
            'MultiStateNode'
        self._UintDataCls = 'pkgs.ui.models.datastoreModel.UintData'
        self._UintNodeCls = 'pkgs.ui.models.datastoreModel.UintNode'
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
        data = Mock()
        node = Mock()
        list = Mock()
        with patch(self._ButtonDataCls) as mockedData, \
                patch(self._ButtonNodeCls) as mockedNode:
            mockedData.return_value = data
            mockedNode.return_value = node
            self._uut._appendButtonNode(list)
            mockedData.assert_called_once_with()
            mockedNode.assert_called_once_with(name, data)
            list.addChild.assert_called_once_with(node)

    def test_insertButtonNode(self) -> None:
        """
        The _insertButtonNode method must create a new button node and
        append it the given button list.
        """
        row = 3
        name = 'NEW_BUTTON'
        data = Mock()
        node = Mock()
        list = Mock()
        with patch(self._ButtonDataCls) as mockedData, \
                patch(self._ButtonNodeCls) as mockedNode:
            mockedData.return_value = data
            mockedNode.return_value = node
            self._uut._insertButtonNode(list, row)
            mockedData.assert_called_once_with()
            mockedNode.assert_called_once_with(name, data)
            list.addChildAt.assert_called_once_with(row, node)

    def test_appendButtonArrayNode(self) -> None:
        """
        The _appendButtonArrayNode method must create a new button array node
        and append it the given button array list.
        """
        name = 'NEW_BUTTON_ARRAY'
        data = Mock()
        node = Mock()
        list = Mock()
        with patch(self._ButtonArrayDataCls) as mockedData, \
                patch(self._ButtonArrayNodeCls) as mockedNode:
            mockedData.return_value = data
            mockedNode.return_value = node
            self._uut._appendButtonArrayNode(list)
            mockedData.assert_called_once_with()
            mockedNode.assert_called_once_with(name, data)
            list.addChild.assert_called_once_with(node)

    def test_insertButtonArrayNode(self) -> None:
        """
        The _insertButtonArrayNode method must create a new button array node
        and append it the given button array list.
        """
        row = 3
        name = 'NEW_BUTTON_ARRAY'
        data = Mock()
        node = Mock()
        list = Mock()
        with patch(self._ButtonArrayDataCls) as mockedData, \
                patch(self._ButtonArrayNodeCls) as mockedNode:
            mockedData.return_value = data
            mockedNode.return_value = node
            self._uut._insertButtonArrayNode(list, row)
            mockedData.assert_called_once_with()
            mockedNode.assert_called_once_with(name, data)
            list.addChildAt.assert_called_once_with(row, node)

    def test_appendFloatNode(self) -> None:
        """
        The _appendFloatNode method must create a new float node and append
        it the given float list.
        """
        name = 'NEW_FLOAT'
        data = Mock()
        node = Mock()
        list = Mock()
        with patch(self._FloatDataCls) as mockedData, \
                patch(self._FloatNodeCls) as mockedNode:
            mockedData.return_value = data
            mockedNode.return_value = node
            self._uut._appendFloatNode(list)
            mockedData.assert_called_once_with()
            mockedNode.assert_called_once_with(name, data)
            list.addChild.assert_called_once_with(node)

    def test_insertFloatNode(self) -> None:
        """
        The _insertFloatNode method must create a new float node and
        append it the given float list.
        """
        row = 3
        name = 'NEW_FLOAT'
        data = Mock()
        node = Mock()
        list = Mock()
        with patch(self._FloatDataCls) as mockedData, \
                patch(self._FloatNodeCls) as mockedNode:
            mockedData.return_value = data
            mockedNode.return_value = node
            self._uut._insertFloatNode(list, row)
            mockedData.assert_called_once_with()
            mockedNode.assert_called_once_with(name, data)
            list.addChildAt.assert_called_once_with(row, node)

    def test_appendFloatArrayNode(self) -> None:
        """
        The _appendFloatArrayNode method must create a new float array node and
        append it the given float array list.
        """
        name = 'NEW_FLOAT_ARRAY'
        data = Mock()
        node = Mock()
        list = Mock()
        with patch(self._FloatArrayDataCls) as mockedData, \
                patch(self._FloatArrayNodeCls) as mockedNode:
            mockedData.return_value = data
            mockedNode.return_value = node
            self._uut._appendFloatArrayNode(list)
            mockedData.assert_called_once_with()
            mockedNode.assert_called_once_with(name, data)
            list.addChild.assert_called_once_with(node)

    def test_insertFloatArrayNode(self) -> None:
        """
        The _insertFloatArrayNode method must create a new float array node and
        append it the given float array list.
        """
        row = 3
        name = 'NEW_FLOAT_ARRAY'
        data = Mock()
        node = Mock()
        list = Mock()
        with patch(self._FloatArrayDataCls) as mockedData, \
                patch(self._FloatArrayNodeCls) as mockedNode:
            mockedData.return_value = data
            mockedNode.return_value = node
            self._uut._insertFloatArrayNode(list, row)
            mockedData.assert_called_once_with()
            mockedNode.assert_called_once_with(name, data)
            list.addChildAt.assert_called_once_with(row, node)

    def test_appendIntNode(self) -> None:
        """
        The _appendIntNode method must create a new int node and append
        it the given int list.
        """
        name = 'NEW_INT'
        data = Mock()
        node = Mock()
        list = Mock()
        with patch(self._IntDataCls) as mockedData, \
                patch(self._IntNodeCls) as mockedNode:
            mockedData.return_value = data
            mockedNode.return_value = node
            self._uut._appendIntNode(list)
            mockedData.assert_called_once_with()
            mockedNode.assert_called_once_with(name, data)
            list.addChild.assert_called_once_with(node)

    def test_insertIntNode(self) -> None:
        """
        The _insertIntNode method must create a new int node and
        append it the given int list.
        """
        row = 3
        name = 'NEW_INT'
        data = Mock()
        node = Mock()
        list = Mock()
        with patch(self._IntDataCls) as mockedData, \
                patch(self._IntNodeCls) as mockedNode:
            mockedData.return_value = data
            mockedNode.return_value = node
            self._uut._insertIntNode(list, row)
            mockedData.assert_called_once_with()
            mockedNode.assert_called_once_with(name, data)
            list.addChildAt.assert_called_once_with(row, node)

    def test_appendIntArrayNode(self) -> None:
        """
        The _appendIntArrayNode method must create a new int array node and
        append it the given int array list.
        """
        name = 'NEW_INT_ARRAY'
        data = Mock()
        node = Mock()
        list = Mock()
        with patch(self._IntArrayDataCls) as mockedData, \
                patch(self._IntArrayNodeCls) as mockedNode:
            mockedData.return_value = data
            mockedNode.return_value = node
            self._uut._appendIntArrayNode(list)
            mockedData.assert_called_once_with()
            mockedNode.assert_called_once_with(name, data)
            list.addChild.assert_called_once_with(node)

    def test_insertIntArrayNode(self) -> None:
        """
        The _insertIntArrayNode method must create a new int array node and
        append it the given int array list.
        """
        row = 3
        name = 'NEW_INT_ARRAY'
        data = Mock()
        node = Mock()
        list = Mock()
        with patch(self._IntArrayDataCls) as mockedData, \
                patch(self._IntArrayNodeCls) as mockedNode:
            mockedData.return_value = data
            mockedNode.return_value = node
            self._uut._insertIntArrayNode(list, row)
            mockedData.assert_called_once_with()
            mockedNode.assert_called_once_with(name, data)
            list.addChildAt.assert_called_once_with(row, node)

    def test_appendMultiStateNode(self) -> None:
        """
        The _appendMultiStateNode method must create a new multi-state node and
        append it the given multi-state list.
        """
        name = 'NEW_MULTI_STATE'
        data = Mock()
        node = Mock()
        list = Mock()
        with patch(self._MultiStateDataCls) as mockedData, \
                patch(self._MultiStateNodeCls) as mockedNode:
            mockedData.return_value = data
            mockedNode.return_value = node
            self._uut._appendMultiStateNode(list)
            mockedData.assert_called_once_with()
            mockedNode.assert_called_once_with(name, data)
            list.addChild.assert_called_once_with(node)

    def test_insertMultiStateNode(self) -> None:
        """
        The _insertMultiStateNode method must create a new multi-state node and
        append it the given multi-state list.
        """
        row = 3
        name = 'NEW_MULTI_STATE'
        data = Mock()
        node = Mock()
        list = Mock()
        with patch(self._MultiStateDataCls) as mockedData, \
                patch(self._MultiStateNodeCls) as mockedNode:
            mockedData.return_value = data
            mockedNode.return_value = node
            self._uut._insertMultiStateNode(list, row)
            mockedData.assert_called_once_with()
            mockedNode.assert_called_once_with(name, data)
            list.addChildAt.assert_called_once_with(row, node)

    def test_appendUintNode(self) -> None:
        """
        The _appendUintNode method must create a new uint node and append
        it the given uint list.
        """
        name = 'NEW_UINT'
        data = Mock()
        node = Mock()
        list = Mock()
        with patch(self._UintDataCls) as mockedData, \
                patch(self._UintNodeCls) as mockedNode:
            mockedData.return_value = data
            mockedNode.return_value = node
            self._uut._appendUintNode(list)
            mockedData.assert_called_once_with()
            mockedNode.assert_called_once_with(name, data)
            list.addChild.assert_called_once_with(node)

    def test_insertUintNode(self) -> None:
        """
        The _insertUintNode method must create a new uint node and
        append it the given uint list.
        """
        row = 3
        name = 'NEW_UINT'
        data = Mock()
        node = Mock()
        list = Mock()
        with patch(self._UintDataCls) as mockedData, \
                patch(self._UintNodeCls) as mockedNode:
            mockedData.return_value = data
            mockedNode.return_value = node
            self._uut._insertUintNode(list, row)
            mockedData.assert_called_once_with()
            mockedNode.assert_called_once_with(name, data)
            list.addChildAt.assert_called_once_with(row, node)

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

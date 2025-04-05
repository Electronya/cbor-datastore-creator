from datetime import datetime
from freezegun import freeze_time
from unittest import TestCase
from unittest.mock import call, Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.models import DatastoreMetadata, DatastoreNode, NodeType   # noqa: E402 E501


class TestDatastoreNode(TestCase):
    """
    DatastoreNode test cases.
    """
    def setUp(self) -> None:
        """
        Test cases setup.
        """
        self._datetimeCls = 'pkgs.ui.models.datastoreNode.datetime'
        self._BaseNodeCls = 'pkgs.ui.models.datastoreNode.BaseNode'
        self._DatastoreNodeCls = 'pkgs.ui.models.datastoreNode.DatastoreNode'
        self._MetadataCls = 'pkgs.ui.models.datastoreNode.DatastoreMetadata'
        self._ObjectListNodeCls = 'pkgs.ui.models.datastoreNode.ObjectListNode'
        self._lastModifiedTimestamp = datetime.now()
        self._workingDir = '/path/to/store'
        self._root = Mock()
        metadata = DatastoreMetadata(self._lastModifiedTimestamp,
                                     workingDir=self._workingDir)
        self._uut = DatastoreNode('store', self._root, metadata)

    def test_constructorBaseClassInitAndSaveData(self) -> None:
        """
        The constructor must call the base class constructor with the right
        parameters and save the metadata.
        """
        root = Mock()
        name = 'test store'
        metadata = DatastoreMetadata(datetime.now(), '/path/to/store')
        with patch(f"{self._BaseNodeCls}.__init__") as mockedBaseNode:
            uut = DatastoreNode(name, root, metadata)
            mockedBaseNode.assert_called_once_with(name, NodeType.STORE,
                                                   parent=root)
            self.assertEqual(metadata, uut._metadata)

    def test_getLastModifiedAtReturnFormatted(self) -> None:
        """
        The getLastModifiedAt method must return the last modified date as a
        string with the dd/mm/yyyy HH:MM:SS.
        """
        modifiedAt = self._lastModifiedTimestamp.strftime('%d/%m/%Y %H:%M:%S')
        self.assertEqual(modifiedAt, self._uut.getLastModifiedAt())

    def test_setLastModifiedAtSaveNewDateFlagChanges(self) -> None:
        """
        The setLastModifiedAt method must save the new timestamp and flag the
        unsaved changes.
        """
        modifiedAt = datetime.now()
        self._uut.setLastModifiedAt(modifiedAt)
        self.assertEqual(modifiedAt, self._uut._metadata.lastModifiedAt)
        self.assertTrue(self._uut._metadata.hasUnsavedChanges)

    def test_hasUnsavedChanges(self) -> None:
        """
        The hasUnsavedChanges method must return true if the store has unsaved
        changes, false otherwise.
        """
        flags = [True, False]
        for flag in flags:
            self._uut._metadata.hasUnsavedChanges = flag
            self.assertEqual(flag, self._uut.hasUnsavedChanges())

    def test_clearUnsavedChangesFlag(self) -> None:
        """
        The clearUnsavedChangesFlag method must the clear the unsaved changes
        flag.
        """
        self._uut._metadata.hasUnsavedChanges = True
        self._uut.clearUnsavedChangesFlag()
        self.assertFalse(self._uut._metadata.hasUnsavedChanges)

    def test_getWorkingDirReturnWorkingDir(self) -> None:
        """
        The getWorkingDir method must return the store working directory.
        """
        self.assertEqual(self._workingDir, self._uut.getWorkingDir())

    @freeze_time('Jan 14th, 2025')
    def test_setWorkingDirSaveWorkingDir(self) -> None:
        """
        The setWorkingDir method must save the new working directory and update
        the store last modified timestamp.
        """
        workingDir = '/new/path/to/store'
        with patch.object(DatastoreNode, 'setLastModifiedAt') \
                as mockedLastModifiedAt:
            self._uut.setWorkingDir(workingDir)
            self.assertEqual(workingDir, self._uut._metadata.workingDir)
            mockedLastModifiedAt.assert_called_once_with(datetime(2025, 1, 14))

    @freeze_time('Jan 14th, 2025')
    def test_createNewStoreCreateStructure(self) -> None:
        """
        The createNewStore method must create all the empty object list nodes
        and return the datastore node.
        """
        root = Mock()
        storeMetadata = Mock()
        newStore = Mock()
        objectLists = []
        calls = []
        for type in NodeType:
            if type != NodeType.STORE and type != NodeType.OBJ_LIST:
                objectLists.append(Mock())
                calls.append(call(type.name, newStore))
        with patch(self._MetadataCls) as mockedStoreMetadata, \
                patch(self._DatastoreNodeCls) as mockedStoreNode, \
                patch(self._ObjectListNodeCls) as mockedObjListNode:
            mockedStoreMetadata.return_value = storeMetadata
            mockedStoreNode.return_value = newStore
            self.assertEqual(newStore, DatastoreNode.createNewStore(root))
            mockedStoreMetadata.assert_called_once_with(datetime(2025, 1, 14))
            mockedStoreNode.assert_called_once_with('datastore', root,
                                                    storeMetadata)
            mockedObjListNode.assert_has_calls(calls)

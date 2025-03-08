from datetime import datetime
from freezegun import freeze_time
from unittest import TestCase
from unittest.mock import Mock, patch

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
        self._lastModifiedTimestamp = datetime.now()
        self._workingDir = '/path/to/store'
        metadata = DatastoreMetadata(self._lastModifiedTimestamp,
                                     workingDir=self._workingDir)
        self._uut = DatastoreNode('store', metadata)

    def test_constructorSaveDataAddToParent(self) -> None:
        """
        The constructor must call the base class constructor with the right
        parameters and save the metadata.
        """
        name = 'test store'
        metadata = DatastoreMetadata(datetime.now(), '/path/to/store')
        with patch(f"{self._BaseNodeCls}.__init__") as mockedBaseNode:
            uut = DatastoreNode(name, metadata)
            mockedBaseNode.assert_called_once_with(name, NodeType.STORE)
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

from dataclasses import dataclass
from datetime import datetime
from .baseNode import BaseNode, NodeType


@dataclass
class DatastoreMetadata:
    lastModifiedAt: datetime
    hasUnsavedChanges: bool = False
    workingDir: str = '.'


class DatastoreNode(BaseNode):
    """
    The datastore tree node class.

    Param
        name: The node name.
        metadata: The datastore metadata.
    """
    def __init__(self, name: str, metadata: DatastoreMetadata) -> None:
        super().__init__(name, NodeType.STORE)
        self._metadata = metadata

    def getLastModifiedAt(self) -> str:
        """
        Get the store last modified timestamp.

        Return
            The formatted last modified timestamp.
        """
        return self._metadata.lastModifiedAt.strftime('%d/%m/%Y %H:%M:%S')

    def setLastModifiedAt(self, lastModifiedAt: datetime) -> None:
        """
        Set the last modified timestamp.

        Param
            lastModifiedAt: The last modified timestamp.
        """
        self._metadata.lastModifiedAt = lastModifiedAt
        self._metadata.hasUnsavedChanges = True

    def hasUnsavedChanges(self) -> bool:
        """
        Check if the store has unsaved changes.

        Return
            True if the store has unsaved changes, false otherwise.
        """
        return self._metadata.hasUnsavedChanges

    def clearUnsavedChangesFlag(self) -> None:
        """
        Clear the unsaved changes flag.
        """
        self._metadata.hasUnsavedChanges = False

    def getWorkingDir(self) -> str:
        """
        Get the store working directory.

        Return
            The store working directory.
        """
        return self._metadata.workingDir

    def setWorkingDir(self, workingDir: str) -> None:
        """
        Set the store working directory.

        Param
            workingDir: The working directory.
        """
        self._metadata.workingDir = workingDir
        self.setLastModifiedAt(datetime.now())

    @classmethod
    def createNew(cls) -> 'DatastoreNode':
        """
        Create a new datastore structure.

        Return
            The new datastore structure.
        """
        pass

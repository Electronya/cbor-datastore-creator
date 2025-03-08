from dataclasses import dataclass
from datetime import datetime
from .baseNode import BaseNode, NodeType
from .objectListNode import ObjectListNode


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
    def __init__(self, name: str, parent: BaseNode,
                 metadata: DatastoreMetadata) -> None:
        super().__init__(name, NodeType.STORE, parent=parent)
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
    def createNewStore(cls, root: BaseNode) -> 'DatastoreNode':
        """
        Create a new datastore structure.

        Param
            root: The datastore tree root node.

        Return
            The new datastore structure.
        """
        metadata = DatastoreMetadata(datetime.now())
        store = DatastoreNode('datastore', root, metadata)
        for type in NodeType:
            if type != NodeType.STORE or type != NodeType.OBJ_LIST:
                store.addChild(ObjectListNode(type.name, store))
        return store

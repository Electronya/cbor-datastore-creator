from PySide6 import QtCore as qtc

from ...datastore import Datastore


class DatastoreModel(qtc.QAbstractItemModel):
    """
    The datastore model class.
    """
    def __init__(self, datastore: Datastore, parent: qtc.QObject = None):
        qtc.QAbstractItemModel.__init__(parent)
        self._datastore = datastore

    def rowCount(self, parent: qtc.QModelIndex) -> int:
        """
        Get the row count.

        Param
            parent: the parent of the node.

        Return
            The row count of the node.
        """

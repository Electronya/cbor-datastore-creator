from unittest import TestCase
from unittest.mock import Mock, patch

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
        self._mockedDatastore = Mock()

    def test_constructorSetup(self) -> None:
        """
        The constructor must call the base class constructor and save the
        datastore.
        """
        parent = 10
        with patch(f"{self._QAbstractItemModelCls}.__init__") as mockedBaseCls:
            uut = DatastoreModel(self._mockedDatastore, parent=parent)
            mockedBaseCls.assert_called_once_with(parent)
        self.assertEqual(self._mockedDatastore, uut._datastore)

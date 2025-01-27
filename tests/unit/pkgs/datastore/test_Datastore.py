from datetime import date, datetime
from unittest import TestCase
from unittest.mock import ANY, call, Mock, patch
import cbor2
import yaml

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.datastore import (                  # noqa: E402
    Datastore,
    DatastoreData,
)


class TestDatastore(TestCase):
    """
    Datastore test cases.
    """
    def setUp(self) -> None:
        """
        Test cases set up.
        """
        self._ButtonCls = 'pkgs.datastore.datastore.Button'
        self._ButtonDataCls = 'pkgs.datastore.datastore.ButtonData'
        self._loggingMod = 'pkgs.datastore.datastore.logging'
        self._mockedLogger = Mock()
        testStoreFile = os.path.join('./tests/unit/pkgs/datastore',
                                     'testDatastore.yml')
        with open(testStoreFile, 'r') as storeFile:
            self._yml = yaml.safe_load(storeFile)
        data = DatastoreData('testDatastore', self._yml['lasModified'],
                             self._yml['workingDir'])
        with patch(self._loggingMod) as mockedLogging:
            mockedLogging.getLogger.return_value = self._mockedLogger
            self._uut = Datastore(data)

    def test_constructorGetLogger(self) -> None:
        """
        The constructor must get the datastore logger.
        """
        data = DatastoreData('testDatastore', self._yml['lasModified'],
                             self._yml['workingDir'])
        with patch(self._loggingMod) as mockedLogging:
            mockedLogging.getLogger.return_value = self._mockedLogger
            Datastore(data)
            mockedLogging.getLogger.assert_called_once_with('app.datastore')

    def test_constructorSaveData(self) -> None:
        """
        The constructor must save the datastore data and log its creation.
        """
        modifiedDate = datetime.strptime(self._yml['lasModified'],
                                         "%d-%m-%Y").date()
        data = DatastoreData('testDatastore', modifiedDate,
                             self._yml['workingDir'])
        logMsg = f"Datastore {data.name} created"
        mockedLogger = Mock()
        with patch(self._loggingMod) as mockedLogging:
            mockedLogging.getLogger.return_value = mockedLogger
            uut = Datastore(data)
            self.assertEqual(data, uut._data)
            mockedLogger.info.assert_called_once_with(logMsg)

    def test_parseCreateNewStore(self) -> None:
        """
        The parse class method must instantiate a new datastore based
        on the yaml encoding.
        """
        newStore = Datastore.parse(self._yml)
        self.assertEqual(self._uut._data, newStore._data)

    def test_populateButtonsCreateButtons(self) -> None:
        """
        The populateButtons method must populate the datastore buttons
        with the given data.
        """
        mockedData = Mock()
        calls = []
        for button in self._yml['buttons']:
            name = list(button.keys())[0]
            index = button[name]['index']
            longPressTime = button[name]['longPressTime']
            inactiveTime = button[name]['inactiveTime']
            calls.append(call(name, index, longPressTime, inactiveTime))
        self.assertEqual(0, len(self._uut._data.buttons))
        with patch(self._ButtonCls) as mockedButton, \
                patch(self._ButtonDataCls) as mockedButtonData:
            mockedButtonData.return_value = mockedData
            self._uut.populateButtons(self._yml['buttons'])
            self.assertEqual(len(self._yml['buttons']),
                             len(self._uut._data.buttons))
            self.assertEqual(len(self._yml['buttons']),
                             mockedButtonData.call_count)
            mockedButtonData.assert_has_calls(calls)
            mockedButton.assert_called_with(mockedData)

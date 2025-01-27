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
        self._ButtonArrayCls = 'pkgs.datastore.datastore.ButtonArray'
        self._ButtonArrayDataCls = 'pkgs.datastore.datastore.ButtonArrayData'
        self._ButtonArrayElmtCls = 'pkgs.datastore.datastore.ButtonArrayElement'    # noqa: E501
        self._FloatCls = 'pkgs.datastore.datastore.Float'
        self._FloatDataCls = 'pkgs.datastore.datastore.FloatData'
        self._FloatArrayCls = 'pkgs.datastore.datastore.FloatArray'
        self._FloatArrayDataCls = 'pkgs.datastore.datastore.FloatArrayData'
        self._FloatArrayElmtCls = 'pkgs.datastore.datastore.FloatArrayElement'
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

    def test_populateButtonArraysCreateArrays(self) -> None:
        """
        The populateButtonArrays method must populate the datastore button
        arrays with he given data.
        """
        mockedArrayData = Mock()
        elementCalls = []
        arrayDataCalls = []
        for array in self._yml['buttonArrays']:
            name = list(array.keys())[0]
            index = array[name]['index']
            longPressTime = array[name]['longPressTime']
            inactiveTime = array[name]['inactiveTime']
            for element in array[name]['elements']:
                elementCalls.append(call(element))
            arrayDataCalls.append(call(name, index, longPressTime,
                                       inactiveTime, ANY))
        self.assertEqual(0, len(self._uut._data.buttonArrays))
        with patch(self._ButtonArrayCls) as mockedButtonArray, \
                patch(self._ButtonArrayDataCls) as mockedData, \
                patch(self._ButtonArrayElmtCls) as mockedElement:
            mockedData.return_value = mockedArrayData
            self._uut.populateButtonArrays(self._yml['buttonArrays'])
            self.assertEqual(len(self._yml['buttonArrays']),
                             len(self._uut._data.buttonArrays))
            self.assertEqual(len(elementCalls), mockedElement.call_count)
            mockedElement.assert_has_calls(elementCalls)
            self.assertEqual(len(arrayDataCalls), mockedData.call_count)
            mockedData.assert_has_calls(arrayDataCalls)
            mockedButtonArray.assert_called_with(mockedArrayData)

    def test_populateFloatsCreateFloats(self) -> None:
        """
        The populateFloats method must populate the datastore floats
        with the given data.
        """
        mockedData = Mock()
        calls = []
        for floatObj in self._yml['floats']:
            name = list(floatObj.keys())[0]
            index = floatObj[name]['index']
            size = floatObj[name]['size']
            inNvm = floatObj[name]['inNvm']
            min = floatObj[name]['min']
            max = floatObj[name]['max']
            default = floatObj[name]['default']
            calls.append(call(name, index, size, min, max, default, inNvm))
        self.assertEqual(0, len(self._uut._data.floatObjs))
        with patch(self._FloatCls) as mockedFloat, \
                patch(self._FloatDataCls) as mockedFloatData:
            mockedFloatData.return_value = mockedData
            self._uut.populateFloats(self._yml['floats'])
            self.assertEqual(len(self._yml['floats']),
                             len(self._uut._data.floatObjs))
            self.assertEqual(len(self._yml['floats']),
                             mockedFloatData.call_count)
            mockedFloatData.assert_has_calls(calls)
            mockedFloat.assert_called_with(mockedData)

    def test_populateFloatArraysCreateArrays(self) -> None:
        """
        The populateFloatArrays method must populate the datastore float
        arrays with he given data.
        """
        mockedArrayData = Mock()
        elementCalls = []
        arrayDataCalls = []
        for array in self._yml['floatArrays']:
            name = list(array.keys())[0]
            index = array[name]['index']
            inNvm = array[name]['inNvm']
            for element in array[name]['elements']:
                elmtName = list(element.keys())[0]
                elmtMin = element[elmtName]['min']
                elmtMax = element[elmtName]['max']
                elmtDefault = element[elmtName]['default']
                elementCalls.append(call(elmtName, elmtMin,
                                         elmtMax, elmtDefault))
            arrayDataCalls.append(call(name, index, ANY, inNvm))
        self.assertEqual(0, len(self._uut._data.floatArrays))
        with patch(self._FloatArrayCls) as mockedFloatArray, \
                patch(self._FloatArrayDataCls) as mockedData, \
                patch(self._FloatArrayElmtCls) as mockedElement:
            mockedData.return_value = mockedArrayData
            self._uut.populateFloatArrays(self._yml['floatArrays'])
            self.assertEqual(len(self._yml['floatArrays']),
                             len(self._uut._data.floatArrays))
            self.assertEqual(len(elementCalls), mockedElement.call_count)
            mockedElement.assert_has_calls(elementCalls)
            self.assertEqual(len(arrayDataCalls), mockedData.call_count)
            mockedData.assert_has_calls(arrayDataCalls)
            mockedFloatArray.assert_called_with(mockedArrayData)

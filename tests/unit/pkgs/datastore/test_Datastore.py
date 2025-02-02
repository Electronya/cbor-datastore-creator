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
    def _initObjectLists(self):
        """
        Initialize the unit under test object lists.
        """
        self._mockedButtons = []
        for button in self._yml['buttons']:
            self._mockedButtons.append(Mock())
        self._mockedButtonArrays = []
        for buttonArray in self._yml['buttonArrays']:
            self._mockedButtonArrays.append(Mock())
        self._mockedFloats = []
        for floatObj in self._yml['floats']:
            self._mockedFloats.append(Mock())
        self._mockedFloatArrays = []
        for floatArray in self._yml['floatArrays']:
            self._mockedFloatArrays.append(Mock())
        self._mockedMultiStates = []
        for multiState in self._yml['multiStates']:
            self._mockedMultiStates.append(Mock())
        self._mockedSignedIntegers = []
        for signedInt in self._yml['signedIntegers']:
            self._mockedSignedIntegers.append(Mock())
        self._mockedIntArrays = []
        for intArray in self._yml['intArrays']:
            self._mockedIntArrays.append(Mock())
        self._mockedUnsignedIntegers = []
        for unsignedInt in self._yml['unsignedIntegers']:
            self._mockedUnsignedIntegers.append(Mock())
        self._mockedUintArrays = []
        for uintArray in self._yml['uintArrays']:
            self._mockedUintArrays.append(Mock())
        self._uut._data.buttons = self._mockedButtons
        self._uut._data.buttonArrays = self._mockedButtonArrays
        self._uut._data.floats = self._mockedFloats
        self._uut._data.floatArrays = self._mockedFloatArrays
        self._uut._data.multiStates = self._mockedMultiStates
        self._uut._data.signedIntegers = self._mockedSignedIntegers
        self._uut._data.intArrays = self._mockedIntArrays
        self._uut._data.unsignedIntegers = self._mockedUnsignedIntegers
        self._uut._data.uintArrays = self._mockedUintArrays

    def _deInitObjectLists(self):
        """
        De-initialize the unit under test object lists.
        """
        self._uut._data.buttons = []
        self._uut._data.buttonArrays = []
        self._uut._data.floats = []
        self._uut._data.floatArrays = []
        self._uut._data.multiStates = []
        self._uut._data.signedIntegers = []
        self._uut._data.intArrays = []
        self._uut._data.unsignedIntegers = []
        self._uut._data.uintArrays = []

    def setUp(self) -> None:
        """
        Test cases set up.
        """
        self._ButtonCls = 'pkgs.datastore.datastore.Button'
        self._ButtonDataCls = 'pkgs.datastore.datastore.ButtonData'
        self._ButtonArrayCls = 'pkgs.datastore.datastore.ButtonArray'
        self._ButtonArrayDataCls = 'pkgs.datastore.datastore.ButtonArrayData'
        self._ButtonArrayElmtCls = 'pkgs.datastore.datastore.ButtonArrayElement'        # noqa: E501
        self._FloatCls = 'pkgs.datastore.datastore.Float'
        self._FloatDataCls = 'pkgs.datastore.datastore.FloatData'
        self._FloatArrayCls = 'pkgs.datastore.datastore.FloatArray'
        self._FloatArrayDataCls = 'pkgs.datastore.datastore.FloatArrayData'
        self._FloatArrayElmtCls = 'pkgs.datastore.datastore.FloatArrayElement'
        self._MultiStateCls = 'pkgs.datastore.datastore.MultiState'
        self._MultiStateDataCls = 'pkgs.datastore.datastore.MultiStateData'
        self._SignedIntegerCls = 'pkgs.datastore.datastore.SignedInteger'
        self._SignedIntegerDataCls = 'pkgs.datastore.datastore.SignedIntegerData'       # noqa: E501
        self._IntArrayCls = 'pkgs.datastore.datastore.IntArray'
        self._IntArrayDataCls = 'pkgs.datastore.datastore.IntArrayData'
        self._IntArrayElementCls = 'pkgs.datastore.datastore.IntArrayElement'
        self._UnsignedIntegerCls = 'pkgs.datastore.datastore.UnsignedInteger'
        self._UnsignedIntegerDataCls = 'pkgs.datastore.datastore.UnsignedIntegerData'   # noqa: E501
        self._UintArrayCls = 'pkgs.datastore.datastore.UintArray'
        self._UintArrayDataCls = 'pkgs.datastore.datastore.UintArrayData'
        self._UintArrayElementCls = 'pkgs.datastore.datastore.UintArrayElement'
        self._loggingMod = 'pkgs.datastore.datastore.logging'
        self._mockedLogger = Mock()
        testStoreFile = os.path.join('./tests/unit/pkgs/datastore',
                                     'testDatastore.yml')
        with open(testStoreFile, 'r') as storeFile:
            self._yml = yaml.safe_load(storeFile)
            modifiedDate = datetime.strptime(self._yml['lasModified'],
                                             "%d-%m-%Y").date()
        data = DatastoreData('testDatastore', modifiedDate,
                             self._yml['workingDir'])
        with patch(self._loggingMod) as mockedLogging:
            mockedLogging.getLogger.return_value = self._mockedLogger
            self._uut = Datastore(data)
        self._initObjectLists()

    def test_constructorGetLogger(self) -> None:
        """
        The constructor must get the datastore logger.
        """
        modifiedDate = datetime.strptime(self._yml['lasModified'],
                                         "%d-%m-%Y").date()
        data = DatastoreData('testDatastore', modifiedDate,
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
        self._deInitObjectLists()
        newStore = Datastore.parse(self._yml)
        self.assertEqual(self._uut._data, newStore._data)

    def test_populateButtonsError(self) -> None:
        """
        The populateButtons method must raise any error raised by creating
        the buttons.
        """
        mockedData = Mock()
        errMsg = 'error message'
        with patch(self._ButtonCls) as mockedButton, \
                patch(self._ButtonDataCls) as mockedButtonData, \
                self.assertRaises(IndexError) as context:
            mockedButtonData.return_value = mockedData
            mockedButton.side_effect = IndexError(errMsg)
            self._uut.populateButtons(self._yml['buttons'])
            mockedButton.assert_called_once()
            self.assertEqual(errMsg, str(context.exception))

    def test_populateButtonsCreateButtons(self) -> None:
        """
        The populateButtons method must populate the datastore buttons
        with the given data.
        """
        self._deInitObjectLists()
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

    def test_populateButtonArraysError(self) -> None:
        """
        The populateButtonArrays method must raise any error raised by creating
        the button arrays.
        """
        mockedData = Mock()
        errMsg = 'error message'
        with patch(self._ButtonArrayCls) as mockedButtonArray, \
                patch(self._ButtonArrayDataCls) as mockedArrayData, \
                patch(self._ButtonArrayElmtCls), \
                self.assertRaises(IndexError) as context:
            mockedArrayData.return_value = mockedData
            mockedButtonArray.side_effect = IndexError(errMsg)
            self._uut.populateButtonArrays(self._yml['buttonArrays'])
            mockedButtonArray.assert_called_once()
            self.assertEqual(errMsg, str(context.exception))

    def test_populateButtonArraysCreateArrays(self) -> None:
        """
        The populateButtonArrays method must populate the datastore button
        arrays with he given data.
        """
        self._deInitObjectLists()
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

    def test_populateFloatsError(self) -> None:
        """
        The populateFloats method must raise any error raised by creating
        the floats.
        """
        mockedData = Mock()
        errMsg = 'error message'
        with patch(self._FloatCls) as mockedFloat, \
                patch(self._FloatDataCls) as mockedFloatData, \
                self.assertRaises(IndexError) as context:
            mockedFloatData.return_value = mockedData
            mockedFloat.side_effect = IndexError(errMsg)
            self._uut.populateFloats(self._yml['floats'])
            mockedFloat.assert_called_once()
            self.assertEqual(errMsg, str(context.exception))

    def test_populateFloatsCreateFloats(self) -> None:
        """
        The populateFloats method must populate the datastore floats
        with the given data.
        """
        self._deInitObjectLists()
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

    def test_populateFloatArraysError(self) -> None:
        """
        The populateFloatArrays method must raise any error raised by creating
        the float arrays.
        """
        mockedData = Mock()
        errMsg = 'error message'
        with patch(self._FloatArrayCls) as mockedFloatArray, \
                patch(self._FloatArrayDataCls) as mockedArrayData, \
                patch(self._FloatArrayElmtCls), \
                self.assertRaises(IndexError) as context:
            mockedArrayData.return_value = mockedData
            mockedFloatArray.side_effect = IndexError(errMsg)
            self._uut.populateFloatArrays(self._yml['floatArrays'])
            mockedFloatArray.assert_called_once()
            self.assertEqual(errMsg, str(context.exception))

    def test_populateFloatArraysCreateArrays(self) -> None:
        """
        The populateFloatArrays method must populate the datastore float
        arrays with he given data.
        """
        self._deInitObjectLists()
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

    def test_populateMultiStatesError(self) -> None:
        """
        The populateMultiStates method must raise any error raised by creating
        the multi-states.
        """
        mockedData = Mock()
        errMsg = 'error message'
        with patch(self._MultiStateCls) as mockedMultiState, \
                patch(self._MultiStateDataCls) as mockedMultiStateData, \
                self.assertRaises(IndexError) as context:
            mockedMultiStateData.return_value = mockedData
            mockedMultiState.side_effect = IndexError(errMsg)
            self._uut.populateMultiStates(self._yml['multiStates'])
            mockedMultiState.assert_called_once()
            self.assertEqual(errMsg, str(context.exception))

    def test_populateMultiStatesCreateMultiStates(self) -> None:
        """
        The populateMultiStates method must populate the datastore multi-states
        with the given data.
        """
        self._deInitObjectLists()
        mockedData = Mock()
        calls = []
        for multiState in self._yml['multiStates']:
            name = list(multiState.keys())[0]
            index = multiState[name]['index']
            inNvm = multiState[name]['inNvm']
            states = multiState[name]['states']
            default = multiState[name]['default']
            calls.append(call(name, index, states, default, inNvm))
        self.assertEqual(0, len(self._uut._data.multiStates))
        with patch(self._MultiStateCls) as mockedMultiState, \
                patch(self._MultiStateDataCls) as mockedMultiStateData:
            mockedMultiStateData.return_value = mockedData
            self._uut.populateMultiStates(self._yml['multiStates'])
            self.assertEqual(len(self._yml['multiStates']),
                             len(self._uut._data.multiStates))
            self.assertEqual(len(self._yml['multiStates']),
                             mockedMultiStateData.call_count)
            mockedMultiStateData.assert_has_calls(calls)
            mockedMultiState.assert_called_with(mockedData)

    def test_populateSignedIntegersError(self) -> None:
        """
        The populateSignedIntegers method must raise any error raised by
        creating the signed integers.
        """
        mockedData = Mock()
        errMsg = 'error message'
        with patch(self._SignedIntegerCls) as mockedSignedInteger, \
                patch(self._SignedIntegerDataCls) as mockedSignedIntegerData, \
                self.assertRaises(IndexError) as context:
            mockedSignedIntegerData.return_value = mockedData
            mockedSignedInteger.side_effect = IndexError(errMsg)
            self._uut.populateSignedIntegers(self._yml['signedIntegers'])
            mockedSignedInteger.assert_called_once()
            self.assertEqual(errMsg, str(context.exception))

    def test_populateSignedIntegersCreateSignedIntegers(self) -> None:
        """
        The populateSignedIntegers method must populate the datastore
        signed integers with the given data.
        """
        self._deInitObjectLists()
        mockedData = Mock()
        calls = []
        for signedInteger in self._yml['signedIntegers']:
            name = list(signedInteger.keys())[0]
            index = signedInteger[name]['index']
            size = signedInteger[name]['size']
            inNvm = signedInteger[name]['inNvm']
            min = signedInteger[name]['min']
            max = signedInteger[name]['max']
            default = signedInteger[name]['default']
            calls.append(call(name, index, size, min, max, default, inNvm))
        self.assertEqual(0, len(self._uut._data.signedIntegers))
        with patch(self._SignedIntegerCls) as mockedSignedInteger, \
                patch(self._SignedIntegerDataCls) as mockedSignedIntegerData:
            mockedSignedIntegerData.return_value = mockedData
            self._uut.populateSignedIntegers(self._yml['signedIntegers'])
            self.assertEqual(len(self._yml['signedIntegers']),
                             len(self._uut._data.signedIntegers))
            self.assertEqual(len(self._yml['signedIntegers']),
                             mockedSignedIntegerData.call_count)
            mockedSignedIntegerData.assert_has_calls(calls)
            mockedSignedInteger.assert_called_with(mockedData)

    def test_populateIntArraysError(self) -> None:
        """
        The populateIntArrays method must raise any error raised by
        creating the signed integer arrays.
        """
        mockedData = Mock()
        errMsg = 'error message'
        with patch(self._IntArrayCls) as mockedIntArray, \
                patch(self._IntArrayDataCls) as mockedArrayData, \
                patch(self._IntArrayElementCls), \
                self.assertRaises(IndexError) as context:
            mockedArrayData.return_value = mockedData
            mockedIntArray.side_effect = IndexError(errMsg)
            self._uut.populateIntArrays(self._yml['intArrays'])
            mockedIntArray.assert_called_once()
            self.assertEqual(errMsg, str(context.exception))

    def test_populateIntArraysCreateArrays(self) -> None:
        """
        The populateIntArrays method must populate the datastore int
        arrays with he given data.
        """
        self._deInitObjectLists()
        mockedArrayData = Mock()
        elementCalls = []
        arrayDataCalls = []
        for array in self._yml['intArrays']:
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
        self.assertEqual(0, len(self._uut._data.intArrays))
        with patch(self._IntArrayCls) as mockedIntArray, \
                patch(self._IntArrayDataCls) as mockedData, \
                patch(self._IntArrayElementCls) as mockedElement:
            mockedData.return_value = mockedArrayData
            self._uut.populateIntArrays(self._yml['intArrays'])
            self.assertEqual(len(self._yml['intArrays']),
                             len(self._uut._data.intArrays))
            self.assertEqual(len(elementCalls), mockedElement.call_count)
            mockedElement.assert_has_calls(elementCalls)
            self.assertEqual(len(arrayDataCalls), mockedData.call_count)
            mockedData.assert_has_calls(arrayDataCalls)
            mockedIntArray.assert_called_with(mockedArrayData)

    def test_populateUnsignedIntegersError(self) -> None:
        """
        The populateUnsignedIntegers method must raise any error raised by
        creating the signed integers.
        """
        mockedData = Mock()
        errMsg = 'error message'
        with patch(self._UnsignedIntegerCls) as mockedUnsignedInteger, \
                patch(self._UnsignedIntegerDataCls) as mockedUintData, \
                self.assertRaises(IndexError) as context:
            mockedUintData.return_value = mockedData
            mockedUnsignedInteger.side_effect = IndexError(errMsg)
            self._uut.populateUnsignedIntegers(self._yml['unsignedIntegers'])
            mockedUnsignedInteger.assert_called_once()
            self.assertEqual(errMsg, str(context.exception))

    def test_populateUnsignedIntegersCreateUnsignedIntegers(self) -> None:
        """
        The populateUnsignedIntegers method must populate the datastore
        unsigned integers with the given data.
        """
        self._deInitObjectLists()
        mockedData = Mock()
        calls = []
        for signedInteger in self._yml['unsignedIntegers']:
            name = list(signedInteger.keys())[0]
            index = signedInteger[name]['index']
            size = signedInteger[name]['size']
            inNvm = signedInteger[name]['inNvm']
            min = signedInteger[name]['min']
            max = signedInteger[name]['max']
            default = signedInteger[name]['default']
            calls.append(call(name, index, size, min, max, default, inNvm))
        self.assertEqual(0, len(self._uut._data.unsignedIntegers))
        with patch(self._UnsignedIntegerCls) as mockedUnsignedInteger, \
                patch(self._UnsignedIntegerDataCls) as mockedUnsignedIntegerData:       # noqa: E501
            mockedUnsignedIntegerData.return_value = mockedData
            self._uut.populateUnsignedIntegers(self._yml['unsignedIntegers'])
            self.assertEqual(len(self._yml['unsignedIntegers']),
                             len(self._uut._data.unsignedIntegers))
            self.assertEqual(len(self._yml['unsignedIntegers']),
                             mockedUnsignedIntegerData.call_count)
            mockedUnsignedIntegerData.assert_has_calls(calls)
            mockedUnsignedInteger.assert_called_with(mockedData)

    def test_populateUintArraysError(self) -> None:
        """
        The populateUintArrays method must raise any error raised by
        creating the signed integer arrays.
        """
        mockedData = Mock()
        errMsg = 'error message'
        with patch(self._UintArrayCls) as mockedUintArray, \
                patch(self._UintArrayDataCls) as mockedArrayData, \
                patch(self._UintArrayElementCls), \
                self.assertRaises(IndexError) as context:
            mockedArrayData.return_value = mockedData
            mockedUintArray.side_effect = IndexError(errMsg)
            self._uut.populateUintArrays(self._yml['uintArrays'])
            mockedUintArray.assert_called_once()
            self.assertEqual(errMsg, str(context.exception))

    def test_populateUintArraysCreateArrays(self) -> None:
        """
        The populateUintArrays method must populate the datastore int
        arrays with he given data.
        """
        self._deInitObjectLists()
        mockedArrayData = Mock()
        elementCalls = []
        arrayDataCalls = []
        for array in self._yml['uintArrays']:
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
        self.assertEqual(0, len(self._uut._data.uintArrays))
        with patch(self._UintArrayCls) as mockedUintArray, \
                patch(self._UintArrayDataCls) as mockedData, \
                patch(self._UintArrayElementCls) as mockedElement:
            mockedData.return_value = mockedArrayData
            self._uut.populateUintArrays(self._yml['uintArrays'])
            self.assertEqual(len(self._yml['uintArrays']),
                             len(self._uut._data.uintArrays))
            self.assertEqual(len(elementCalls), mockedElement.call_count)
            mockedElement.assert_has_calls(elementCalls)
            self.assertEqual(len(arrayDataCalls), mockedData.call_count)
            mockedData.assert_has_calls(arrayDataCalls)
            mockedUintArray.assert_called_with(mockedArrayData)

    def test_getNameReturnName(self) -> None:
        """
        The getName method must return the datastore name.
        """
        names = ['datastore_1, datastore_2']
        for name in names:
            self._uut._data.name = name
            self.assertEqual(name, self._uut.getName())

    def test_setNameSaveNewName(self) -> None:
        """
        The setName method must save the new datastore name.
        """
        names = ['datastore_1, datastore_2']
        for name in names:
            self._uut.setName(name)
            self.assertEqual(name, self._uut._data.name)

    def test_getLastModifiedReturnDate(self) -> None:
        """
        The getLastModified method must return the last modified date
        as a string with the format dd-mm-yyyy.
        """
        dates = ['29-01-2025', '01-02-2025']
        for dateStr in dates:
            self._uut._data.lastModified = datetime \
                .strptime(dateStr, '%d-%m-%Y').date()
            self.assertEqual(dateStr, self._uut.getLastModified())

    def test_setLastModifiedSaveDate(self) -> None:
        """
        The setLastModified method must save the new last modified date
        from a string with the format dd-mm-yyyy.
        """
        dates = ['29-01-2025', '01-02-2025']
        for dateStr in dates:
            lastModified = datetime.strptime(dateStr, '%d-%m-%Y').date()
            self._uut.setLastModified(dateStr)
            self.assertEqual(lastModified, self._uut._data.lastModified)

    def test_getWorkingDirReturnWorkingDir(self) -> None:
        """
        The getWorkingDir must return the datastore working directory.
        """
        dirs = ['/home/testDir1/workingDir1', '/home/testDir2/workingDir2']
        for dir in dirs:
            self._uut._data.workingDir = dir
            self.assertEqual(dir, self._uut.getWorkingDir())

    def test_setWorkingDirSaveNewWorkingDir(self) -> None:
        """
        The setWorkingDir must save the datastore new working directory.
        """
        dirs = ['/home/testDir1/workingDir1', '/home/testDir2/workingDir2']
        for dir in dirs:
            self._uut.setWorkingDir(dir)
            self.assertEqual(dir, self._uut._data.workingDir)

    def test_getButtonsReturnButtons(self) -> None:
        """
        The getButtons method must return the datastore list of buttons.
        """
        buttons = self._uut.getButtons()
        self.assertEqual(self._uut._data.buttons, buttons)

    def test_getButtonAtIndexOutOfBound(self) -> None:
        """
        The getButtonAtIndex must raise an index error if the requested
        index is out of bound.
        """
        index = 4
        errMsg = f"No button at index {index}"
        with self.assertRaises(IndexError) as context:
            self._uut.getButtonAtIndex(index)
            self._mockedLogger.error.assert_Called_once_with(errMsg)
            self.assertEqual(errMsg, str(context.exception))

    def test_getButtonAtIndexReturnButton(self) -> None:
        """
        The getButtonAtIndex must return the button at the given index.
        """
        indexes = [0, 1]
        for index in indexes:
            button = self._uut.getButtonAtIndex(index)
            self.assertEqual(self._uut._data.buttons[index], button)

    def test_appendButtonSaveNewButton(self) -> None:
        """
        The appendButton method must append the new button to the
        datastore button list.
        """
        button = Mock()
        self.assertEqual(len(self._yml['buttons']),
                         len(self._uut._data.buttons))
        self._uut.appendButton(button)
        self.assertEqual(len(self._yml['buttons']) + 1,
                         len(self._uut._data.buttons))
        self.assertEqual(button, self._uut._data.buttons[-1])

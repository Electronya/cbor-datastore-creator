from unittest import TestCase
from unittest.mock import Mock, patch
import cbor2
import yaml

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.objects import (                  # noqa: E402
    ButtonState,
    ButtonStateData,
    TimeError,
)


class TestButtonState(TestCase):
    """
    ButtonState test cases.
    """
    def setUp(self) -> None:
        """
        Test cases set up.
        """
        self._loggingMod = 'pkgs.objects.buttonState.logging'
        self._mockedLogger = Mock()
        objectData = ButtonStateData('testObject', 1, 4000, 5000)
        with patch(self._loggingMod) as mockedLogging:
            mockedLogging.getLogger.return_value = self._mockedLogger
            self._uut = ButtonState(objectData)
        objectDict = {
            objectData.name: {
                'index': objectData.index,
                'longPressTime': objectData.longPressTime,
                'isLongPress': objectData.isLongPress,
                'inactiveTime': objectData.inactiveTime,
                'isInactive': objectData.isInactive,
                'state': objectData.state.name,
            }
        }
        self._ymlString = yaml.dump(objectDict)
        objectDict = {
            'id': ButtonState.BASE_ID | objectData.index,
            'longPressTime': objectData.longPressTime,
            'isLongPress': objectData.isLongPress,
            'inactiveTime': objectData.inactiveTime,
            'isInactive': objectData.isInactive,
            'state': objectData.state.value,
        }
        self._cborEncoding = cbor2.dumps(objectDict)

    def test_constructorInvalidIndex(self) -> None:
        """
        The constructor must raise an index error if the object index is not
        valid.
        """
        objectData = ButtonStateData("testObject", 256)
        errMsg = f"Cannot create object {objectData.name}: Invalid index " \
            f"({objectData.index})"
        with patch(self._loggingMod) as mockedLogging, \
                self.assertRaises(IndexError) as context:
            mockedLogging.getLogger.return_value = self._mockedLogger
            ButtonState(objectData)
            self._mockedLogger.error.assert_called_once_with(errMsg)
            self.assertEqual(errMsg, str(context.exception))

    def test_constructorInvalidLongPressTime(self) -> None:
        """
        The constructor must raise a time error if the long press time used to
        initialize the object is invalid.
        """
        objectData = ButtonStateData('testObject', 1, 65536, 5000)
        errMsg = f"Cannot create object {objectData.name}: Invalid long " \
            f"press time ({objectData.longPressTime})"
        with patch(self._loggingMod) as mockedLogging, \
                self.assertRaises(TimeError) as context:
            mockedLogging.getLogger.return_value = self._mockedLogger
            ButtonState(objectData)
            self._mockedLogger.error.assert_called_once_with(errMsg)
            self.assertEqual(errMsg, str(context.exception))

    def test_constructorInvalidInactiveTime(self) -> None:
        """
        The constructor must raise a time error if the inactive time used to
        initialize the object is invalid.
        """
        objectData = ButtonStateData('testObject', 1, 6000, 999)
        errMsg = f"Cannot create object {objectData.name}: Invalid inactive " \
            f"time ({objectData.inactiveTime})"
        with patch(self._loggingMod) as mockedLogging, \
                self.assertRaises(TimeError) as context:
            mockedLogging.getLogger.return_value = self._mockedLogger
            ButtonState(objectData)
            self._mockedLogger.error.assert_called_once_with(errMsg)
            self.assertEqual(errMsg, str(context.exception))

    def test_constructorGetLogger(self) -> None:
        """
        The constructor must get the uint logger.
        """
        objectData = ButtonStateData("testObject", 1)
        with patch(self._loggingMod) as mockedLogging:
            ButtonState(objectData)
            mockedLogging.getLogger.assert_called_once_with('app.objects.uint')

    def test_constructorSaveObjectData(self) -> None:
        """
        The constructor must save the object data.
        """
        objectData = ButtonStateData("testObject", 1)
        with patch(self._loggingMod):
            testObject = ButtonState(objectData)
        self.assertEqual(objectData, testObject._data)

    def test__isIndexValid(self) -> None:
        """
        The _isIndexValid method must return true when the index is valid,
        false otherwise. To be valid the index must be between 1 and 255.
        """
        # test values: (index, result)
        testValues = [(256, False), (0, False), (1, True), (255, True)]
        for values in testValues:
            self.assertEqual(values[1], self._uut._isIndexValid(values[0]))

    def test__isTimeValidReturnValue(self) -> None:
        """
        The _isTimeValid method must return true when the time is valid and
        false otherwise. To be valid the time must be greater or equal to 1000
        and less than 65536.
        """
        # test values: (time, result)
        testValues = [(65536, False), (65535, True),
                      (999, False), (1000, True)]
        for values in testValues:
            self.assertEqual(values[1], self._uut._isTimeValid(values[0]))

    def test_getNameReturnName(self) -> None:
        """
        The getName method must return the object name.
        """
        names = ['name1', "name2"]
        for name in names:
            self._uut._data.name = name
            self.assertEqual(name, self._uut.getName())

    def test_setNameSaveName(self) -> None:
        """
        The setName method must save the object name.
        """
        names = ['name1', "name2"]
        for name in names:
            self._uut.setName(name)
            self.assertEqual(name, self._uut._data.name)

    def test_getIdReturnId(self) -> None:
        """
        The getId method must return the object ID.
        """
        indexes = [1, 2]
        for index in indexes:
            self._uut._data.index = index
            self.assertEqual(ButtonState.BASE_ID | index,
                             self._uut.getId())

    def test_getIndexReturnIndex(self) -> None:
        """
        The getIndex method must return the object index based on its ID.
        """
        indexes = [1, 2]
        for index in indexes:
            self._uut._data.index = index
            self.assertEqual(index, self._uut.getIndex())

    def test_setIndexOutOfRange(self) -> None:
        """
        The setIndex method must raise an index error when the give index is
        out of range.
        """
        objectIndexes = [0x0100, 0xffff, -1, -13]
        errMsg = 'Index out of range'
        for index in objectIndexes:
            with self.assertRaises(IndexError) as context:
                self._uut.setIndex(index)
                self.assertEqual(errMsg, str(context.exception))

    def test_setIndexSaveNewObjectId(self) -> None:
        """
        The setIndex method must save the new object ID based on the new index.
        """
        objectIndexes = [1, 255]
        for index in objectIndexes:
            self._uut.setIndex(index)
            self.assertEqual(index, self._uut._data.index)

    def test_getLongPressTimeReturnLongPressTime(self) -> None:
        """
        The getLongPressTime method must return the object longPressTime.
        """
        objectTimes = [3000, 6000]
        for time in objectTimes:
            self._uut._data.longPressTime = time
            self.assertEqual(time, self._uut.getLongPressTime())

    def test_setLongPressTimeRaiseTimeError(self) -> None:
        """
        The setLongPressTime method must raise a time error if the given time
        is invalid.
        """
        objectTimes = [999, 65536]
        for time in objectTimes:
            errMsg = f"A long press time of {time}ms is invalid"
            with self.assertRaises(TimeError) as context:
                self._uut.setLongPressTime(time)
                self.assertEqual(errMsg, str(context.exception))

    def test_setLongPressTimeSaveNewLongPressTime(self) -> None:
        """
        The setLongPressTime method must save the new object long press time.
        """
        objectTimes = [1000, 8000]
        for time in objectTimes:
            self._uut.setLongPressTime(time)
            self.assertEqual(time, self._uut._data.longPressTime)

    def test_setInactiveTimeRaiseTimeError(self) -> None:
        """
        The setInactiveTime method must raise a time error if the given time
        is invalid.
        """
        objectTimes = [999, 65536]
        for time in objectTimes:
            errMsg = f"An inactive time of {time}ms is invalid"
            with self.assertRaises(TimeError) as context:
                self._uut.setInactiveTime(time)
                self.assertEqual(errMsg, str(context.exception))

    def test_setInactiveTimeSaveNewInactiveTime(self) -> None:
        """
        The setInactiveTime method must save the new object inactive time.
        """
        objectTimes = [1000, 8000]
        for time in objectTimes:
            self._uut.setInactiveTime(time)
            self.assertEqual(time, self._uut._data.inactiveTime)

    def test_getYamlStringReturnYamlString(self) -> None:
        """
        The getYamlString must return the object yaml encoding as a string.
        """
        string = self._uut.getYamlString()
        self.assertEqual(self._ymlString, string)

    def test_encodeCborReturnEncoded(self) -> None:
        """
        The encodeCbor method must return the object encoded in CBOR format.
        """
        encoding = self._uut.encodeCbor()
        self.assertEqual(self._cborEncoding, encoding)

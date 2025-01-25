from unittest import TestCase
from unittest.mock import Mock, patch
import cbor2
import yaml

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.objects import (                  # noqa: E402
    LimitError,
    SizeError,
    Float,
    FloatData
)


class TestFloat(TestCase):
    """
    Float test cases.
    """
    def setUp(self) -> None:
        """
        Test cases set up.
        """
        self._loggingMod = 'pkgs.objects.floatObject.logging'
        self._mockedLogger = Mock()
        objectData = FloatData('testObject', 1, 4, -128.5, 128.5, 32.0)
        with patch(self._loggingMod) as mockedLogging:
            mockedLogging.getLogger.return_value = self._mockedLogger
            self._uut = Float(objectData)
        objectDict = {
            objectData.name: {
                'index': objectData.index,
                'size': objectData.size,
                'min': objectData.min,
                'max': objectData.max,
                'default': objectData.default,
                'inNvm': objectData.inNvm,
            }
        }
        self._ymlString = yaml.dump(objectDict)
        objectDict = {
            'id': Float.BASE_ID | objectData.index,
            'size': objectData.size,
            'min': objectData.min,
            'max': objectData.max,
            'default': objectData.default,
            'inNvm': objectData.inNvm,
        }
        self._cborEncoding = cbor2.dumps(objectDict)

    def test_constructorInvalidIndex(self) -> None:
        """
        The constructor must raise an index error if the object index is not
        valid.
        """
        objectData = FloatData("testObject", 256)
        errMsg = f"Cannot create object {objectData.name}: Invalid index " \
            f"({objectData.index})"
        with patch(self._loggingMod) as mockedLogging, \
                self.assertRaises(IndexError) as context:
            mockedLogging.getLogger.return_value = self._mockedLogger
            Float(objectData)
            self._mockedLogger.error.assert_called_once_with(errMsg)
            self.assertEqual(errMsg, str(context.exception))

    def test_constructorInvalidSize(self) -> None:
        """
        The constructor must raise a size error if the size used to initialize
        the object is invalid.
        """
        objectData = FloatData("testObject", 1, 3, 0.0, 255.0, 32.0)
        errMsg = f"Cannot create object {objectData.name}: Invalid size " \
            f"({objectData.size})"
        with patch(self._loggingMod) as mockedLogging, \
                self.assertRaises(SizeError) as context:
            mockedLogging.getLogger.return_value = self._mockedLogger
            Float(objectData)
            self._mockedLogger.error.assert_called_once_with(errMsg)
            self.assertEqual(errMsg, str(context.exception))

    def test_constructorInvalidLimits(self) -> None:
        """
        The constructor must raise a limit error if the limits used to
        initialize the object are invalid.
        """
        objectData = FloatData("testObject", 1, 4, 1.0, -1.0, 0.0)
        errMsg = f"Cannot create object {objectData.name}: Invalid min " \
            f"({objectData.min}) or max ({objectData.max})"
        with patch(self._loggingMod) as mockedLogging, \
                self.assertRaises(LimitError) as context:
            mockedLogging.getLogger.return_value = self._mockedLogger
            Float(objectData)
            self._mockedLogger.error.assert_called_once_with(errMsg)
            self.assertEqual(errMsg, str(context.exception))

    def test_constructorInvalidDefault(self) -> None:
        """
        The constructor must raise a limit error if the default value used to
        initialize the object is invalid.
        """
        objectData = FloatData("testObject", 1, 8, -128.0, 127.0, 128.0)
        errMsg = f"Cannot create object {objectData.name}: Invalid default " \
            f"({objectData.default})"
        with patch(self._loggingMod) as mockedLogging, \
                self.assertRaises(LimitError) as context:
            mockedLogging.getLogger.return_value = self._mockedLogger
            Float(objectData)
            self._mockedLogger.error.assert_called_once_with(errMsg)
            self.assertEqual(errMsg, str(context.exception))

    def test_constructorGetLogger(self) -> None:
        """
        The constructor must get the float logger.
        """
        objectData = FloatData("testObject", 1)
        with patch(self._loggingMod) as mockedLogging:
            Float(objectData)
            mockedLogging.getLogger.assert_called_once_with('app.objects.'
                                                            'float')

    def test_constructorSaveObjectData(self) -> None:
        """
        The constructor must save the object data.
        """
        objectData = FloatData("testObject", 1)
        with patch(self._loggingMod):
            testObject = Float(objectData)
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

    def test__isSizeValidReturnValue(self) -> None:
        """
        The _isSizeValid method must return true when the size is valid and
        false otherwise. To be valid the size must either 1, 2, 4 or 8.
        """
        results = [False, False, False, True, False, False, False, True, False]
        for idx, result in enumerate(results):
            size = idx + 1
            self.assertEqual(result, self._uut._isSizeValid(size))

    def test__areLimitsValidReturnValue(self) -> None:
        """
        The _areLimitsValid method return true when the limits are valid and
        false otherwise. to be valid the minimum must be less than the maximum.
        """
        # test values: (min, max, result)
        testValues = [(129.0, 127.0, False), (0, 128, True),
                      (-32766.0, -32767.0, False), (-32768, 32768, True)]
        for values in testValues:
            self.assertEqual(values[2], self._uut._areLimitsValid(values[0],
                                                                  values[1]))

    def test__isDefaultValidReturnValue(self) -> None:
        """
        The _isDefaultValid method must return true when the default is valid
        and false otherwise. To be valid the default value must between the
        minimum and maximum, included.
        """
        # test values: (min, max, default, result)
        testValues = [(-128.0, 127.0, -129.0, False),
                      (-128.0, 127.0, 128.0, False),
                      (-128.0, 127.0, -128.0, True),
                      (-128.0, 127.0, 127.0, True)]
        for values in testValues:
            self.assertEqual(values[3], self._uut._isDefaultValid(values[0],
                                                                  values[1],
                                                                  values[2]))

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
            self.assertEqual(Float.BASE_ID | index,
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

    def test_getSizeReturnSize(self) -> None:
        """
        The getSize method must return the object size.
        """
        objectSizes = [1, 2]
        for size in objectSizes:
            self._uut._data.size = size
            self.assertEqual(size, self._uut.getSize())

    def test_setSizeRaiseSizeError(self) -> None:
        """
        The setSize method must raise a size error if the given size is
        supported.
        """
        objectSizes = [1, 2, 3, 5, 6, 7, 9]
        for size in objectSizes:
            errMsg = f"A {size} bytes is not supported"
            with self.assertRaises(SizeError) as context:
                self._uut.setSize(size)
                self.assertEqual(errMsg, str(context.exception))

    def test_setSizeSaveNewObjectSave(self) -> None:
        """
        The setSize method must save the new object size.
        """
        objectSizes = [4, 8]
        for size in objectSizes:
            self._uut.setSize(size)
            self.assertEqual(size, self._uut._data.size)

    def test_getMinReturnMin(self) -> None:
        """
        The getMin method must return the object minimum value.
        """
        objectMinimums = [1.2, 50.5, 0.0]
        for min in objectMinimums:
            self._uut._data.min = min
            self.assertEqual(min, self._uut.getMin())

    def test_getMaxReturnMax(self) -> None:
        """
        The getMax method must return the object maximum value.
        """
        objectMaximums = [127.3, 100.8, 75.12]
        for max in objectMaximums:
            self._uut._data.max = max
            self.assertEqual(max, self._uut.getMax())

    def test_setLimitsRaiseLimitError(self) -> None:
        """
        The setLimits method must raise a limit error if the given limits are
        invalid.
        """
        # Limits: (min, max)
        objectLimits = [(3, 1), (-120, -127)]
        for limits in objectLimits:
            errMsg = f"A min of {limits[0]} or a max of " \
                     f"{limits[1]} is not valid"
            with self.assertRaises(LimitError) as context:
                self._uut.setLimits(limits[0], limits[1])
                self.assertEqual(errMsg, str(context.exception))

    def test_setLimitsSaveLimits(self) -> None:
        """
        The setLimits method must save the new limits.
        """
        # Limits: (min, max)
        objectLimits = [(-128.1, 127.9), (10.2, 15.8),
                        (-30.3, 75.7), (-10.5, 100.6)]
        for limits in objectLimits:
            self._uut.setLimits(limits[0], limits[1])
            self.assertEqual(limits[0], self._uut._data.min)
            self.assertEqual(limits[1], self._uut._data.max)

    def test_getDefaultReturnDefault(self) -> None:
        """
        The getDefault method must return the object default value.
        """
        objectDefaultValues = [127.4, 100.7, 75.2]
        for defaultVal in objectDefaultValues:
            self._uut._data.default = defaultVal
            self.assertEqual(defaultVal, self._uut.getDefault())

    def test_setDefaultRaiseLimitError(self) -> None:
        """
        The setDefault method must raise a limit error if the default value is
        outside of the limits.
        """
        # test values: (min, max, default)
        testValues = [(0.0, 127.9, 128.1), (-128.9, 15.5, -129.4),
                      (30.3, 100.7, 255), (10.5, 150.2, 0.4)]
        for values in testValues:
            errMsg = f"A value of {values[2]} is outside of the " \
                     f"{values[0]} minimum and {values[1]} maximum"
            self._uut._data.min = values[0]
            self._uut._data.max = values[1]
            with self.assertRaises(LimitError) as context:
                self._uut.setDefault(values[2])
                self.assertEqual(errMsg, str(context.exception))

    def test_setDefaultSaveDefault(self) -> None:
        """
        The setDefault method must save the object default value.
        """
        objectDefaultValues = [127.6, -128.4, 75.4]
        for defaultVal in objectDefaultValues:
            self._uut.setDefault(defaultVal)
            self.assertEqual(defaultVal, self._uut._data.default)

    def test_isInNvmReturnFlag(self) -> None:
        """
        The isInNvm method must return True if the object is flag to be save
        in NVM, False otherwise.
        """
        inNvmFlags = [True, False]
        for flag in inNvmFlags:
            self._uut._data.inNvm = flag
            self.assertEqual(flag, self._uut.isInNvm())

    def test_setInNvmSaveFlag(self) -> None:
        """
        The setInNvmFlag method must save the inNvm flag.
        """
        inNvmFlags = [True, False]
        for flag in inNvmFlags:
            self._uut.setInNvmFlag(flag)
            self.assertEqual(flag, self._uut._data.inNvm)

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

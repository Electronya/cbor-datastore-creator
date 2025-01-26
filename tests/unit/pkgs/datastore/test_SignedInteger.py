from unittest import TestCase
from unittest.mock import Mock, patch
import cbor2
import yaml

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.datastore import (                  # noqa: E402
    LimitError,
    SizeError,
    SignedInteger,
    SignedIntegerData
)


class TestSignedInteger(TestCase):
    """
    SignedInteger test cases.
    """
    def setUp(self) -> None:
        """
        Test cases set up.
        """
        self._loggingMod = 'pkgs.datastore.signedInteger.logging'
        self._mockedLogger = Mock()
        objectData = SignedIntegerData('testObject', 1, 1, -128, 127, 32)
        with patch(self._loggingMod) as mockedLogging:
            mockedLogging.getLogger.return_value = self._mockedLogger
            self._uut = SignedInteger(objectData)
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
            'id': SignedInteger.BASE_ID | objectData.index,
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
        objectData = SignedIntegerData("testObject", 256)
        errMsg = f"Cannot create object {objectData.name}: Invalid index " \
            f"({objectData.index})"
        with patch(self._loggingMod) as mockedLogging, \
                self.assertRaises(IndexError) as context:
            mockedLogging.getLogger.return_value = self._mockedLogger
            SignedInteger(objectData)
            self._mockedLogger.error.assert_called_once_with(errMsg)
            self.assertEqual(errMsg, str(context.exception))

    def test_constructorInvalidSize(self) -> None:
        """
        The constructor must raise a size error if the size used to initialize
        the object is invalid.
        """
        objectData = SignedIntegerData("testObject", 1, 3, 0, 255, 32)
        errMsg = f"Cannot create object {objectData.name}: Invalid size " \
            f"({objectData.size})"
        with patch(self._loggingMod) as mockedLogging, \
                self.assertRaises(SizeError) as context:
            mockedLogging.getLogger.return_value = self._mockedLogger
            SignedInteger(objectData)
            self._mockedLogger.error.assert_called_once_with(errMsg)
            self.assertEqual(errMsg, str(context.exception))

    def test_constructorInvalidLimits(self) -> None:
        """
        The constructor must raise a limit error if the limits used to
        initialize the object are invalid.
        """
        objectData = SignedIntegerData("testObject", 1, 1, -1, 255, 32)
        errMsg = f"Cannot create object {objectData.name}: Invalid min " \
            f"({objectData.min}) or max ({objectData.max})"
        with patch(self._loggingMod) as mockedLogging, \
                self.assertRaises(LimitError) as context:
            mockedLogging.getLogger.return_value = self._mockedLogger
            SignedInteger(objectData)
            self._mockedLogger.error.assert_called_once_with(errMsg)
            self.assertEqual(errMsg, str(context.exception))

    def test_constructorInvalidDefault(self) -> None:
        """
        The constructor must raise a limit error if the default value used to
        initialize the object is invalid.
        """
        objectData = SignedIntegerData("testObject", 1, 1, -128, 127, 128)
        errMsg = f"Cannot create object {objectData.name}: Invalid default " \
            f"({objectData.default})"
        with patch(self._loggingMod) as mockedLogging, \
                self.assertRaises(LimitError) as context:
            mockedLogging.getLogger.return_value = self._mockedLogger
            SignedInteger(objectData)
            self._mockedLogger.error.assert_called_once_with(errMsg)
            self.assertEqual(errMsg, str(context.exception))

    def test_constructorGetLogger(self) -> None:
        """
        The constructor must get the int logger.
        """
        objectData = SignedIntegerData("testObject", 1)
        with patch(self._loggingMod) as mockedLogging:
            SignedInteger(objectData)
            mockedLogging.getLogger.assert_called_once_with('app.datastore.int')

    def test_constructorSaveObjectData(self) -> None:
        """
        The constructor must save the object data.
        """
        objectData = SignedIntegerData("testObject", 1)
        with patch(self._loggingMod):
            testObject = SignedInteger(objectData)
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
        results = [True, True, False, True, False, False, False, True, False]
        for idx, result in enumerate(results):
            size = idx + 1
            self.assertEqual(result, self._uut._isSizeValid(size))

    def test__areLimitsValidReturnValue(self) -> None:
        """
        The _areLimitsValid method return true when the limits are valid and
        false otherwise. to be valid the minimum must be -1 * 2^(8 * size) / 2
        or greater, the maximum must be 2^(8 * size) / 2 - 1 or smaller and the
        minimum must be less than the maximum.
        """
        min4bits = int(-1 * pow(2, 8 * 4) / 2)
        max4bits = int(pow(2, 8 * 4) / 2 - 1)
        min8bits = int(-1 * pow(2, 8 * 8) / 2)
        max8bits = int(pow(2, 8 * 8) / 2 - 1)
        # test values: (size, min, max, result)
        testValues = [(1, -129, 127, False), (1, 0, 128, False),
                      (2, -32769, 32767, False), (2, -32768, 32768, False),
                      (4, min4bits - 1, max4bits, False),
                      (4, min4bits, max4bits + 1, False),
                      (8, min8bits - 1, max8bits, False),    # noqa: E501
                      (8, min8bits, max8bits + 1, False),
                      (1, 1, -1, False), (1, -128, 127, True),
                      (2, -32768, 32767, True), (4, min4bits, max4bits, True),
                      (8, min8bits, max8bits, True)]
        for values in testValues:
            self.assertEqual(values[3], self._uut._areLimitsValid(values[0],
                                                                  values[1],
                                                                  values[2]))

    def test__isDefaultValidReturnValue(self) -> None:
        """
        The _isDefaultValid method must return true when the default is valid
        and false otherwise. To be valid the default value must between the
        minimum and maximum, included.
        """
        # test values: (min, max, default, result)
        testValues = [(-128, 127, -129, False), (-128, 127, 128, False),
                      (-128, 127, -128, True), (-128, 127, 127, True)]
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
            self.assertEqual(SignedInteger.BASE_ID | index,
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
        objectSizes = [3, 5, 6, 7, 9]
        for size in objectSizes:
            errMsg = f"A {size} bytes is not supported"
            with self.assertRaises(SizeError) as context:
                self._uut.setSize(size)
                self.assertEqual(errMsg, str(context.exception))

    def test_setSizeSaveNewObjectSave(self) -> None:
        """
        The setSize method must save the new object size.
        """
        objectSizes = [1, 2, 4, 8]
        for size in objectSizes:
            self._uut.setSize(size)
            self.assertEqual(size, self._uut._data.size)

    def test_getMinReturnMin(self) -> None:
        """
        The getMin method must return the object minimum value.
        """
        objectMinimums = [1, 50, 0]
        for min in objectMinimums:
            self._uut._data.min = min
            self.assertEqual(min, self._uut.getMin())

    def test_getMaxReturnMax(self) -> None:
        """
        The getMax method must return the object maximum value.
        """
        objectMaximums = [127, 100, 75]
        for max in objectMaximums:
            self._uut._data.max = max
            self.assertEqual(max, self._uut.getMax())

    def test_setLimitsRaiseLimitError(self) -> None:
        """
        The setLimits method must raise a limit error if the given limits are
        invalid.
        """
        # Limits: (min, max)
        objectLimits = [(3, 1), (-129, 127), (10, 256), (10, 65536)]
        for limits in objectLimits:
            errMsg = f"A min of {limits[0]} or a max of " \
                     f"{limits[1]} is not valid"
            if limits[1] > 65535:
                self._uut._data.size = 2
            with self.assertRaises(LimitError) as context:
                self._uut.setLimits(limits[0], limits[1])
                self.assertEqual(errMsg, str(context.exception))

    def test_setLimitsSaveLimits(self) -> None:
        """
        The setLimits method must save the new limits.
        """
        # Limits: (min, max)
        objectLimits = [(-128, 127), (10, 15), (-30, 75), (-10, 100)]
        for limits in objectLimits:
            self._uut.setLimits(limits[0], limits[1])
            self.assertEqual(limits[0], self._uut._data.min)
            self.assertEqual(limits[1], self._uut._data.max)

    def test_getDefaultReturnDefault(self) -> None:
        """
        The getDefault method must return the object default value.
        """
        objectDefaultValues = [127, 100, 75]
        for defaultVal in objectDefaultValues:
            self._uut._data.default = defaultVal
            self.assertEqual(defaultVal, self._uut.getDefault())

    def test_setDefaultRaiseLimitError(self) -> None:
        """
        The setDefault method must raise a limit error if the default value is
        outside of the limits.
        """
        # test values: (min, max, default)
        testValues = [(0, 127, 128), (-128, 15, -129),
                      (30, 100, 255), (10, 150, 0)]
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
        objectDefaultValues = [127, -128, 75]
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

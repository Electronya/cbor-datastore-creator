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
    UnsignedInteger,
    UnsignedIntegerData
)


class TestUnsignedInteger(TestCase):
    """
    UnsignedInteger test cases.
    """
    def setUp(self) -> None:
        """
        Test cases set up.
        """
        self._loggingMod = 'pkgs.objects.unsignedInteger.logging'
        self._mockedLogger = Mock()
        objectData = UnsignedIntegerData('testObject', 0x0101, 1, 0, 255, 32)
        with patch(self._loggingMod) as mockedLogging:
            mockedLogging.getLogger.return_value = self._mockedLogger
            self._uut = UnsignedInteger(objectData)
        objectDict = {
            objectData.name: {
                'id': objectData.id,
                'size': objectData.size,
                'min': objectData.min,
                'max': objectData.max,
                'default': objectData.default,
                'inNvm': objectData.inNvm,
            }
        }
        self._ymlString = yaml.dump(objectDict)
        self._cborEncoding = cbor2.dumps(objectDict[objectData.name])

    def test_constructorGetLogger(self) -> None:
        """
        The constructor must get the uint logger.
        """
        objectData = UnsignedIntegerData(0x0101, 1, 0, 255, 32)
        with patch(self._loggingMod) as mockedLogging:
            UnsignedInteger(objectData)
            mockedLogging.getLogger.assert_called_once_with('app.objects.uint')

    def test_constructorSaveObjectData(self) -> None:
        """
        The constructor must save the object data.
        """
        objectData = UnsignedIntegerData(0x0101, 1, 0, 255, 32)
        with patch(self._loggingMod):
            testObject = UnsignedInteger(objectData)
        self.assertEqual(objectData, testObject._data)

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
        objectIds = [0x0101, 0xff02]
        for objectId in objectIds:
            self._uut._data.id = objectId
            self.assertEqual(objectId, self._uut.getId())

    def test_getIndexReturnIndex(self) -> None:
        """
        The getIndex method must return the object index based on its ID.
        """
        objectIds = [0x0101, 0xff02]
        for objectId in objectIds:
            self._uut._data.id = objectId
            self.assertEqual(0xff & objectId, self._uut.getIndex())

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
        objectIndexes = [0x01, 0xff]
        for index in objectIndexes:
            self._uut.setIndex(index)
            self.assertEqual(UnsignedIntegerData.UINT_BASE_ID | index,
                             self._uut._data.id)

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
        objectMaximums = [255, 100, 75]
        for max in objectMaximums:
            self._uut._data.max = max
            self.assertEqual(max, self._uut.getMax())

    def test_setLimitsRaiseLimitError(self) -> None:
        """
        The setLimits method must raise a limit error if the given limits are
        invalid.
        """
        # Limits: (min, max)
        objectLimits = [(3, 1), (-1, 255), (10, 256), (10, 65536)]
        for limits in objectLimits:
            errMsg = f"A min of {limits[0]} or a max of " \
                     f"{limits[1]} is not valid"
            if limits[0] > 65535:
                self._uut._data.size = 2
            with self.assertRaises(LimitError) as context:
                self._uut.setLimits(limits[0], limits[1])
                self.assertEqual(errMsg, str(context.exception))

    def test_setLimitsSaveLimits(self) -> None:
        """
        The setLimits method must save the new limits.
        """
        # Limits: (min, max)
        objectLimits = [(0, 255), (10, 15), (30, 200), (10, 150)]
        for limits in objectLimits:
            self._uut.setLimits(limits[0], limits[1])
            self.assertEqual(limits[0], self._uut._data.min)
            self.assertEqual(limits[1], self._uut._data.max)

    def test_getDefaultReturnDefault(self) -> None:
        """
        The getDefault method must return the object default value.
        """
        objectDefaultValues = [255, 100, 75]
        for defaultVal in objectDefaultValues:
            self._uut._data.default = defaultVal
            self.assertEqual(defaultVal, self._uut.getDefault())

    def test_setDefaultRaiseLimitError(self) -> None:
        """
        The setDefault method must raise a limit error if the default value is
        outside of the limits.
        """
        # test values: (min, max, default)
        testValues = [(0, 255, 256), (10, 15, 5), (30, 200, 255), (10, 150, 0)]
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
        objectDefaultValues = [255, 100, 75]
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

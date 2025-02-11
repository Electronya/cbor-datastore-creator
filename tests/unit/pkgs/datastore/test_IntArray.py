from unittest import TestCase
from unittest.mock import Mock, patch
import cbor2
import yaml

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.datastore import (                  # noqa: E402
    ElementError,
    IntArray,
    IntArrayData,
    IntArrayElement,
)


class TestIntArray(TestCase):
    """
    IntArray test cases.
    """
    def setUp(self) -> None:
        """
        Test cases set up.
        """
        self._loggingMod = 'pkgs.datastore.intArray.logging'
        self._mockedLogger = Mock()
        self._arrayElements = [
            IntArrayElement('int_1', -255, 100, 32),
            IntArrayElement('int_2', -50, 255, 50),
            IntArrayElement('int_3', -25, 75, 32),
        ]
        objectData = IntArrayData('testObject', 1, self._arrayElements, True)
        with patch(self._loggingMod) as mockedLogging:
            mockedLogging.getLogger.return_value = self._mockedLogger
            self._uut = IntArray(objectData)
        objectDict = {
            objectData.name: {
                'index': objectData.index,
                'inNvm': objectData.inNvm,
                'elements': [
                    {objectData.elements[0].name: {
                        'min': objectData.elements[0].min,
                        'max': objectData.elements[0].max,
                        'default': objectData.elements[0].default
                    }},
                    {objectData.elements[1].name: {
                        'min': objectData.elements[1].min,
                        'max': objectData.elements[1].max,
                        'default': objectData.elements[1].default
                    }},
                    {objectData.elements[2].name: {
                        'min': objectData.elements[2].min,
                        'max': objectData.elements[2].max,
                        'default': objectData.elements[2].default
                    }},
                ],
            }
        }
        self._ymlString = yaml.dump(objectDict)
        objectDict = {
            'id': IntArray.BASE_ID | objectData.index,
            'inNvm': objectData.inNvm,
            'elements': [
                {'min': objectData.elements[0].min,
                 'max': objectData.elements[0].max,
                 'default': objectData.elements[0].default},
                {'min': objectData.elements[1].min,
                 'max': objectData.elements[1].max,
                 'default': objectData.elements[1].default},
                {'min': objectData.elements[2].min,
                 'max': objectData.elements[2].max,
                 'default': objectData.elements[2].default},
            ],
        }
        self._cborEncoding = cbor2.dumps(objectDict)

    def test_constructorInvalidIndex(self) -> None:
        """
        The constructor must raise an index error if the object index is not
        valid.
        """
        objectData = IntArrayData("testObject", 256, self._arrayElements)
        errMsg = f"Cannot create object {objectData.name}: Invalid index " \
            f"({objectData.index})"
        with patch(self._loggingMod) as mockedLogging, \
                self.assertRaises(IndexError) as context:
            mockedLogging.getLogger.return_value = self._mockedLogger
            IntArray(objectData)
            self._mockedLogger.error.assert_called_once_with(errMsg)
        self.assertEqual(errMsg, str(context.exception))

    def test_constructorInvalidElements(self) -> None:
        """
        The constructor must raise an index error if the object index is not
        valid.
        """
        for elementIdx in range(len(self._arrayElements)):
            if elementIdx > 0:
                self._arrayElements[elementIdx - 1].min = 0
            self._arrayElements[elementIdx].min = -1 * pow(2, 32) - 1
            objectData = IntArrayData("testObject", 1, self._arrayElements)
            errMsg = f"Cannot create object {objectData.name}: Invalid " \
                f"element ({self._arrayElements[elementIdx]})"
            with patch(self._loggingMod) as mockedLogging, \
                    self.assertRaises(ElementError) as context:
                mockedLogging.getLogger.return_value = self._mockedLogger
                IntArray(objectData)
                self._mockedLogger.error.assert_called_once_with(errMsg)
            self.assertEqual(errMsg, str(context.exception))

    def test_constructorGetLogger(self) -> None:
        """
        The constructor must get the uint array logger.
        """
        objectData = IntArrayData("testObject", 1, self._arrayElements)
        with patch(self._loggingMod) as mockedLogging:
            IntArray(objectData)
            mockedLogging.getLogger.assert_called_once_with('app.datastore.'
                                                            'intArray')

    def test_constructorSaveObjectData(self) -> None:
        """
        The constructor must save the object data.
        """
        objectData = IntArrayData("testObject", 1, self._arrayElements)
        with patch(self._loggingMod):
            testObject = IntArray(objectData)
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

    def test__isElementValid(self) -> None:
        """
        The _isElementValid must return true when the element is valid, false
        otherwise. To be valid the element must comply to the following
        conditions:
          - min >= -1 * 2^32
          - max <= 2^32 - 1
          - min < max
          - min <= default <= max
        """
        # test values: (min, max, default, result)
        testValues = [(-1 * pow(2, 32) - 1, 255, 100, False),
                      (0, pow(2, 32), 100, False),
                      (0, pow(2, 32) - 1, -1, False),
                      (0, pow(2, 32) - 1, pow(2, 32), False),
                      (0, pow(2, 32) - 1, pow(2, 16), True)]
        for values in testValues:
            print(values)
            self.assertEqual(values[3], self._uut
                             ._isElementValid(IntArrayElement('int_4',
                                                              values[0],
                                                              values[1],
                                                              values[2])))

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
            self.assertEqual(IntArray.BASE_ID | index,
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

    def test_setIndexSaveIndex(self) -> None:
        """
        The setIndex must save the index.
        """
        objectIndexes = [2, 3, 4]
        for index in objectIndexes:
            self._uut.setIndex(index)
            self.assertEqual(index, self._uut._data.index)

    def test_getElementCount(self) -> None:
        """
        The getElementCount method must return the number of element in the
        array.
        """
        count = len(self._arrayElements)
        elements = [IntArrayElement('int_4', 10, 30, 15),
                    IntArrayElement('int_5', 0, 255, 4)]
        for element in elements:
            self._uut._data.elements.append(element)
            count += 1
            self.assertEqual(count, self._uut.getElementCount())

    def test_getElementsReturnElements(self) -> None:
        """
        The getElements method must return the list of elements in the
        array.
        """
        self.assertEqual(self._arrayElements, self._uut.getElements())

    def test_getElementRaiseIndexError(self) -> None:
        """
        The getElement method must raise an index error if the given index
        is out of range.
        """
        index = len(self._arrayElements) + 1
        errMsg = f"Element index out of range ({index})"
        with self.assertRaises(IndexError) as context:
            self._uut.getElement(index)
            self._mockedLogger.error.assert_called_once_with(errMsg)
        self.assertEqual(errMsg, str(context.exception))

    def test_getElementReturnElement(self) -> None:
        """
        The getElement method must return the element at the provided index.
        """
        for index in range(len(self._arrayElements)):
            self.assertEqual(self._arrayElements[index],
                             self._uut.getElement(index))

    def test_appendElementRaiseElementError(self) -> None:
        """
        The appendElement method must raise an element error if the new
        element is invalid.
        """
        element = IntArrayElement('int_4', -1 * pow(2, 32) - 1, 10, 5)
        errMsg = f"Cannot append element ({element}) because it's invalid"
        with self.assertRaises(ElementError) as context:
            self._uut.appendElement(element)
            self._mockedLogger.error.assert_called_once_with(errMsg)
        self.assertEqual(errMsg, str(context.exception))

    def test_appendElementAppendNewElement(self) -> None:
        """
        The appendElement method must append the new element.
        """
        newElementIdx = len(self._arrayElements)
        element = IntArrayElement('int_4', 0, 10, 5)
        self._uut.appendElement(element)
        self.assertEqual(element, self._uut._data.elements[newElementIdx])

    def test_removeElementAtIndexRaiseIndexError(self) -> None:
        """
        The removeElementAtIndex method must raise an index error if the given
        index is out of range.
        """
        index = len(self._arrayElements) + 1
        errMsg = f"Element index out of range ({index})"
        with self.assertRaises(IndexError) as context:
            self._uut.removeElementAtIndex(index)
            self._mockedLogger.error.assert_called_once_with(errMsg)
        self.assertEqual(errMsg, str(context.exception))

    def test_removeElementAtIndexRemoveElement(self) -> None:
        """
        The removeElementAtIndex method must remove the element at the given
        index.
        """
        index = 1
        elements = [self._arrayElements[0], self._arrayElements[2]]
        self._uut.removeElementAtIndex(index)
        self.assertEqual(elements, self._uut._data.elements)

    def test_removeElementRaiseValueError(self) -> None:
        """
        The removeElement method must raise a value error when the element is
        not in the array.
        """
        element = IntArrayElement('int_4', 0, 15, 3)
        errMsg = f"Unable to remove element ({element}) because it's not in " \
            f"the array"
        with self.assertRaises(ValueError) as context:
            self._uut.removeElement(element)
            self._mockedLogger.error.assert_called_once_with(errMsg)
        self.assertEqual(errMsg, str(context.exception))

    def test_removeElementRemoveElement(self) -> None:
        """
        The removeElement method must remove the given element.
        """
        element = self._arrayElements[1]
        elements = [self._arrayElements[0], self._arrayElements[2]]
        self._uut.removeElement(element)
        self.assertEqual(elements, self._uut._data.elements)

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

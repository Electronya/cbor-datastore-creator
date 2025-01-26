from unittest import TestCase
from unittest.mock import Mock, patch
import cbor2
import yaml

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.datastore import (                  # noqa: E402
    MultiState,
    MultiStateData,
)


class TestMultiState(TestCase):
    """
    MultiState test cases.
    """
    def setUp(self) -> None:
        """
        Test cases set up.
        """
        self._loggingMod = 'pkgs.datastore.multiState.logging'
        self._mockedLogger = Mock()
        objectData = MultiStateData('testObject', 1, ['STATE_1', 'STATE_2'])
        with patch(self._loggingMod) as mockedLogging:
            mockedLogging.getLogger.return_value = self._mockedLogger
            self._uut = MultiState(objectData)
        objectDict = {
            objectData.name: {
                'index': objectData.index,
                'inNvm': objectData.inNvm,
                'states': objectData.states,
            }
        }
        self._ymlString = yaml.dump(objectDict)
        objectDict = {
            'id': MultiState.BASE_ID | objectData.index,
            'inNvm': objectData.inNvm,
            'states': objectData.states,
        }
        self._cborEncoding = cbor2.dumps(objectDict)

    def test_constructorInvalidIndex(self) -> None:
        """
        The constructor must raise an index error if the object index is not
        valid.
        """
        objectData = MultiStateData("testObject", 256)
        errMsg = f"Cannot create object {objectData.name}: Invalid index " \
            f"({objectData.index})"
        with patch(self._loggingMod) as mockedLogging, \
                self.assertRaises(IndexError) as context:
            mockedLogging.getLogger.return_value = self._mockedLogger
            MultiState(objectData)
            self._mockedLogger.error.assert_called_once_with(errMsg)
            self.assertEqual(errMsg, str(context.exception))

    def test_constructorGetLogger(self) -> None:
        """
        The constructor must get the multi-state logger.
        """
        objectData = MultiStateData("testObject", 1)
        with patch(self._loggingMod) as mockedLogging:
            MultiState(objectData)
            mockedLogging.getLogger.assert_called_once_with('app.datastore.'
                                                            'multi-state')

    def test_constructorSaveObjectData(self) -> None:
        """
        The constructor must save the object data.
        """
        objectData = MultiStateData("testObject", 1, ['STATE_1', 'STATE_2'])
        with patch(self._loggingMod):
            testObject = MultiState(objectData)
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
            self.assertEqual(MultiState.BASE_ID | index,
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

    def test_getStateCountReturnStateCount(self) -> None:
        """
        The getStateCount method must return the object state count.
        """
        objectStates = [['STATE_1', 'STATE_2'],
                        ['STATE_1', 'STATE_2', 'STATE_3']]
        for states in objectStates:
            self._uut._data.states = states
            self.assertEqual(len(states), self._uut.getStateCount())

    def test_getStatesReturnStateList(self) -> None:
        """
        The getStates method must return the object state list.
        """
        objectStates = [['STATE_1', 'STATE_2'],
                        ['STATE_1', 'STATE_2', 'STATE_3']]
        for states in objectStates:
            self._uut._data.states = states
            self.assertEqual(states, self._uut.getStates())

    def test_appendStateSaveNewState(self) -> None:
        """
        The appendState must save the new state in the sate list.
        """
        newStates = ['STATE_3', 'STATE_4']
        expected = list(self._uut._data.states)
        for newState in newStates:
            expected.append(newState)
            self._uut.appendState(newState)
            self.assertEqual(expected, self._uut._data.states)

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

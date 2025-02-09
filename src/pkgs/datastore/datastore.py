from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Self
import cbor2
import logging
import yaml

from .button import Button, ButtonData
from .buttonArray import ButtonArray, ButtonArrayData, ButtonArrayElement
from .floatArray import FloatArray, FloatArrayData, FloatArrayElement
from .floatObject import Float, FloatData
from .intArray import IntArray, IntArrayData, IntArrayElement
from .multiState import MultiState, MultiStateData
from .signedInteger import SignedInteger, SignedIntegerData
from .uintArray import UintArray, UintArrayData, UintArrayElement
from .unsignedInteger import UnsignedInteger, UnsignedIntegerData


@dataclass
class DatastoreData:
    """
    The datastore data.
    """
    name: str
    lastModified: date
    workingDir: str = '.'
    buttons: list[Button] = field(default_factory=list)
    buttonArrays: list[ButtonArray] = field(default_factory=list)
    floats: list[Float] = field(default_factory=list)
    floatArrays: list[FloatArray] = field(default_factory=list)
    multiStates: list[MultiState] = field(default_factory=list)
    signedIntegers: list[SignedInteger] = field(default_factory=list)
    intArrays: list[IntArray] = field(default_factory=list)
    unsignedIntegers: list[UnsignedInteger] = field(default_factory=list)
    uintArrays: list[UintArray] = field(default_factory=list)


class Datastore:
    """
    The datastore class.
    """
    def __init__(self, data: DatastoreData) -> None:
        """
        Constructor.

        Param
            data: the new datastore data.
        """
        self._logger = logging.getLogger('app.datastore')
        self._data = data
        self._logger.info(f"Datastore {self._data.name} created")

    @classmethod
    def parse(cls, yml: dict) -> Self:
        """
        Parser constructor.

        Param
            yml: The datastore dictionary from the yaml encoding.
        """
        lastModified = datetime.strptime(yml['lasModified'], "%d-%m-%Y").date()
        data = DatastoreData(yml['name'], lastModified,
                             yml['workingDir'])
        newStore = Datastore(data)
        return newStore

    def populateButtons(self, buttons: list[dict]) -> None:
        """
        Populate the datastore buttons.

        Param
            buttons: The buttons data.
        """
        for button in buttons:
            name = list(button.keys())[0]
            index = button[name]['index']
            longPressTime = button[name]['longPressTime']
            inactiveTime = button[name]['inactiveTime']
            data = ButtonData(name, index, longPressTime, inactiveTime)
            self._data.buttons.append(Button(data))

    def populateButtonArrays(self, buttonArrays: list[dict]) -> None:
        """
        Populate the datastore button arrays.

        Param
            buttonArrays: The button arrays data.
        """
        for array in buttonArrays:
            name = list(array.keys())[0]
            index = array[name]['index']
            longPressTime = array[name]['longPressTime']
            inactiveTime = array[name]['inactiveTime']
            elements = []
            for element in array[name]['elements']:
                elements.append(ButtonArrayElement(element))
            data = ButtonArrayData(name, index, longPressTime,
                                   inactiveTime, elements)
            self._data.buttonArrays.append(ButtonArray(data))

    def populateFloats(self, floats: list[dict]) -> None:
        """
        Populate the datastore floats.

        Param
            floats: The floats data.
        """
        for floatObj in floats:
            name = list(floatObj.keys())[0]
            index = floatObj[name]['index']
            size = floatObj[name]['size']
            inNvm = floatObj[name]['inNvm']
            min = floatObj[name]['min']
            max = floatObj[name]['max']
            default = floatObj[name]['default']
            data = FloatData(name, index, size, min, max, default, inNvm)
            self._data.floats.append(Float(data))

    def populateFloatArrays(self, floatArrays: list[dict]) -> None:
        """
        Populate the datastore float arrays.

        Param
            floatArrays: The float arrays data.
        """
        for array in floatArrays:
            name = list(array.keys())[0]
            index = array[name]['index']
            inNvm = array[name]['inNvm']
            elements = []
            for element in array[name]['elements']:
                elmtName = list(element.keys())[0]
                elmtMin = element[elmtName]['min']
                elmtMax = element[elmtName]['max']
                elmtDefault = element[elmtName]['default']
                elements.append(FloatArrayElement(elmtName, elmtMin,
                                                  elmtMax, elmtDefault))
            data = FloatArrayData(name, index, elements, inNvm)
            self._data.floatArrays.append(FloatArray(data))

    def populateMultiStates(self, multiStates: list[dict]) -> None:
        """
        Populate the datastore multi-states.

        Param
            multiStates: the multi-states data.
        """
        for multiState in multiStates:
            name = list(multiState.keys())[0]
            index = multiState[name]['index']
            inNvm = multiState[name]['inNvm']
            default = multiState[name]['default']
            states = multiState[name]['states']
            data = MultiStateData(name, index, states, default, inNvm)
            self._data.multiStates.append(MultiState(data))

    def populateSignedIntegers(self, signedIntegers: list[dict]) -> None:
        """
        Populate the datastore signed integers.

        Param
            signedIntegers: the signed integer data.
        """
        for signedInteger in signedIntegers:
            name = list(signedInteger.keys())[0]
            index = signedInteger[name]['index']
            size = signedInteger[name]['size']
            inNvm = signedInteger[name]['inNvm']
            min = signedInteger[name]['min']
            max = signedInteger[name]['max']
            default = signedInteger[name]['default']
            data = SignedIntegerData(name, index, size, min,
                                     max, default, inNvm)
            self._data.signedIntegers.append(SignedInteger(data))

    def populateIntArrays(self, intArrays: list[dict]) -> None:
        """
        Populate the datastore int arrays.

        Param
            intArrays: The int arrays data.
        """
        for array in intArrays:
            name = list(array.keys())[0]
            index = array[name]['index']
            inNvm = array[name]['inNvm']
            elements = []
            for element in array[name]['elements']:
                elmtName = list(element.keys())[0]
                elmtMin = element[elmtName]['min']
                elmtMax = element[elmtName]['max']
                elmtDefault = element[elmtName]['default']
                elements.append(IntArrayElement(elmtName, elmtMin,
                                                elmtMax, elmtDefault))
            data = IntArrayData(name, index, elements, inNvm)
            self._data.intArrays.append(IntArray(data))

    def populateUnsignedIntegers(self, unsignedIntegers: list[dict]) -> None:
        """
        Populate the datastore unsigned integers.

        Param
            unsignedIntegers: the unsigned integer data.
        """
        for unsignedInteger in unsignedIntegers:
            name = list(unsignedInteger.keys())[0]
            index = unsignedInteger[name]['index']
            size = unsignedInteger[name]['size']
            inNvm = unsignedInteger[name]['inNvm']
            min = unsignedInteger[name]['min']
            max = unsignedInteger[name]['max']
            default = unsignedInteger[name]['default']
            data = UnsignedIntegerData(name, index, size, min,
                                       max, default, inNvm)
            self._data.unsignedIntegers.append(UnsignedInteger(data))

    def populateUintArrays(self, uintArrays: list[dict]) -> None:
        """
        Populate the datastore uint arrays.

        Param
            uintArrays: The uint arrays data.
        """
        for array in uintArrays:
            name = list(array.keys())[0]
            index = array[name]['index']
            inNvm = array[name]['inNvm']
            elements = []
            for element in array[name]['elements']:
                elmtName = list(element.keys())[0]
                elmtMin = element[elmtName]['min']
                elmtMax = element[elmtName]['max']
                elmtDefault = element[elmtName]['default']
                elements.append(UintArrayElement(elmtName, elmtMin,
                                                 elmtMax, elmtDefault))
            data = UintArrayData(name, index, elements, inNvm)
            self._data.uintArrays.append(UintArray(data))

    def getName(self) -> str:
        """
        Get the datastore name.

        Return
            The datastore name.
        """
        return self._data.name

    def setName(self, name: str) -> None:
        """
        Set the datastore name.

        Param
            name: the new datastore name.
        """
        self._data.name = name

    def getLastModified(self) -> str:
        """
        Get the last modified date as a string with the format dd-mm-yyyy.

        Return
            The last modified date.
        """
        return self._data.lastModified.strftime("%d-%m-%Y")

    def setLastModified(self, dateStr: str) -> None:
        """
        Set the last modified date.

        Param
            dateStr: The last modified date as string with the format
                     dd-mm-yyyy.
        """
        lastModified = datetime.strptime(dateStr, "%d-%m-%Y").date()
        self._data.lastModified = lastModified

    def getWorkingDir(self) -> str:
        """
        Get the working directory.

        Return
            The working directory.
        """
        return self._data.workingDir

    def setWorkingDir(self, workingDir: str) -> None:
        """
        Set the working directory.

        Param
            workingDir: the working directory.
        """
        self._data.workingDir = workingDir

    def getButtons(self) -> list[Button]:
        """
        Get the datastore buttons.

        Return
            The datastore buttons.
        """
        return self._data.buttons

    def getButtonAtIndex(self, index: int) -> Button:
        """
        Get the button at the specified index.

        Param
            index: the button index.

        Return
            The button at the given index.
        """
        if index >= len(self._data.buttons):
            errMsg = f"Index {index} is out of range"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        return self._data.buttons[index]

    def appendButton(self, button: Button) -> None:
        """
        Append a new button to the datastore.

        Param
            button: The button to append.
        """
        self._data.buttons.append(button)

    def removeButtonAtIndex(self, index: int) -> None:
        """
        Remove the button at given index.

        Params
            index: The index of the button to remove.

        Raise
            An index error if the given index is out of range.
        """
        if index >= len(self._data.buttons):
            errMsg = f"Index {index} is out of range"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        self._data.buttons.pop(index)

    def removeButton(self, button: Button) -> None:
        """
        Remove the given button.

        Params
            button: The button to remove.

        Raise
            A value error if the button is present in the datastore.
        """
        try:
            self._data.buttons.remove(button)
        except ValueError:
            errMsg = f"Button {button.getName()} not present"
            self._logger.error(errMsg)
            raise ValueError(errMsg)

    def getButtonArrays(self) -> list[ButtonArray]:
        """
        Get the datastore button arrays.

        Return
            The datastore button arrays
        """
        return self._data.buttonArrays

    def getButtonArrayAtIndex(self, index: int) -> ButtonArray:
        """
        Get the button array at the given index.

        Params
            index: the given index.

        Return
            The button array at the given index.

        Raise
            An Index error if the given index is out of range.
        """
        if index >= len(self._data.buttonArrays):
            errMsg = f"Index {index} is out of range"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        return self._data.buttonArrays[index]

    def appendButtonArray(self, buttonArray: ButtonArray) -> None:
        """
        Append a new button array to the datastore.

        Param
            buttonArray: The button array to append.
        """
        self._data.buttonArrays.append(buttonArray)

    def removeButtonArrayAtIndex(self, index: int) -> None:
        """
        Remove the button array at given index.

        Params
            index: The index of the button array to remove.

        Raise
            An index error if the given index is out of range.
        """
        if index >= len(self._data.buttonArrays):
            errMsg = f"Index {index} is out of range"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        self._data.buttonArrays.pop(index)

    def removeButtonArray(self, buttonArray: ButtonArray) -> None:
        """
        Remove the given button array.

        Params
            buttonArray: The button array to remove.

        Raise
            A value error if the button array is not in the datastore.
        """
        try:
            self._data.buttonArrays.remove(buttonArray)
        except ValueError:
            errMsg = f"Button array {buttonArray.getName()} not present"
            self._logger.error(errMsg)
            raise ValueError(errMsg)

    def getFloats(self) -> list[Float]:
        """
        Get the datastore floats.

        Return
            The datastore floats.
        """
        return self._data.floats

    def getFloatAtIndex(self, index: int) -> Float:
        """
        Get the float at the given index.

        Params
            index: the given index.

        Return
            The float at the given index.

        Raise
            An Index error if the given index is out of range.
        """
        if index >= len(self._data.floats):
            errMsg = f"Index {index} is out of range"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        return self._data.floats[index]

    def appendFloat(self, floatObj: Float) -> None:
        """
        Append a new float to the datastore.

        Param
            floatObj: The float to append.
        """
        self._data.floats.append(floatObj)

    def removeFloatAtIndex(self, index: int) -> None:
        """
        Remove the float at given index.

        Params
            index: The index of the float to remove.

        Raise
            An index error if the given index is out of range.
        """
        if index >= len(self._data.floats):
            errMsg = f"Index {index} is out of range"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        self._data.floats.pop(index)

    def removeFloat(self, floatObj: Float) -> None:
        """
        Remove the given float.

        Params
            floatObj: The float to remove.

        Raise
            A value error if the float is not in the datastore.
        """
        try:
            self._data.floats.remove(floatObj)
        except ValueError:
            errMsg = f"Float {floatObj.getName()} not present"
            self._logger.error(errMsg)
            raise ValueError(errMsg)

    def getFloatArrays(self) -> list[FloatArray]:
        """
        Get the datastore float arrays.

        Return
            The datastore float arrays
        """
        return self._data.floatArrays

    def getFloatArrayAtIndex(self, index: int) -> FloatArray:
        """
        Get the float array at the given index.

        Params
            index: the given index.

        Return
            The float array at the given index.

        Raise
            An Index error if the given index is out of range.
        """
        if index >= len(self._data.floatArrays):
            errMsg = f"Index {index} is out of range"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        return self._data.floatArrays[index]

    def appendFloatArray(self, floatArray: FloatArray) -> None:
        """
        Append a new float array to the datastore.

        Param
            floatArray: The float array to append.
        """
        self._data.floatArrays.append(floatArray)

    def removeFloatArrayAtIndex(self, index: int) -> None:
        """
        Remove the float array at given index.

        Params
            index: The index of the float array to remove.

        Raise
            An index error if the given index is out of range.
        """
        if index >= len(self._data.floatArrays):
            errMsg = f"Index {index} is out of range"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        self._data.floatArrays.pop(index)

    def removeFloatArray(self, floatArray: FloatArray) -> None:
        """
        Remove the given float array.

        Params
            floatArray: The float array to remove.

        Raise
            A value error if the float array is not in the datastore.
        """
        try:
            self._data.floatArrays.remove(floatArray)
        except ValueError:
            errMsg = f"Float array {floatArray.getName()} not present"
            self._logger.error(errMsg)
            raise ValueError(errMsg)

    def getMultiStates(self) -> list[MultiState]:
        """
        Get the datastore multi-states.

        Return
            The datastore multi-states.
        """
        return self._data.multiStates

    def getMultiStateAtIndex(self, index: int) -> MultiState:
        """
        Get the multi-state at the given index.

        Params
            index: the given index.

        Return
            The multi-state at the given index.

        Raise
            An Index error if the given index is out of range.
        """
        if index >= len(self._data.multiStates):
            errMsg = f"Index {index} is out of range"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        return self._data.multiStates[index]

    def appendMultiState(self, multiState: MultiState) -> None:
        """
        Append a new multi-state to the datastore.

        Param
            multiState: The multi-state to append.
        """
        self._data.multiStates.append(multiState)

    def removeMultiStateAtIndex(self, index: int) -> None:
        """
        Remove the multi-state at given index.

        Params
            index: The index of the multi-state to remove.

        Raise
            An index error if the given index is out of range.
        """
        if index >= len(self._data.multiStates):
            errMsg = f"Index {index} is out of range"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        self._data.multiStates.pop(index)

    def removeMultiState(self, multiState: MultiState) -> None:
        """
        Remove the given multi-state.

        Params
            multiState: The multi-state to remove.

        Raise
            A value error if the multi-state is not in the datastore.
        """
        try:
            self._data.multiStates.remove(multiState)
        except ValueError:
            errMsg = f"Multi-state {multiState.getName()} not present"
            self._logger.error(errMsg)
            raise ValueError(errMsg)

    def getSignedIntegers(self) -> list[SignedInteger]:
        """
        Get the datastore signed integer.

        Return
            The datastore signed integer.
        """
        return self._data.signedIntegers

    def getSignedIntegerAtIndex(self, index: int) -> SignedInteger:
        """
        Get the signed integer at the given index.

        Params
            index: the given index.

        Return
            The signed integer at the given index.

        Raise
            An Index error if the given index is out of range.
        """
        if index >= len(self._data.signedIntegers):
            errMsg = f"Index {index} is out of range"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        return self._data.signedIntegers[index]

    def appendSignedInteger(self, signedInteger: SignedInteger) -> None:
        """
        Append a new signed integer to the datastore.

        Param
            signedInteger: The signed integer to append.
        """
        self._data.signedIntegers.append(signedInteger)

    def removeSignedIntegerAtIndex(self, index: int) -> None:
        """
        Remove the signed integer at given index.

        Params
            index: The index of the signed integer to remove.

        Raise
            An index error if the given index is out of range.
        """
        if index >= len(self._data.signedIntegers):
            errMsg = f"Index {index} is out of range"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        self._data.signedIntegers.pop(index)

    def removeSignedInteger(self, signedInteger: SignedInteger) -> None:
        """
        Remove the given signed integer.

        Params
            signedInteger: The signed integer to remove.

        Raise
            A value error if the signed integer is not in the datastore.
        """
        try:
            self._data.signedIntegers.remove(signedInteger)
        except ValueError:
            errMsg = f"Signed integer {signedInteger.getName()} not present"
            self._logger.error(errMsg)
            raise ValueError(errMsg)

    def getIntArrays(self) -> list[IntArray]:
        """
        Get the datastore singed integer arrays.

        Return
            The datastore signed integer arrays
        """
        return self._data.intArrays

    def getIntArrayAtIndex(self, index: int) -> IntArray:
        """
        Get the integer array at the given index.

        Params
            index: the given index.

        Return
            The integer array at the given index.

        Raise
            An Index error if the given index is out of range.
        """
        if index >= len(self._data.intArrays):
            errMsg = f"Index {index} is out of range"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        return self._data.intArrays[index]

    def appendIntArray(self, intArray: IntArray) -> None:
        """
        Append a new signed integer array to the datastore.

        Param
            intArray: The signed integer array to append.
        """
        self._data.intArrays.append(intArray)

    def removeIntArrayAtIndex(self, index: int) -> None:
        """
        Remove the signed integer array at given index.

        Params
            index: The index of the signed integer array to remove.

        Raise
            An index error if the given index is out of range.
        """
        if index >= len(self._data.intArrays):
            errMsg = f"Index {index} is out of range"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        self._data.intArrays.pop(index)

    def removeIntArray(self, intArray: IntArray) -> None:
        """
        Remove the given signed integer array.

        Params
            intArray: The signed integer array to remove.

        Raise
            A value error if the signed integer array is not in the datastore.
        """
        try:
            self._data.intArrays.remove(intArray)
        except ValueError:
            errMsg = f"Signed integer array {intArray.getName()} not present"
            self._logger.error(errMsg)
            raise ValueError(errMsg)

    def getUnsignedIntegers(self) -> list[UnsignedInteger]:
        """
        Get the datastore unsigned integer.

        Return
            The datastore unsigned integer.
        """
        return self._data.unsignedIntegers

    def getUnsignedIntegerAtIndex(self, index: int) -> UnsignedInteger:
        """
        Get the unsigned integer at the given index.

        Params
            index: the given index.

        Return
            The unsigned integer at the given index.

        Raise
            An Index error if the given index is out of range.
        """
        if index >= len(self._data.unsignedIntegers):
            errMsg = f"Index {index} is out of range"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        return self._data.unsignedIntegers[index]

    def appendUnsignedInteger(self, unsignedInteger: UnsignedInteger) -> None:
        """
        Append a new unsigned integer to the datastore.

        Param
            unsignedInteger: The unsigned integer to append.
        """
        self._data.unsignedIntegers.append(unsignedInteger)

    def removeUnsignedIntegerAtIndex(self, index: int) -> None:
        """
        Remove the unsigned integer at given index.

        Params
            index: The index of the unsigned integer to remove.

        Raise
            An index error if the given index is out of range.
        """
        if index >= len(self._data.unsignedIntegers):
            errMsg = f"Index {index} is out of range"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        self._data.unsignedIntegers.pop(index)

    def removeUnsignedInteger(self, unsignedInteger: UnsignedInteger) -> None:
        """
        Remove the given unsigned integer.

        Params
            unsignedInteger: The unsigned integer to remove.

        Raise
            A value error if the unsigned integer is not in the datastore.
        """
        try:
            self._data.unsignedIntegers.remove(unsignedInteger)
        except ValueError:
            errMsg = f"Unsigned integer {unsignedInteger.getName()} " \
                f"not present"
            self._logger.error(errMsg)
            raise ValueError(errMsg)

    def getUintArrays(self) -> list[UintArray]:
        """
        Get the datastore unsigned integer arrays.

        Return
            The datastore unsigned integer arrays
        """
        return self._data.uintArrays

    def getUintArrayAtIndex(self, index: int) -> UintArray:
        """
        Get the integer array at the given index.

        Params
            index: the given index.

        Return
            The integer array at the given index.

        Raise
            An Index error if the given index is out of range.
        """
        if index >= len(self._data.uintArrays):
            errMsg = f"Index {index} is out of range"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        return self._data.uintArrays[index]

    def appendUintArray(self, uintArray: UintArray) -> None:
        """
        Append a new unsigned integer array to the datastore.

        Param
            intArray: The unsigned integer array to append.
        """
        self._data.uintArrays.append(uintArray)

    def removeUintArrayAtIndex(self, index: int) -> None:
        """
        Remove the unsigned integer array at given index.

        Params
            index: The index of the unsigned integer array to remove.

        Raise
            An index error if the given index is out of range.
        """
        if index >= len(self._data.uintArrays):
            errMsg = f"Index {index} is out of range"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        self._data.uintArrays.pop(index)

    def removeUintArray(self, uintArray: UintArray) -> None:
        """
        Remove the given unsigned integer array.

        Params
            intArray: The unsigned integer array to remove.

        Raise
            A value error if the unsigned integer array is not in the
            datastore.
        """
        try:
            self._data.uintArrays.remove(uintArray)
        except ValueError:
            errMsg = f"Unsigned integer array {uintArray.getName()} not " \
                f"present"
            self._logger.error(errMsg)
            raise ValueError(errMsg)

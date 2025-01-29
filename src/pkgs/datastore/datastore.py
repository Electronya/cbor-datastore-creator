from dataclasses import dataclass, field
from datetime import date
from os import path
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
    floatObjs: list[Float] = field(default_factory=list)
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
        data = DatastoreData(yml['name'], yml['lasModified'],
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
            self._data.floatObjs.append(Float(data))

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

from dataclasses import dataclass, field
from datetime import date
from os import path
from typing import Self
import cbor2
import logging
import yaml

from .button import Button, ButtonData
from .buttonArray import ButtonArray, ButtonArrayData, ButtonArrayElement
from .floatArray import FloatArray
from .floatObject import Float
from .intArray import IntArray
from .multiState import MultiState
from .signedInteger import SignedInteger
from .uintArray import UintArray
from .unsignedInteger import UnsignedInteger


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

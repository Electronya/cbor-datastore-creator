from dataclasses import dataclass
from enum import Enum
import cbor2
import logging
import yaml

from .objectCommon import TimeError


class ButtonStateEnum(Enum):
    """
    The button state enumeration.
    """
    BUTTON_DEPRESSED = 0
    BUTTON_PRESSED = 1


@dataclass
class ButtonStateData:
    """
    Button state data class.
    """
    name: str
    index: int
    longPressTime: int = 3000
    inactiveTime: int = 6000
    isLongPress: bool = False
    isInactive: bool = False
    state: ButtonStateEnum = ButtonStateEnum.BUTTON_DEPRESSED


class ButtonState:
    """
    The button state object type class.
    """
    BASE_ID: int = 0x0400
    MIN_TIME: int = 1000
    MAX_TIME: int = 65535

    def __init__(self, data: ButtonStateData):
        """
        Constructor.

        Params:
            data: The object data.
        """
        self._logger = logging.getLogger("app.objects.uint")
        if not self._isIndexValid(data.index):
            errMsg = f"Cannot create object {data.name}: Invalid index " \
                f"({data.index})"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        if not self._isTimeValid(data.longPressTime):
            errMsg = f"Cannot create object {data.name}: Invalid long press " \
                f"time ({data.longPressTime})"
            self._logger.error(errMsg)
            raise TimeError(errMsg)
        if not self._isTimeValid(data.inactiveTime):
            errMsg = f"Cannot create object {data.name}: Invalid inactive " \
                f"time ({data.inactiveTime})"
            self._logger.error(errMsg)
            raise TimeError(errMsg)
        self._data = data

    def _isIndexValid(self, index: int) -> bool:
        """
        Check if the Index is valid.
        """
        if index < 1 or index > 255:
            return False
        return True

    def _isTimeValid(self, time: int) -> bool:
        """
        Check if the time (long press and inactive times) is valid.

        Params
            time: the time to validate.

        Return
            True if the time is valid, False otherwise.
        """
        if time < self.MIN_TIME or time > self.MAX_TIME:
            return False
        return True

    def getName(self) -> str:
        """
        Get the object name.

        Return
            The object name.
        """
        return self._data.name

    def setName(self, name: str) -> None:
        """
        Set the object name.

        Params
            name: the object name.
        """
        self._data.name = name

    def getId(self) -> int:
        """
        Get the object ID.

        Return
            The object ID.
        """
        return self.BASE_ID | self._data.index

    def getIndex(self) -> int:
        """
        Get the object index.

        Return
            The unsigned integer index.
        """
        return self._data.index

    def setIndex(self, index: int) -> None:
        """
        Set the object index.

        Params
            index: The new object index.

        Raise
            An index error if the index is out of range.
        """
        if not self._isIndexValid(index):
            raise IndexError('Index out of range')
        self._data.index = index

    def getLongPressTime(self) -> int:
        """
        Get the object long press time.

        Return
            The object long press time.
        """
        return self._data.longPressTime

    def setLongPressTime(self, time: int) -> None:
        """
        Set the object long press time.

        Params
            time: The new object long press time (in ms).

        Raise
            A time error if the long press time is invalid.
        """
        if not self._isTimeValid(time):
            raise TimeError(f"A long press time of {time}ms is invalid")
        self._data.longPressTime = time

    def setInactiveTime(self, time: int) -> None:
        """
        Set the object inactive time.

        Params
            time: The new object inactive time (in ms).

        Raise
            A time error if the inactive time is invalid.
        """
        if not self._isTimeValid(time):
            raise TimeError(f"An inactive time of {time}ms is invalid")
        self._data.inactiveTime = time

    def getYamlString(self) -> str:
        """
        Get the object yaml encoding as a string.

        Return
            The object yaml encoding as a string.
        """
        data = {
            self._data.name: {
                'index': self._data.index,
                'longPressTime': self._data.longPressTime,
                'isLongPress': self._data.isLongPress,
                'inactiveTime': self._data.inactiveTime,
                'isInactive': self._data.isInactive,
                'state': self._data.state.name,
            }
        }
        return yaml.dump(data)

    def encodeCbor(self) -> bytes:
        """
        Encode the object in CBOR format.

        Return
            The encoded object.
        """
        data = {
            'id': ButtonState.BASE_ID | self._data.index,
            'longPressTime': self._data.longPressTime,
            'isLongPress': self._data.isLongPress,
            'inactiveTime': self._data.inactiveTime,
            'isInactive': self._data.isInactive,
            'state': self._data.state.value,
        }
        return cbor2.dumps(data)

from dataclasses import dataclass
import cbor2
import logging
import yaml

from .objectCommon import LimitError, SizeError


@dataclass
class UnsignedIntegerData:
    """
    Unsigned integer data class.
    """
    name: str
    index: int
    size: int = 1
    min: int = 0
    max: int = 255
    default: int = 0
    inNvm: bool = False


class UnsignedInteger:
    """
    The unsigned integer object type class.
    """
    BASE_ID: int = 0x0100
    VALID_SIZES = (1, 2, 4, 8)

    def __init__(self, data: UnsignedIntegerData):
        """
        Constructor.

        Params:
            data: The object data dictionary.
        """
        self._logger = logging.getLogger("app.objects.uint")
        if not self._isIndexValid(data.index):
            errMsg = f"Cannot create object {data.name}: Invalid index " \
                f"({data.index})"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        if not self._isSizeValid(data.size):
            errMsg = f"Cannot create object {data.name}: Invalid size " \
                f"({data.size})"
            self._logger.error(errMsg)
            raise SizeError(errMsg)
        if not self._areLimitsValid(data.size, data.min, data.max):
            errMsg = f"Cannot create object {data.name}: Invalid min " \
                f"({data.min}) or max ({data.max})"
            self._logger.error(errMsg)
            raise LimitError(errMsg)
        if not self._isDefaultValid(data.min, data.max, data.default):
            errMsg = f"Cannot create object {data.name}: Invalid default " \
                f"({data.default})"
            self._logger.error(errMsg)
            raise LimitError(errMsg)
        self._data = data

    def _isIndexValid(self, index: int) -> bool:
        """
        Check if the Index is valid.
        """
        if index < 1 or index > 255:
            return False
        return True

    def _isSizeValid(self, size: int) -> bool:
        """
        Check if the size is valid.

        Params
            size: the object size.

        Return
            True if the size is valid, False otherwise.
        """
        if size not in self.VALID_SIZES:
            return False
        return True

    def _areLimitsValid(self, size: int, min: int, max: int) -> bool:
        """
        Check if the limits are valid.

        Params
            size: the object size.
            min: the object minimum value.
            max: the object maximum value.

        Return
            True if the limits are valid, False otherwise.
        """
        if min > max or min < 0 or max > pow(2, 8 * size) - 1:
            return False
        return True

    def _isDefaultValid(self, min: int, max: int, default: int) -> None:
        """
        Check if the default is valid.

        Params:
            min: the object minimum value.
            max: the object maximum value.
            default: the object default value.

        Return
            True if the default is valid, False otherwise.
        """
        if default < min or default > max:
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

    def getSize(self) -> int:
        """
        Get the object size.

        Return
            The object size.
        """
        return self._data.size

    def setSize(self, size: int) -> None:
        """
        Set the object size.

        Params
            size: The new object size (1, 2, 4 or 8 bytes).

        Raise
            A size error if the size is not supported.
        """
        if not self._isSizeValid(size):
            raise SizeError(f"A {size} bytes is not supported")
        self._data.size = size

    def getMin(self) -> int:
        """
        Get the object minimum value.

        Return
            The object minimum value.
        """
        return self._data.min

    def getMax(self) -> int:
        """
        Get the object maximum value.

        Return
            The object maximum value.
        """
        return self._data.max

    def setLimits(self, min: int, max: int) -> None:
        """
        Set the object limits.

        Params
            min: the object minimum value.
            max: the object maximum value.

        Raise
            A limit error if the limits are invalid.
        """
        if not self._areLimitsValid(self._data.size, min, max):
            raise LimitError(f"A min of {min} or a max of {max} is not valid")
        self._data.min = min
        self._data.max = max

    def getDefault(self) -> int:
        """
        Get the object default value.

        Return
            The object default value.
        """
        return self._data.default

    def setDefault(self, default: int) -> None:
        """
        Set the object default value.

        Params
            default: the object default value.

        Raise
            A limit error if the default value is invalid.
        """
        if not self._isDefaultValid(self._data.min, self._data.max, default):
            raise LimitError(f"A value of {default} is outside of the "
                             f"{self._data.min} minimum and "
                             f"{self._data.max} maximum")
        self._data.default = default

    def isInNvm(self) -> bool:
        """
        Check if the object should be saved in NVM.

        Return
            True if the object should saved in NVM, False otherwise.
        """
        return self._data.inNvm

    def setInNvmFlag(self, inNvm: bool) -> None:
        """
        Set the inNvm flag.

        Params
            inNvm: the inNvm flag.
        """
        self._data.inNvm = inNvm

    def getYamlString(self) -> str:
        """
        Get the object yaml encoding as a string.

        Return
            The object yaml encoding as a string.
        """
        data = {
            self._data.name: {
                'index': self._data.index,
                'size': self._data.size,
                'min': self._data.min,
                'max': self._data.max,
                'default': self._data.default,
                'inNvm': self._data.inNvm
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
            'id': self.BASE_ID | self._data.index,
            'size': self._data.size,
            'min': self._data.min,
            'max': self._data.max,
            'default': self._data.default,
            'inNvm': self._data.inNvm
        }
        return cbor2.dumps(data)

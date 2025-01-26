from dataclasses import dataclass, field
import cbor2
import logging
import yaml

from .objectCommon import ElementError


@dataclass
class UintArrayElement:
    """
    The unsigned integer array element.
    """
    name: str
    min: int
    max: int
    default: int


@dataclass
class UintArrayData:
    """
    The unsigned integer array data.
    """
    name: str
    index: int
    elements: list[UintArrayElement] = field(default_factory=list)
    inNvm: bool = False


class UintArray():
    """
    The unsigned integer array class.
    """
    BASE_ID: int = 0x0600

    def __init__(self, data: UintArrayData):
        """
        Constructor.

        Param
            data: the object data.
        """
        self._logger = logging.getLogger('app.objects.uintArray')
        if not self._isIndexValid(data.index):
            errMsg = f"Cannot create object {data.name}: Invalid index " \
                f"({data.index})"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        for element in data.elements:
            if not self._isElementValid(element):
                errMsg = f"Cannot create object {data.name}: Invalid " \
                    f"element ({element})"
                self._logger.error(errMsg)
                raise ElementError(errMsg)
        self._data = data

    def _isIndexValid(self, index: int) -> bool:
        """
        Check the validity of the index.

        Param
            index: the index to validate.

        Return
            True if the index is valid, False otherwise.
        """
        if index < 1 or index > 255:
            return False
        return True

    def _isElementValid(self, element: UintArrayElement) -> bool:
        """
        Check the validity of one array element.

        Param
            element: the element to validate.

        Return
            True if the element is valid, false otherwise.
        """
        if element.min < 0 or element.max > pow(2, 32) - 1 or \
                element.min >= element.max or \
                element.default < element.min or \
                element.default > element.max:
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
            The object index.
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

    def getElementCount(self) -> int:
        """
        Get the array element count.

        Return
            The array element count.
        """
        return len(self._data.elements)

    def getElements(self) -> list[UintArrayElement]:
        """
        Get the array elements.

        Return
            The array elements.
        """
        return self._data.elements

    def getElement(self, index: int) -> UintArrayElement:
        """
        Get the element at specified index.

        Params
            index: The element index.

        Return
            The element at the given index.

        Raise
            An index error if the element index is out of range.
        """
        if index >= len(self._data.elements):
            errMsg = f"Element index out of range ({index})"
            self._logger(errMsg)
            raise IndexError(errMsg)
        return self._data.elements[index]

    def appendElement(self, element: UintArrayElement) -> None:
        """
        Append a new element to the array.

        Param
            element : The new element to append.

        Raise
            An element error if the element is invalid.
        """
        if not self._isElementValid(element):
            errMsg = f"Cannot append element ({element}) because it's invalid"
            self._logger.error(errMsg)
            raise ElementError(errMsg)
        self._data.elements.append(element)

    def removeElementAtIndex(self, index: int) -> None:
        """
        Remove the element at the given index.

        Param
            index: The index of the element to remove.

        Raise
            An index error if the given index is out of range.
        """
        if index >= len(self._data.elements):
            errMsg = f"Element index out of range ({index})"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        self._data.elements.pop(index)

    def removeElement(self, element: UintArrayElement) -> None:
        """
        Remove the element from the array.

        Param
            element: The element to remove from the list.

        Raise
            A value error if the element is not in the array.
        """
        if element not in self._data.elements:
            errMsg = f"Unable to remove element ({element}) because it's " \
                f"not in the array"
            self._logger.error(errMsg)
            raise ValueError(errMsg)
        self._data.elements.remove(element)

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
                'inNvm': self._data.inNvm,
                'elements': [],
            }
        }
        for element in self._data.elements:
            data[self._data.name]['elements'].append({element.name: {
                'min': element.min, 'max': element.max, 'default': element.default}})  # noqa: E501
        return yaml.dump(data)

    def encodeCbor(self) -> bytes:
        """
        Encode the object in CBOR format.

        Return
            The encoded object.
        """
        data = {
            'id': UintArray.BASE_ID | self._data.index,
            'inNvm': self._data.inNvm,
            'elements': [],
        }
        for element in self._data.elements:
            data['elements'].append({'min': element.min,
                                     'max': element.max,
                                     'default': element.default})
        return cbor2.dumps(data)

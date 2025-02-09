from dataclasses import dataclass, field
import cbor2
import logging
import yaml


@dataclass
class ButtonArrayElement:
    """
    The button array element.
    """
    name: str


@dataclass
class ButtonArrayData:
    """
    The button array data.
    """
    name: str
    index: int
    longPressTime: int
    inactiveTime: int
    elements: list[ButtonArrayElement] = field(default_factory=list)


class ButtonArray():
    """
    The button array class.
    """
    BASE_ID: int = 0x0900

    def __init__(self, data: ButtonArrayData):
        """
        Constructor.

        Param
            data: the object data.
        """
        self._logger = logging.getLogger('app.datastore.buttonArray')
        if not self._isIndexValid(data.index):
            errMsg = f"Cannot create object {data.name}: Invalid index " \
                f"({data.index})"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
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

    def getElements(self) -> list[ButtonArrayElement]:
        """
        Get the array elements.

        Return
            The array elements.
        """
        return self._data.elements

    def getElement(self, index: int) -> ButtonArrayElement:
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

    def appendElement(self, element: ButtonArrayElement) -> None:
        """
        Append a new element to the array.

        Param
            element : The new element to append.

        Raise
            An element error if the element is invalid.
        """
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

    def removeElement(self, element: ButtonArrayElement) -> None:
        """
        Remove the element from the array.

        Param
            element: The element to remove from the list.

        Raise
            A value error if the element is not in the array.
        """
        try:
            self._data.elements.remove(element)
        except ValueError:
            errMsg = f"Unable to remove element ({element}) because it's " \
                f"not in the array"
            self._logger.error(errMsg)
            raise ValueError(errMsg)

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
                'inactiveTime': self._data.inactiveTime,
                'elements': [],
            }
        }
        for element in self._data.elements:
            data[self._data.name]['elements'].append(element.name)
        return yaml.dump(data)

    def encodeCbor(self) -> bytes:
        """
        Encode the object in CBOR format.

        Return
            The encoded object.
        """
        data = {
            'id': self.BASE_ID | self._data.index,
            'longPressTime': self._data.longPressTime,
            'inactiveTime': self._data.inactiveTime,
            'elementCount': len(self._data.elements),
        }
        return cbor2.dumps(data)

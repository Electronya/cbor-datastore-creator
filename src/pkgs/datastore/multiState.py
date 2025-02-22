from dataclasses import dataclass, field
import cbor2
import logging
import yaml


@dataclass
class MultiStateData:
    """
    Multi-state data class.
    """
    name: str
    index: int
    states: list[str] = field(default_factory=list)
    default: str = ''
    inNvm: bool = False


class MultiState:
    """
    The button state object type class.
    """
    BASE_ID: int = 0x0500

    def __init__(self, data: MultiStateData):
        """
        Constructor.

        Param
            data: The object data.
        """
        self._logger = logging.getLogger('app.datastore.multi-state')
        if not self._isIndexValid(data.index):
            errMsg = f"Cannot create object {data.name}: Invalid index " \
                f"({data.index})"
            self._logger.error(errMsg)
            raise IndexError(errMsg)
        self._data = data

    def _isIndexValid(self, index: int) -> bool:
        """
        Check if the Index is valid.

        Param
            index: the index to validate.

        Return
            True if the index is valid, false otherwise.
        """
        if index < 1 or index > 255:
            return False
        return True

    def _isDefaultValid(self, default: str) -> bool:
        """
        Check if the default is valid.

        Param
            default: the default to validate.

        Return
            True if the default is valid, false otherwise.
        """
        if default not in self._data.states:
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

        Param
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

        Param
            index: The new object index.

        Raise
            An index error if the index is out of range.
        """
        if not self._isIndexValid(index):
            raise IndexError('Index out of range')
        self._data.index = index

    def getStateCount(self) -> int:
        """
        Get the state count.

        Return
            The object state count.
        """
        return len(self._data.states)

    def getStates(self) -> list[str]:
        """
        Get the states list.

        Return
            The object state list.
        """
        return self._data.states

    def appendState(self, state: str) -> None:
        """
        Append a state to the object.

        Param
            state: the state to append.
        """
        self._data.states.append(state)

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

        Param
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
                'states': self._data.states,
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
            'id': MultiState.BASE_ID | self._data.index,
            'inNvm': self._data.inNvm,
            'states': self._data.states,
        }
        return cbor2.dumps(data)

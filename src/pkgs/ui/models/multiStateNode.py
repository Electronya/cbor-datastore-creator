from dataclasses import dataclass, field
from .baseNode import BaseNode, NodeType
from .stateNode import StateNode


@dataclass
class MultiStateData:
    """
    The multi-state node data.
    """
    states: list[StateNode] = field(default_factory=list)
    default: int = 0
    inNvm: bool = False


class MultiStateNode(BaseNode):
    """
    The multi-state node class.
    """
    def __init__(self, name: str, data: MultiStateData,
                 parent: BaseNode = None):
        super().__init__(name, NodeType.MULTI_STATE, parent=parent)
        self._data = data

    def getStateList(self) -> list[StateNode]:
        """
        Get the state list.

        Return
            The state list.
        """
        return self._data.states

    def getDefaultIndex(self) -> int:
        """
        Get the default state index.

        Return
            The index of the default state.
        """
        return self._data.default

    def setDefaultIndex(self, index: int) -> None:
        """
        Set the default state index.

        Params
            index: The default state index.
        """
        self._data.default = index

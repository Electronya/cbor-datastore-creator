from dataclasses import dataclass, field
from .baseNode import BaseNode, NodeType


@dataclass
class MultiStateData:
    """
    The multi-state node data.
    """
    states: list[str] = field(default_factory=list)
    default: str = ''
    inNvm: bool = False


class MultiStateNode(BaseNode):
    """
    The multi-state node class.
    """
    def __init__(self, name: str, data: MultiStateData,
                 parent: BaseNode = None):
        super().__init__(name, NodeType.MULTI_STATE, parent=parent)
        self._data = data

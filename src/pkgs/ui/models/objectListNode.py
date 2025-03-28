from .baseNode import BaseNode, NodeType


class ObjectListNode(BaseNode):
    """
    The object list node class.
    """
    def __init__(self, name: str, parent: BaseNode) -> None:
        super().__init__(name, NodeType.OBJ_LIST, parent=parent)

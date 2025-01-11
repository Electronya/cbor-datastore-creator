
class SizeError(Exception):
    """
    The object size error.
    """
    def __init__(self, *args):
        super().__init__(*args)


class LimitError(Exception):
    """
    The object limits error
    """
    def __init__(self, *args):
        super().__init__(*args)

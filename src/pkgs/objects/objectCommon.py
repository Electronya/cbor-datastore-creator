
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


class TimeError(Exception):
    """
    The object time error
    """
    def __init__(self, *args):
        super().__init__(*args)


class ElementError(Exception):
    """
    The element error
    """
    def __init__(self, *args):
        super().__init__(*args)

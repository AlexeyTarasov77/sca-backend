class BaseError(Exception):
    """Simplifies creation of custom errors by using msg from declared class attr
    without need of overriding init"""

    msg: str = "base error"

    def __init__(self):
        return super().__init__(self.msg)

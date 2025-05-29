class BaseError(Exception):
    """Simplifies creation of custom errors by using msg from declared class attr
    without need of overriding init"""

    msg: str = "base error"

    def __init__(self, custom_msg: str | None = None):
        return super().__init__(custom_msg or self.msg)

class ServiceError(Exception):
    msg: str = "server error"

    def __init__(self):
        return super().__init__(self.msg)


class InvalidCatBreedError(ServiceError):
    msg = "Invalid breed name"

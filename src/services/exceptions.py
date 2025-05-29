from core.exceptions import BaseError


class ServiceError(BaseError):
    msg: str = "server error"


class InvalidCatBreedError(ServiceError):
    msg = "Invalid breed name"


class CatNotFoundError(ServiceError):
    msg = "Cat not found"

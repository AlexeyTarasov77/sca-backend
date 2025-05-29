from core.exceptions import BaseError


class ServiceError(BaseError):
    msg: str = "server error"


class InvalidCatBreedError(ServiceError):
    msg = "Invalid breed name"


class CatNotFoundError(ServiceError):
    msg = "Cat not found"


class MissionNotFoundError(ServiceError):
    msg = "Mission not found"


class TargetNotFoundError(ServiceError):
    msg = "Target not found"


class InvalidOperationError(ServiceError):
    """Raised when an operation is not allowed in the current state."""

    msg = "Action not allowed"


class InvalidTargetsCount(ServiceError):
    msg = "Targets count should be in range from 1 to 3"

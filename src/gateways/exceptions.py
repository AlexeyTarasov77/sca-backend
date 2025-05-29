from core.exceptions import BaseError


class GatewayError(BaseError):
    msg = "gateway error"


class StorageNotFoundError(GatewayError):
    msg = "record not found in storage"

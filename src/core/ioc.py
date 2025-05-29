from functools import lru_cache
import typing as t
from fastapi import Depends
import punq

from services.cats import CatsService
from services.contracts import ICatsService, IMissionsService
from services.missions import MissionsService


@lru_cache(1)
def get_container() -> punq.Container:
    return init_container()


def init_container() -> punq.Container:
    container = punq.Container()

    container.register(ICatsService, CatsService)
    container.register(IMissionsService, MissionsService)

    return container


def Resolve[T](dep: type[T] | str, **kwargs) -> T:
    return t.cast(T, get_container().resolve(dep, **kwargs))


def Inject[T](dep: type[T] | str, **kwargs):
    def resolver() -> T:
        return Resolve(dep, **kwargs)

    return Depends(resolver)

from threading import Lock
from typing import Any, Type, TypeVar

from named import get_type_name

__all__ = (
    # singleton types
    "Singleton",
    "UnsafeSingleton",
    # singleton meta types
    "SingletonType",
    "UnsafeSingletonType",
    # singleton instances
    "singleton",
    "unsafe_singleton",
)

S = TypeVar("S")


class UnsafeSingletonType(type):
    """The *unsafe* singleton meta type, used to implement *unsafe* singleton types."""

    _INSTANCES = {}  # type: ignore

    def __call__(cls: Type[S], *args: Any, **kwargs: Any) -> S:
        instances = cls._INSTANCES  # type: ignore

        if cls not in instances:
            instances[cls] = super().__call__(*args, **kwargs)  # type: ignore

        return instances[cls]  # type: ignore


class UnsafeSingleton(metaclass=UnsafeSingletonType):
    """The *unsafe* singleton type."""

    def __repr__(self) -> str:
        return get_type_name(self)


unsafe_singleton = UnsafeSingleton()
"""The *unsafe* singleton instance."""


class SingletonType(type):
    """The singleton meta type, used to implement singleton types."""

    _INSTANCES = {}  # type: ignore
    _LOCK = Lock()

    def __call__(cls: Type[S], *args: Any, **kwargs: Any) -> S:
        instances = cls._INSTANCES  # type: ignore
        lock = cls._LOCK  # type: ignore

        # use double-checked locking

        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = super().__call__(*args, **kwargs)  # type: ignore

        return instances[cls]  # type: ignore


class Singleton(metaclass=SingletonType):
    """The singleton type."""

    def __repr__(self) -> str:
        return get_type_name(self)


singleton = Singleton()
"""The singleton instance."""

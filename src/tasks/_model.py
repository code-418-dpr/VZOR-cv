import typing
from abc import ABC, abstractmethod


class Model(ABC):
    @classmethod
    @abstractmethod
    def scan_images(cls, images: typing.Iterable[bytes]) -> list:
        pass

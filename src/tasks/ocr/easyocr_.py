import typing

from easyocr import Reader

from src import conf
from src.tasks._model import Model


class EasyOCR(Model):
    _reader = Reader(lang_list=["en", "ru"], model_storage_directory=conf.MODEL_CACHE_DIR)

    @classmethod
    def scan_images(cls, images: typing.Iterable[bytes]) -> list[str]:
        results = tuple(cls._reader.readtext(image_bytes, detail=0) for image_bytes in images)
        return ["\n".join(result) for result in results]

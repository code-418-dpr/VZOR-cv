import typing

from easyocr import Reader

from src import conf
from src.logger import get_logger
from src.tasks._model import Model

logger = get_logger(__name__)


class EasyOCR(Model):
    _reader = Reader(lang_list=["en", "ru"], model_storage_directory=conf.MODEL_CACHE_DIR)

    @classmethod
    def scan_images(cls, images: typing.Iterable[bytes]) -> list[str]:
        logger.info("Scanning images")
        results = tuple(cls._reader.readtext(image_bytes, detail=0) for image_bytes in images)
        logger.info("Processing finished")
        return ["\n".join(result) for result in results]

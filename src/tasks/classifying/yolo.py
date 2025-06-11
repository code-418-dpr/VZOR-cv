import typing
from io import BytesIO

import ultralytics
from PIL import Image, ImageFile

from src import conf
from src.logger import get_logger
from src.tasks._model import Model

logger = get_logger(__name__)


class YOLO(Model):
    MIN_CONFIDENCE = 0.20
    _detection_model = ultralytics.YOLO(model=conf.MODEL_CACHE_DIR / "yolo11x.pt")
    _classifying_model = ultralytics.YOLO(model=conf.MODEL_CACHE_DIR / "yolo11x-cls.pt")

    @staticmethod
    def _preprocess_bytes(image_bytes: bytes) -> ImageFile:
        return Image.open(BytesIO(image_bytes))

    @classmethod
    def _scan_images_classifying(cls, images: tuple[ImageFile]) -> list[set[str]]:
        outputs = cls._classifying_model(images)
        results = []
        for output in outputs:
            result = set()
            probs = output.probs.data
            top5 = probs.topk(5)
            for idx, conf_ in zip(top5.indices, top5.values, strict=True):
                category: str = output.names[idx.item()]
                value = conf_.item()
                if value > cls.MIN_CONFIDENCE:
                    result.add(category.replace("_", " ").lower())
            results.append(result)
        return results

    @classmethod
    def _scan_images_detection(cls, images: tuple[ImageFile]) -> list[set[str]]:
        outputs = cls._detection_model(images)
        results = []
        for output in outputs:
            class_names = set()
            for class_index in output.boxes.cls.int():
                class_name = output.names[class_index.item()]
                class_name = class_name.replace("_", " ").lower()
                class_names.add(class_name)
            results.append(class_names)
        return results

    @classmethod
    def scan_images(cls, images: typing.Iterable[bytes]) -> list[set[str]]:
        logger.info("Scanning images (detection)")
        images = tuple(cls._preprocess_bytes(image_bytes) for image_bytes in images)
        detection_results = cls._scan_images_detection(images)
        logger.info("Scanning images (classifying)")
        classifying_results = cls._scan_images_classifying(images)
        results = []
        for detection_result, classifying_result in zip(detection_results, classifying_results, strict=True):
            results.append(detection_result | classifying_result)
        logger.info("Processing finished")
        return results

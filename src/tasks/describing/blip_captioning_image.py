import typing
from io import BytesIO

from PIL import Image
from transformers import BlipForConditionalGeneration, BlipProcessor

from src import conf
from src.tasks._model import Model

MODEL_NAME = "Salesforce/blip-image-captioning-base"


class BlipCaptioning(Model):
    _processor = BlipProcessor.from_pretrained(MODEL_NAME, cache_dir=conf.MODEL_CACHE_DIR)
    _model = BlipForConditionalGeneration.from_pretrained(MODEL_NAME, cache_dir=conf.MODEL_CACHE_DIR)

    @staticmethod
    def _preprocess_bytes(image_bytes: bytes) -> Image:
        return Image.open(BytesIO(image_bytes)).convert("RGB")

    @classmethod
    def scan_images(cls, images: typing.Iterable[bytes]) -> list[str]:
        images = tuple(cls._preprocess_bytes(image_bytes) for image_bytes in images)
        inputs = cls._processor(images, return_tensors="pt")
        outputs = cls._model.generate(**inputs)
        results = cls._processor.batch_decode(outputs, skip_special_tokens=True)
        return results

from deep_translator import GoogleTranslator
from PIL import Image
from transformers import pipeline


class ObjectDetectionService:
    def __init__(self) -> None:
        self.detector = pipeline("object-detection", model="facebook/detr-resnet-50")
        self.translator = GoogleTranslator(source="en", target="ru")

    def detect_objects(self, image_path: str) -> list[str]:
        image = Image.open(image_path)
        results = self.detector(image)

        object_names = list({result["label"] for result in results})
        russian_names = [self.translator.translate(name) for name in object_names]

        return russian_names

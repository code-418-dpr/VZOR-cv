from deep_translator import GoogleTranslator
from PIL import Image
from transformers import pipeline


class ImageDescriptionService:
    def __init__(self) -> None:
        self.descriptor = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")
        self.translator = GoogleTranslator(source="en", target="ru")

    def generate_description(self, image_path: str) -> str:
        image = Image.open(image_path)
        result = self.descriptor(image)[0]["generated_text"]
        return self.translator.translate(result)

from src.models.data_models import ImageAnalysisResult
from src.services.image_description import ImageDescriptionService
from src.services.object_detection import ObjectDetectionService
from src.services.text_detection import TextDetectionService


class ImageAnalysisService:
    def __init__(self) -> None:
        self.object_detector = ObjectDetectionService()
        self.text_detector = TextDetectionService()
        self.image_descriptor = ImageDescriptionService()

    def analyze_image(self, image_path: str) -> ImageAnalysisResult:
        objects = self.object_detector.detect_objects(image_path)
        text = self.text_detector.detect_and_correct_text(image_path)
        description = self.image_descriptor.generate_description(image_path)

        return ImageAnalysisResult(
            objects=objects,
            text=text,
            description=description,
        )

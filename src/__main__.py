import json
from pathlib import Path

from src.logger import get_logger
from src.models.data_models import ImageAnalysisResult
from src.services.image_description import ImageDescriptionService
from src.services.object_detection import ObjectDetectionService
from src.services.text_detection import TextDetectionService

logger = get_logger(__name__)

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

def main() -> None:
    logger.info("Starting CV service...")

    input_dir = Path("input")
    input_dir.mkdir(exist_ok=True)

    service = ImageAnalysisService()

    for image_path in input_dir.glob("*"):
        if image_path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            logger.info("Processing image: %s", image_path)
            try:
                result = service.analyze_image(str(image_path))
                logger.info("Analysis result:\n%s", json.dumps(result.model_dump(), ensure_ascii=False, indent=2))
            except Exception:
                logger.exception("Error processing image %s", image_path)

if __name__ == "__main__":
    main()

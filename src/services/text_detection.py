from PIL import Image
from pyaspeller import YandexSpeller
from surya.detection import DetectionPredictor
from surya.recognition import RecognitionPredictor


class TextDetectionService:
    def __init__(self) -> None:
        self.recognition_predictor = RecognitionPredictor()
        self.detection_predictor = DetectionPredictor()
        self.speller = YandexSpeller()

    def detect_and_correct_text(self, image_path: str) -> str:
        image = Image.open(image_path)
        langs = None

        predictions = self.recognition_predictor([image], [langs], self.detection_predictor)

        result = " ".join([line.text for line in predictions[0].text_lines])

        return self.speller.spelled_text(result)

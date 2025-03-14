import json
from pathlib import Path

from src.logger import get_logger
from src.models.data_models import ImageAnalysisResult
from src.services.image_analysis import ImageAnalysisService
from src.app import app

logger = get_logger(__name__)

def main() -> None:
    logger.info("Starting CV service with Flask web server...")
    app.run(debug=True, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()

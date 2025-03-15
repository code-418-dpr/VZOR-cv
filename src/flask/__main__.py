import os
import tempfile

from flask_restx import Api, Resource, fields
from werkzeug.datastructures import FileStorage

from flask import Flask, request
from src.logger import get_logger
from src.services.image_analysis import ImageAnalysisService
from src.utils import json_to_xml

logger = get_logger(__name__)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024

api = Api(
    app,
    version="1.0",
    title="VZOR CV API",
    description="API for image analysis",
    doc="/swagger/",
    default_mediatype="multipart/form-data",
)

analysis_result_model = api.model(
    "ImageAnalysisResult",
    {
        "objects": fields.List(fields.String, description="Detected objects in the image"),
        "text": fields.String(description="Detected and corrected text in the image"),
        "description": fields.String(description="Generated description of the image"),
    },
)

# Определяем новый namespace для более детальной настройки запросов
ns = api.namespace("analyze", description="Image analysis operations")

# Настраиваем загрузку файлов для multipart/form-data
upload_parser = api.parser()
upload_parser.add_argument(
    "files",
    location="files",
    type=FileStorage,
    required=True,
    help="Image file(s) to analyze (JPG, JPEG, PNG only)",
    action="append",  # Указывает, что можно загружать несколько файлов
)


@ns.route("")
class ImageAnalysis(Resource):
    @ns.expect(upload_parser)
    @api.doc(consumes="multipart/form-data")
    @ns.produces(["application/xml"])
    def post(self):
        """Analyze uploaded images."""
        temp_files = []
        try:
            logger.info("Received file upload request")
            logger.debug("Request headers: %s", dict(request.headers))

            # Проверяем тип содержимого
            if not request.content_type or "multipart/form-data" not in request.content_type:
                logger.warning(f"Incorrect content type: {request.content_type}")
                return {"error": "Content-Type must be multipart/form-data"}, 415

            args = upload_parser.parse_args()
            uploaded_files = args.get("files", [])
            logger.info("Number of files received: %d", len(uploaded_files) if uploaded_files else 0)

            if not uploaded_files:
                logger.error("No files were uploaded")
                return {"error": "No files were uploaded"}, 400

            for file in uploaded_files:
                if not file or not file.filename:
                    logger.error("Invalid file object received")
                    return {"error": "Invalid file object"}, 400

                logger.info("Processing file: %s", file.filename)
                file_ext = os.path.splitext(file.filename)[1].lower()
                if file_ext not in [".jpg", ".jpeg", ".png"]:
                    logger.error("Invalid file type: %s", file_ext)
                    return {
                        "error": "Invalid file type",
                        "message": f"File {file.filename} has unsupported extension. Supported types: JPG, JPEG, PNG",
                    }, 400

                if hasattr(file, "content_length") and file.content_length > app.config["MAX_CONTENT_LENGTH"]:
                    logger.error("File too large: %s (%d bytes)", file.filename, file.content_length)
                    return {"error": "File too large", "message": f"File {file.filename} exceeds 100MB limit"}, 413

            service = ImageAnalysisService()
            results = []

            for file in uploaded_files:
                temp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1].lower())
                temp_path = temp.name
                temp_files.append(temp_path)
                try:
                    logger.info("Saving file %s to temporary location: %s", file.filename, temp_path)
                    file.save(temp_path)
                    temp.close()

                    logger.info("Processing image: %s", file.filename)
                    result = service.analyze_image(temp_path)
                    results.append({"objects": result.objects, "description": result.description, "text": result.text})
                    logger.info("Successfully processed image: %s", file.filename)
                except Exception as e:
                    logger.exception("Error processing image %s: %s", file.filename, str(e))
                    return {
                        "error": "Processing error",
                        "message": f"Error processing image {file.filename}: {e!s}",
                    }, 500

            logger.info("Successfully processed all images")
            return json_to_xml(results)

        finally:
            for temp_path in temp_files:
                try:
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                        logger.debug("Cleaned up temporary file: %s", temp_path)
                except Exception as e:
                    logger.warning("Failed to clean up temporary file %s: %s", temp_path, str(e))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

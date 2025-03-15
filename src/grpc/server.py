import logging
import os
import tempfile
from concurrent import futures

import imageGrpc_pb2
import imageGrpc_pb2_grpc
from google.protobuf.empty_pb2 import Empty

import grpc

# Логирование
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Предположим, что у вас есть класс ImageAnalysisService
class ImageAnalysisService:
    def analyze_image(self, image_path):
        # Здесь должна быть ваша логика анализа изображения
        # Возвращаем фиктивные данные для примера
        class Result:
            objects = ["object1", "object2"]
            description = "This is a sample description"
            text = "Sample text"
        return Result()

class ImageServiceServicer(imageGrpc_pb2_grpc.ImageServiceServicer):
    def UploadImage(self, request, context):
        logger.info("Received image upload request")
        temp_files = []

        try:
            # Сохраняем изображение во временный файл
            temp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            temp_path = temp.name
            temp_files.append(temp_path)
            temp.write(request.image_data)
            temp.close()

            # Обрабатываем изображение
            service = ImageAnalysisService()
            result = service.analyze_image(temp_path)

            # Формируем ответ
            return imageGrpc_pb2.UploadImageResponse(
                success=True,
                message="Image processed successfully",
            )
        except Exception as e:
            logger.exception("Error processing image: %s", str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error processing image: {e}")
            return imageGrpc_pb2.UploadImageResponse(
                success=False,
                message=f"Error processing image: {e}",
            )
        finally:
            # Удаляем временные файлы
            for temp_path in temp_files:
                try:
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                        logger.debug("Cleaned up temporary file: %s", temp_path)
                except Exception as e:
                    logger.warning("Failed to clean up temporary file %s: %s", temp_path, str(e))

    def ReturnImageData(self, request, context):
        logger.info("Received ReturnImageData request")
        # Здесь можно вызвать клиент для отправки данных, если нужно
        # Например, отправить данные в другой сервис
        return Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    imageGrpc_pb2_grpc.add_ImageServiceServicer_to_server(ImageServiceServicer(), server)
    server.add_insecure_port("[::]:50050")
    logger.info("Starting gRPC server on port 50050")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

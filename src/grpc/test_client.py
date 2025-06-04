import grpc
from src.grpc import image_pb2 as pb2
from src.grpc import image_pb2_grpc as pb2_grpc
from src import conf


if __name__ == "__main__":
    channel = grpc.insecure_channel(f"localhost:{conf.GRPC_PORT}")
    stub = pb2_grpc.ImageServiceStub(channel)

    request = pb2.UploadImageRequest(
        images=[
            pb2.ImageToProcess(
                id="Амбулатория",
                url="https://region15.ru/wp-content/uploads/2020/12/B5B2364C-05BC-4D8A-A408-8EE24B58B245-scaled.jpeg",
            ),
            pb2.ImageToProcess(
                id="Храм ВС РФ", url="https://pic.rutubelist.ru/video/96/70/9670a4fc5775acdb6fae4a71b9b33cb5.jpg"
            ),
            pb2.ImageToProcess(
                id="Мем", url="https://i.pinimg.com/originals/76/dc/5c/76dc5c67199e014108ccf35e307f67cd.jpg"
            ),
        ]
    )

    response = stub.UploadImage(request)
    for img in response.images:
        print(f"{img.id}:\n{img.description}\n{img.tags}\n{img.recognized_text}")

import grpc

from concurrent import futures
from collections.abc import Callable

from src import conf
from src.grpc import image_pb2 as pb2
from src.grpc import image_pb2_grpc as pb2_grpc


class ImageServiceServicer(pb2_grpc.ImageServiceServicer):
    def __init__(self, serve_func: Callable[[list[dict[str, str]]], list[dict[str, str | set[str]]]]):
        self.serve_func = serve_func

    async def UploadImage(
        self, request: pb2.UploadImageRequest, context: grpc.aio.ServicerContext
    ) -> pb2.UploadImageResponse:
        unprocessed_images = [{"id": image.id, "url": image.url} for image in request.images]
        processed_images = await self.serve_func(unprocessed_images)
        return pb2.UploadImageResponse(images=[pb2.ProcessedImage(**image) for image in processed_images])


async def server(func: Callable[[list[dict[str, str]]], list[dict[str, str | set[str]]]]) -> None:
    server_ = grpc.aio.server()
    pb2_grpc.add_ImageServiceServicer_to_server(ImageServiceServicer(func), server_)
    server_.add_insecure_port(f"[::]:{conf.GRPC_PORT}")
    await server_.start()
    await server_.wait_for_termination()

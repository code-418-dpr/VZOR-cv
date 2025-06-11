import asyncio

import httpx

from src import tasks
from src.grpc import server
from src.logger import get_logger

logger = get_logger(__name__)
client = httpx.AsyncClient()


async def download_image(url: str) -> bytes:
    logger.info("Downloading %s", url)
    response = await client.get(url, timeout=20)
    return response.content


async def serve(images: list[dict[str, str]]) -> list[dict[str, str | set[str]]]:
    try:
        image_bytes = await asyncio.gather(*(download_image(image["url"]) for image in images))
    except httpx.ConnectError:
        logger.exception("Failed downloading images")
        return []
    logger.info("Everything downloaded")
    descriptions = tasks.captioning.BlipImageCaptioning.scan_images(image_bytes)
    classifications = tasks.classifying.YOLO.scan_images(image_bytes)
    texts = tasks.ocr.EasyOCR.scan_images(image_bytes)
    logger.info("Everything processed, creating response")
    processed_images = [
        {
            "id": image["id"],
            "description": descriptions[i],
            "tags": classifications[i],
            "recognized_text": texts[i],
        }
        for i, image in enumerate(images)
    ]
    return processed_images


async def main() -> None:
    logger.info("gRPC server started")
    await server(serve)


if __name__ == "__main__":
    asyncio.run(main())

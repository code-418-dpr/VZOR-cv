import asyncio

import httpx

from src import tasks
from src.grpc import server

client = httpx.AsyncClient()


async def download_image(url: str) -> bytes:
    response = await client.get(url, timeout=20)
    return response.content


async def serve(images: list[dict[str, str]]) -> list[dict[str, str | set[str]]]:
    image_bytes = await asyncio.gather(*(download_image(image["url"]) for image in images))

    descriptions = tasks.describing.BlipCaptioning.scan_images(image_bytes)
    classifications = tasks.classifying.YOLO.scan_images(image_bytes)
    texts = tasks.ocr.EasyOCR.scan_images(image_bytes)

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


if __name__ == "__main__":
    server(
        lambda images: asyncio.run(serve(images)),
    )

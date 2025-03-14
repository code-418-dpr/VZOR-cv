from pydantic import BaseModel


class ImageAnalysisResult(BaseModel):
    objects: list[str]
    text: str
    description: str

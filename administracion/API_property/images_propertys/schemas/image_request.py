from typing import List, Optional, Any
from pydantic import BaseModel

class ImageDetail(BaseModel):
    id_image: int
    image_name: str

class ImageRequest(BaseModel):
    image: List[dict]
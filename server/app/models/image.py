from pydantic import BaseModel
from typing import Optional, List

# This model is just for reference if you want to shape how you store data
class ImageModel(BaseModel):
    url: str
    hash: str
    feature_vector: List[float]
    created_at: Optional[str] = None

class ImageMatch(BaseModel):
    url: str
    similarity: float
    source_url: Optional[str] = None


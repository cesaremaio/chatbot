from pydantic import BaseModel
from typing import Any, Union

class QdrantDocument(BaseModel):
    title: str
    author: str
    keywords: Any
    tables: Union[Any, None] = None
    images: Union[Any, None] = None
    text: str
    full_text: str
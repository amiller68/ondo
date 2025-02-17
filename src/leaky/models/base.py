from pydantic import BaseModel
from typing import Optional

class FileObject(BaseModel):
    cid: str
    path: str
    is_dir: bool
    object: Optional[dict] 
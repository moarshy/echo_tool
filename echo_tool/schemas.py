from pydantic import BaseModel
from typing import Optional

class InputSchema(BaseModel):
    func_name: str
    func_args: Optional[dict] = None
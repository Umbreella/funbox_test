from typing import List

from pydantic import BaseModel


class LinksSchema(BaseModel):
    links: List[str]

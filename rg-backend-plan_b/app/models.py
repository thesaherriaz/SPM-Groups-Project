from pydantic import BaseModel
from typing import List

class ResearchGapRequest(BaseModel):
    query: str

class GapItem(BaseModel):
    statement: str
    score: int

class ResearchGapResponse(BaseModel):
    gaps: List[GapItem]

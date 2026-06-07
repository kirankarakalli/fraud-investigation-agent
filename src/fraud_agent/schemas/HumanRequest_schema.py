from typing import Literal
from pydantic import BaseModel

class HumanReviewRequest(BaseModel):
    decision: Literal["APPROVED", "REJECTED"]
    reviewed_by: str
    review_notes: str
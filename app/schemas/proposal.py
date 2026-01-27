from datetime import datetime
from pydantic import BaseModel, Field

class ProposalCreate(BaseModel):
    cover_letter: str = Field(..., max_length=120)
    proposed_price: int = Field(..., gt=0)


class ProposalResponse(BaseModel):
    task_id: int = Field(..., )
    freelancer_id: int = Field(..., )
    cover_letter: str  = Field(..., )
    proposed_price: int = Field(..., )
    status: str = Field(..., )
    created_at: datetime = Field(..., )

    class Config:
        from_attributes=True

class ProposalResponseList(BaseModel):
    tasks: list[ProposalResponse]
    total: int = Field(..., description='Total number of proposal')

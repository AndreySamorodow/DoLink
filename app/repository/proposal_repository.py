from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.proposals import Proposal


class ProposalRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, task_id, user_id, proposal_data) -> Proposal:
        try:
            proposal_dict = proposal_data.model_dump()
            proposal_dict["task_id"] = task_id
            proposal_dict["freelancer_id"] = user_id

                
            db_proposal = Proposal(**proposal_dict)
                
            self.db.add(db_proposal)
            await self.db.commit()  
            await self.db.refresh(db_proposal)
                
            return db_proposal
                
        except Exception as e:
            await self.db.rollback()  # Откат в случае ошибки
            raise e

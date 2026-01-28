from typing import List, Optional
from sqlalchemy import select, update
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
            await self.db.rollback()
            raise e

    async def get_proposal_exists(self, task_id, user_id):
        query = select(Proposal).filter_by(task_id=task_id, freelancer_id=user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_proposal(self, proposal_id):
        query = select(Proposal).filter_by(id=proposal_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def set_status_approved(self, proposal_id):
        stmt = select(Proposal).filter_by(id=proposal_id)
        result = await self.db.execute(stmt)
        proposal = result.scalar_one_or_none()
        task_id = proposal.task_id

        query = update(Proposal).where(Proposal.task_id == task_id).values(status="rejected")
        await self.db.execute(query)
        query2 = update(Proposal).where(Proposal.id == proposal_id).values(status="approved")
        await self.db.execute(query2)

        await self.db.commit()
        return proposal


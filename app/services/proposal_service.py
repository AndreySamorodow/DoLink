from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.proposal import ProposalResponse

from app.repository.proposal_repository import ProposalRepository


class ProposalService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.proposal_repository = ProposalRepository(db)

    async def verification(self, proposal_id, user_id):
        proposal = await self.proposal_repository.get_proposal(proposal_id)
        if not proposal:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Proposal not exists")
        if not await self.proposal_repository.verification_user(proposal_id, user_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    async def set_approved(self, proposal_id):
        proposal = await self.proposal_repository.get_proposal(proposal_id)
        if not proposal:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Proposal not exists")
        return ProposalResponse.model_validate(await self.proposal_repository.set_status_approved(proposal_id))

    async def set_rejected(self, proposal_id):
        proposal = await self.proposal_repository.get_proposal(proposal_id)
        if not proposal:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Proposal not exists")
        return ProposalResponse.model_validate(await self.proposal_repository.set_status_rejected(proposal_id))
    
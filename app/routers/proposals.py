from typing import Annotated
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth_function import get_user_id
from app.database.database import get_session
from app.services.proposal_service import ProposalService


router = APIRouter(prefix="/api/proposal", tags=["proposals"])

@router.patch("/proposal/{proposal_id}/approved")
async def set_approved_status(proposal_id: int, db: Annotated[AsyncSession, Depends(get_session)]):
    service = ProposalService(db)
    return await service.set_approved(proposal_id)

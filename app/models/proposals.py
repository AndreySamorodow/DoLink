from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, nullable=False)
    task_id = Column(Integer, nullable=False)
    freelancer_id = Column(Integer, nullable=False)
    cover_letter = Column(String, nullable=True)
    proposed_price = Column(Integer, nullable=False)
    status = Column(String, default="pending")#pending (рассматривается), approved (принят заказчиком), rejected (отклонен), archived (устарел)
    created_at = Column(DateTime, default=datetime.utcnow())

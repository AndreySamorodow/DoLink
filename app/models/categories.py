from sqlalchemy import Column, Integer, String
from app.database.database import Base


class Tasks(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)

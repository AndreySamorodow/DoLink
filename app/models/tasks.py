from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.database import Base


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, nullable=False)
    short_description = Column(String, nullable=False)
    description = Column(String, nullable=False)
    author_id = Column(String, nullable=False)
    price = Column()
    category = Column(ForeignKey("categories.id"), nullable=False)

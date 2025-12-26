from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)

    tasks = relationship("Task", back_populates="category") #There can be many tasks of the same category.

    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
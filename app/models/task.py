from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, nullable=False)
    short_description = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer)
    category_id = Column(ForeignKey("categories.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    category = relationship("Category", back_populates="tasks") #A task can have only one category
    author = relationship("User", back_populates="my_tasks")  #A task can have only one author


    
    def __repr__(self):
        return f"<Task(id={self.id}, name='{self.short_description}', price={self.price})>"
    
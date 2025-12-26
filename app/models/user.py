from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    tasks = relationship("Task", back_populates="author") #One author can have many tasks

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.short_description}')>"
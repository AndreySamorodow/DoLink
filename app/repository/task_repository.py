from typing import List
from sqlalchemy.orm import Session, joinedload
from app.models.task import Task


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    async def get_all(self) -> List[Task]:
        return self.db.query(Task).all()
    
    async def get_by_category(self, category_id: int) -> List[Task]:
        return (
            self.db.query(Task)
            .filter_by(Task.category_id == category_id)
            .all()
        )
    

from typing import List
from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:
    def __init__(self, db:Session):
        self.db = db

    async def get_all(self) -> List[Category]:
        return self.db.query(Category).all()
    
    
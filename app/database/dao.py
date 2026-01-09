from sqlalchemy import select
from app.models.user import User


class BaseDao:
    model = None

    @classmethod
    async def find_one_or_none(cls, db, **filters):
        query = select(cls.model).filter_by(**filters)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @classmethod
    async def find_by_id(cls, db, id: int):
        query = select(cls.model).filter_by(id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
class UserDao(BaseDao):
    model = User

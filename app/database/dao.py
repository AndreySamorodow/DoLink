from sqlalchemy import select
from app.models.user import User


class BaseDao:
    model = None

    @classmethod
    async def find_one_or_none(cls, db, **filters):
        query = select(cls.model).filter_by(**filters)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
class UserDao(BaseDao):
    model = User

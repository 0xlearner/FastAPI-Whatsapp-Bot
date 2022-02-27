from sqlalchemy import select
from sqlalchemy.orm import Session

from models.customer import Customer
from models.cake import Cake

from db.models.user import User
from db.models.order import Order


class UserDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def fetch_user_by_email(self, email: str):
        user = await self.db_session.execute(select(User).filter(User.email == email))
        return user.scalar_one_or_none()

    async def record_order(self, u: Customer, c: Cake, price: float):
        user = await self.fetch_user_by_email(u.email)

        if not user:
            user = User(name=u.name, email=u.email)
            self.db_session.add(user)
            await self.db_session.flush()

        order = Order(
            **c.dict(),
            price=price,
            user_id=user.id,
        )
        self.db_session.add(order)
        await self.db_session.flush()

        return order

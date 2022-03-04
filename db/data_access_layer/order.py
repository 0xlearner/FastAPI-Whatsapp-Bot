import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from db.models.order import Order


class CustomerOrder:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def all_cake_orders(self) -> List[Order]:
        orders = await self.db_session.execute(
            select(Order)
            .options(selectinload(Order.users))
            .order_by(Order.created_date.desc())
        )
        return orders.scalars().all()

    async def find_order_by_id(self, order_id) -> Optional[Order]:
        order = await self.db_session.get(Order, order_id)
        return order

    async def fulfill_order(self, order_id) -> bool:
        order = await self.find_order_by_id(order_id)

        if not order:
            return False

        if order.fullfiled_date:
            return True

        order.fullfiled_date = datetime.datetime.now()

        return True

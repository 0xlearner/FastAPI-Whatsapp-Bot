from db.session import async_engine

from db.data_access_layer.order import CustomerOrder


async def get_orders_db():
    async with async_engine() as session:
        async with session.begin():
            yield CustomerOrder(session)

from db.session import async_engine

from db.data_access_layer.user import UserDAL


async def get_user_db():
    async with async_engine() as session:
        async with session.begin():
            yield UserDAL(session)

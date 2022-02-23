from db.session import async_engine
from web_hook.bot import Bot_DAL


async def get_bot_db():
    async with async_engine() as session:
        async with session.begin():
            yield Bot_DAL(session)

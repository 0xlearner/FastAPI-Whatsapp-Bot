from pathlib import Path
import json

import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles


from db.session import engine
from db.base import Base

from views import home, admin
from web_hook import bot

api = fastapi.FastAPI()


@api.on_event("startup")
async def start_app():
    # create db tables on initializing
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


def configure():
    configure_routing()
    # configure_api_keys()


# def configure_api_keys():
#     file = Path("settings.json").absolute()
#     if not file.exists():
#         print(
#             f"WARNING: {file} file not found, you cannot continue, please see settings_template.json"
#         )
#         raise Exception(
#             "settings.json file not found, you cannot continue, please see settings_template.json"
#         )

#     with open("settings.json") as fin:
#         settings = json.load(fin)
#         openweather_service.api_key = settings.get("api_key")


def configure_routing():
    api.mount("/static", StaticFiles(directory="static"), name="static")
    api.include_router(home.router)
    api.include_router(admin.router)
    api.include_router(bot.router)


if __name__ == "__main__":
    configure()
    uvicorn.run(api, port=8000)

else:
    configure()

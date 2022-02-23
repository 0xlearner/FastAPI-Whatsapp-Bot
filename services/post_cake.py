import httpx
from httpx import Response


async def post_data(cake):
    url = "http://127.0.0.1:8000/api/order"

    async with httpx.AsyncClient() as client:
        resp: Response = await client.post(url, json=cake)
        if resp.status_code != 200:
            print(resp.text, resp.status_code)

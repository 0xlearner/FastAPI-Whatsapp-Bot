import httpx
from httpx import Response


async def get_menu():
    url = "https://cloudcitycakecompany.azurewebsites.net/api/flavours"

    async with httpx.AsyncClient() as client:
        resp: Response = await client.get(url, timeout=None)
        if resp.status_code != 200:
            print(resp.text, resp.status_code)

    data = resp.json()
    return data


# https://cloudcitycakecompany.azurewebsites.net/api/pricecalculator?size=large&flavour=vanilla&topping=sprinkles&frosting=vanilla


async def get_price(size: str, flavour: str, frosting: str, topping: str):
    url = f"https://cloudcitycakecompany.azurewebsites.net/api/pricecalculator?size={size}&flavour={flavour}&topping={topping}&frosting={frosting}"

    async with httpx.AsyncClient() as client:
        resp: Response = await client.get(url, timeout=None)
        if resp.status_code != 200:
            print(resp.text, resp.status_code)

    price = resp.json()
    return price["total"]

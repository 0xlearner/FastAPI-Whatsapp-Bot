import fastapi
from fastapi import Request

from models.order import CakeOrder

router = fastapi.APIRouter()


@router.post("/api/order")
async def order(request: Request):
    data = await request.json()

    cake_order = CakeOrder(**data)
    print(cake_order)
    return {"recvd": cake_order.dict()}

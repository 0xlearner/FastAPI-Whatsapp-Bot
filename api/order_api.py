import fastapi
from fastapi import Request

router = fastapi.APIRouter()


@router.post("/api/order")
async def order(request: Request):
    data = await request.json()
    return {"recvd": data}

from uuid import UUID
import fastapi
from fastapi import Request, HTTPException, status
from fastapi import responses
from fastapi import Depends

from starlette.templating import Jinja2Templates

from db.depends import get_orders_db
from db.data_access_layer.order import CustomerOrder


templates = Jinja2Templates("templates")

router = fastapi.APIRouter()


@router.get("/admin")
async def order(request: Request, user_orders: CustomerOrder = Depends(get_orders_db)):
    orders = await user_orders.all_cake_orders()
    return templates.TemplateResponse(
        "admin/index.html", {"request": request, "orders": orders}
    )


@router.get("/admin/fulfill/{order_id}")
async def fulfill(
    order_id,
    user_orders: CustomerOrder = Depends(get_orders_db),
):
    order = await user_orders.find_order_by_id(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} does not exist",
        )
    await user_orders.fulfill_order(order_id)
    return responses.RedirectResponse("/admin")

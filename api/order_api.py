# import fastapi
# from fastapi import Request
# from fastapi import Depends

# from models.order import CakeOrder
# from db.depends import get_user_db
# from db.data_access_layer.user import UserDAL
# from models.order_response import OrderResponse

# router = fastapi.APIRouter()


# @router.post("/api/order")
# async def order(request: Request, user_order: UserDAL = Depends(get_user_db)):
#     data = await request.json()

#     cake_order = CakeOrder(**data)

#     db_order = await user_order.record_order(
#         cake_order.customer, cake_order.cake, cake_order.price
#     )

#     resp = OrderResponse(
#         order_id=db_order.id,
#         order_date=db_order.created_date,
#         email=cake_order.customer.email,
#         price=db_order.price,
#         cake=cake_order.cake,
#     )
#     return resp.dict()

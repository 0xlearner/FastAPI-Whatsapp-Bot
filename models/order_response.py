from uuid import UUID
import datetime
from pydantic import BaseModel

from models.cake import Cake


class OrderResponse(BaseModel):
    order_id: UUID
    order_date: datetime.datetime
    email: str
    price: float
    cake: Cake

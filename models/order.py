from pydantic import BaseModel


from typing import Optional

from models.cake import Cake
from models.customer import Customer


class CakeOrder(BaseModel):
    customer: Customer
    cake: Cake
    price: float
    ref_img: Optional[str] = None

    class config:
        anystr_strip_whitespace: True

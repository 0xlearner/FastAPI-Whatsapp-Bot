import uuid
import datetime
from typing import List
import enum

from sqlalchemy import Column, String, DateTime, orm, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.base_class import Base
from db.models.order import Order


class Status(enum.Enum):
    main_mode = "main_mode"
    ordering_mode = "ordering_mode"
    size_mode = "size_mode"
    flavour_mode = "flavour_mode"
    topping_mode = "topping_mode"
    frosting_mode = "frosting_mode"
    price_mode = "price_mode"
    get_name_mode = "get_name_mode"
    get_email_mode = "get_email_mode"
    order_review = "order_review"


class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    name = Column(String)
    phone = Column(String, index=True)
    email = Column(String, index=True)
    status = Column("status", Enum(Status))
    orders: List[Order] = orm.relationship("Order", back_populates="users")

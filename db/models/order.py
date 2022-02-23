import uuid
import datetime

from sqlalchemy import Column, Float, Integer, String, DateTime, ForeignKey, orm
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.base_class import Base


class Order(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    fullfiled_date = Column(DateTime, index=True)
    size = Column(String)
    flavour = Column(String)
    topping = Column(String)
    frosting = Column(String)
    price = Column(Float, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), default=uuid.uuid4)
    users = orm.relationship("User", back_populates="orders")

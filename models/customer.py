from pydantic import BaseModel


class Customer(BaseModel):
    name: str
    number: str
    email: str
    status: str

    class config:
        anystr_strip_whitespace: True

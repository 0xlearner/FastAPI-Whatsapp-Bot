from pydantic import BaseModel


class Customer(BaseModel):
    name: str
    email: str
    number: str

    class config:
        anystr_strip_whitespace: True

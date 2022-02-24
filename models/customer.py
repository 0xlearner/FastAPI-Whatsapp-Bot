from pydantic import BaseModel


class Customer(BaseModel):
    name: str
    email: str

    class config:
        anystr_strip_whitespace: True


class CutomerInDB(Customer):
    number: str
    status: str

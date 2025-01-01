from pydantic import BaseModel, EmailStr, Field

class OrderDetailsCreate(BaseModel):
    order_id: str
    amount: float = Field(..., gt=0)
    profit: float
    quantity: int = Field(..., gt=0)
    category: str
    sub_category: str


class SalesTargetCreate(BaseModel):
    month: str
    category: str
    target: float = Field(..., gt=0)


class OrderCreate(BaseModel):
    order_id: str
    order_date: str
    customer_name: str
    state: str
    city: str


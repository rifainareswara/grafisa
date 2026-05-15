from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from .models import OrderStatus


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    target: Optional[str] = None
    price: float
    canva_link: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: Optional[str] = None
    price: Optional[float] = None


class Product(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    price: float

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    buyer_name: str
    buyer_email: str
    buyer_phone: Optional[str] = None
    items: List[OrderItemCreate]


class OrderOut(BaseModel):
    id: int
    order_id: str
    buyer_name: str
    buyer_email: str
    buyer_phone: Optional[str]
    total_amount: float
    status: OrderStatus
    midtrans_token: Optional[str]
    midtrans_redirect_url: Optional[str]
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True


class AdminLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class PaymentNotification(BaseModel):
    order_id: str
    status_code: str
    gross_amount: str
    signature_key: str
    transaction_status: str
    fraud_status: Optional[str] = None

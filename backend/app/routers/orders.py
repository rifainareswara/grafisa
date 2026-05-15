from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Order, OrderItem, Product, OrderStatus
from ..schemas import OrderCreate, OrderOut
from ..auth import verify_admin
import uuid

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("/", response_model=OrderOut)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    order_id = f"GRF-{uuid.uuid4().hex[:8].upper()}"

    total = 0.0
    items_to_create = []

    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Produk ID {item.product_id} tidak ditemukan")
        total += product.price
        items_to_create.append((product, item.quantity))

    db_order = Order(
        order_id=order_id,
        buyer_name=order_data.buyer_name,
        buyer_email=order_data.buyer_email,
        buyer_phone=order_data.buyer_phone,
        total_amount=total,
        status=OrderStatus.pending,
    )
    db.add(db_order)
    db.flush()

    for product, _ in items_to_create:
        db_item = OrderItem(
            order_id=db_order.id,
            product_id=product.id,
            product_name=product.name,
            price=product.price,
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order tidak ditemukan")
    return order


@router.get("/", response_model=List[OrderOut])
def list_orders(
    db: Session = Depends(get_db),
    _: str = Depends(verify_admin),
):
    return db.query(Order).order_by(Order.created_at.desc()).all()

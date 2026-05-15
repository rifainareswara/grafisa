from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Order, Product, OrderStatus
from ..schemas import AdminLogin, Token
from ..auth import create_access_token, verify_admin
from ..config import settings

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/login", response_model=Token)
def admin_login(data: AdminLogin):
    if data.username != settings.admin_username or data.password != settings.admin_password:
        raise HTTPException(status_code=401, detail="Username atau password salah")
    token = create_access_token({"sub": data.username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/stats")
def get_stats(db: Session = Depends(get_db), _: str = Depends(verify_admin)):
    total_orders = db.query(Order).count()
    paid_orders = db.query(Order).filter(Order.status == OrderStatus.paid).count()
    pending_orders = db.query(Order).filter(Order.status == OrderStatus.pending).count()
    total_products = db.query(Product).count()

    revenue = db.query(Order).filter(Order.status == OrderStatus.paid).all()
    total_revenue = sum(o.total_amount for o in revenue)

    return {
        "total_orders": total_orders,
        "paid_orders": paid_orders,
        "pending_orders": pending_orders,
        "total_products": total_products,
        "total_revenue": total_revenue,
    }

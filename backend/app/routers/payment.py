from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Order, OrderStatus
from ..schemas import PaymentNotification
from ..config import settings
import midtransclient
import hashlib

router = APIRouter(prefix="/api/payment", tags=["payment"])


def get_snap():
    return midtransclient.Snap(
        is_production=settings.midtrans_is_production,
        server_key=settings.midtrans_server_key,
        client_key=settings.midtrans_client_key,
    )


@router.post("/create/{order_id}")
def create_payment(order_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order tidak ditemukan")
    if order.status != OrderStatus.pending:
        raise HTTPException(status_code=400, detail="Order sudah diproses")

    snap = get_snap()

    item_details = []
    for item in order.items:
        item_details.append({
            "id": str(item.product_id),
            "price": int(item.price),
            "quantity": 1,
            "name": item.product_name[:50],
        })

    transaction = {
        "transaction_details": {
            "order_id": order.order_id,
            "gross_amount": int(order.total_amount),
        },
        "customer_details": {
            "first_name": order.buyer_name,
            "email": order.buyer_email,
            "phone": order.buyer_phone or "",
        },
        "item_details": item_details,
        "callbacks": {
            "finish": f"{settings.frontend_url}/payment/success?order_id={order.order_id}",
        },
    }

    try:
        snap_response = snap.create_transaction(transaction)
        order.midtrans_token = snap_response["token"]
        order.midtrans_redirect_url = snap_response["redirect_url"]
        db.commit()
        return {
            "token": snap_response["token"],
            "redirect_url": snap_response["redirect_url"],
            "order_id": order.order_id,
            "client_key": settings.midtrans_client_key,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal membuat transaksi: {str(e)}")


@router.post("/notification")
async def payment_notification(request: Request, db: Session = Depends(get_db)):
    body = await request.json()

    order_id = body.get("order_id")
    status_code = body.get("status_code")
    gross_amount = body.get("gross_amount")
    server_key = settings.midtrans_server_key
    transaction_status = body.get("transaction_status")
    fraud_status = body.get("fraud_status")

    raw = f"{order_id}{status_code}{gross_amount}{server_key}"
    signature = hashlib.sha512(raw.encode()).hexdigest()
    if signature != body.get("signature_key"):
        raise HTTPException(status_code=400, detail="Signature tidak valid")

    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order tidak ditemukan")

    if transaction_status == "capture":
        if fraud_status == "accept":
            order.status = OrderStatus.paid
    elif transaction_status == "settlement":
        order.status = OrderStatus.paid
    elif transaction_status in ("cancel", "deny", "expire"):
        order.status = OrderStatus.cancelled

    db.commit()
    return {"status": "ok"}

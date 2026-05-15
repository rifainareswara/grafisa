from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import products, orders, payment, admin
from .seed import seed_products
from .config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Grafisa Canva Templates API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173", "http://localhost:4173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(orders.router)
app.include_router(payment.router)
app.include_router(admin.router)


@app.on_event("startup")
def on_startup():
    seed_products()


@app.get("/")
def root():
    return {"message": "Grafisa API is running"}

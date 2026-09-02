from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import auth, categories, products, search, cart, wishlist, addresses, orders

app = FastAPI(
    title="Opticals API",
    description="Lenskart-style Eyewear E-commerce API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_prefix = "/api/v1"
app.include_router(auth.router, prefix=api_prefix)
app.include_router(categories.router, prefix=api_prefix)
app.include_router(products.router, prefix=api_prefix)
app.include_router(search.router, prefix=api_prefix)
app.include_router(cart.router, prefix=api_prefix)
app.include_router(wishlist.router, prefix=api_prefix)
app.include_router(addresses.router, prefix=api_prefix)
app.include_router(orders.router, prefix=api_prefix)


@app.get("/")
def root():
    return {"message": "Opticals API is running", "docs": "/docs"}

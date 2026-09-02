from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    brand = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    discount_price = Column(Float, nullable=True)
    gender = Column(String(20), nullable=True)  # men, women, unisex, kids
    frame_shape = Column(String(50), nullable=True)  # round, rectangle, aviator, cat-eye, wayfarer, etc.
    frame_type = Column(String(50), nullable=True)  # full-rim, half-rim, rimless
    frame_material = Column(String(50), nullable=True)  # metal, acetate, titanium, TR90
    color = Column(String(50), nullable=True)
    stock_quantity = Column(Integer, default=0)
    rating_avg = Column(Float, default=0.0)
    promo_tag = Column(String(50), nullable=True)  # e.g. "Buy 1 Get 1", "Flat 50% Off"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship("Category", back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(String(500), nullable=False)
    is_primary = Column(Integer, default=0)  # 1 = primary

    product = relationship("Product", back_populates="images")

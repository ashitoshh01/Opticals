"""Seed script to populate database with sample categories and ~35 products."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.db.base import Base
from app.db.database import engine
from app.models.category import Category
from app.models.product import Product, ProductImage

# Import all models so Base.metadata knows about them
from app.models.user import User
from app.models.cart import CartItem, WishlistItem
from app.models.order import Order, OrderItem
from app.models.review import Review
from app.models.address import Address


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear existing data
    db.query(ProductImage).delete()
    db.query(Product).delete()
    db.query(Category).delete()
    db.commit()

    # Categories
    categories = [
        Category(name="Eyeglasses", slug="eyeglasses"),
        Category(name="Sunglasses", slug="sunglasses"),
        Category(name="Contact Lenses", slug="contact-lenses"),
        Category(name="Kids Glasses", slug="kids-glasses"),
    ]
    db.add_all(categories)
    db.commit()
    for c in categories:
        db.refresh(c)

    cat_map = {c.slug: c.id for c in categories}

    # Placeholder image base
    IMG = "https://placehold.co/400x300/222/FFC609?text="

    products_data = [
        # Eyeglasses (10)
        {"name": "Vincent Chase Classic Rectangle", "slug": "vc-classic-rectangle", "brand": "Vincent Chase", "cat": "eyeglasses", "price": 1999, "dp": 999, "gender": "unisex", "shape": "rectangle", "ftype": "full-rim", "material": "acetate", "color": "Black", "stock": 50, "rating": 4.3, "promo": "Buy 1 Get 1"},
        {"name": "Lenskart Air Round", "slug": "lk-air-round", "brand": "Lenskart Air", "cat": "eyeglasses", "price": 2499, "dp": 1299, "gender": "unisex", "shape": "round", "ftype": "full-rim", "material": "TR90", "color": "Tortoise", "stock": 35, "rating": 4.5, "promo": "Flat 50% Off"},
        {"name": "John Jacobs Aviator", "slug": "jj-aviator-gold", "brand": "John Jacobs", "cat": "eyeglasses", "price": 3999, "dp": 1999, "gender": "men", "shape": "aviator", "ftype": "full-rim", "material": "metal", "color": "Gold", "stock": 20, "rating": 4.7, "promo": None},
        {"name": "Vincent Chase Cat Eye", "slug": "vc-cat-eye-pink", "brand": "Vincent Chase", "cat": "eyeglasses", "price": 2199, "dp": 1099, "gender": "women", "shape": "cat-eye", "ftype": "full-rim", "material": "acetate", "color": "Pink", "stock": 40, "rating": 4.2, "promo": "Buy 1 Get 1"},
        {"name": "Lenskart Blu Zero Power", "slug": "lk-blu-zero", "brand": "Lenskart Blu", "cat": "eyeglasses", "price": 1499, "dp": 799, "gender": "unisex", "shape": "rectangle", "ftype": "full-rim", "material": "TR90", "color": "Matte Black", "stock": 100, "rating": 4.6, "promo": "Best Seller"},
        {"name": "John Jacobs Wayfarer", "slug": "jj-wayfarer-brown", "brand": "John Jacobs", "cat": "eyeglasses", "price": 3499, "dp": 1749, "gender": "unisex", "shape": "wayfarer", "ftype": "full-rim", "material": "acetate", "color": "Brown", "stock": 25, "rating": 4.4, "promo": None},
        {"name": "Vincent Chase Rimless", "slug": "vc-rimless-silver", "brand": "Vincent Chase", "cat": "eyeglasses", "price": 2999, "dp": 1499, "gender": "men", "shape": "rectangle", "ftype": "rimless", "material": "titanium", "color": "Silver", "stock": 15, "rating": 4.1, "promo": "Flat 50% Off"},
        {"name": "Lenskart Air Half Rim", "slug": "lk-air-half-rim", "brand": "Lenskart Air", "cat": "eyeglasses", "price": 1899, "dp": 949, "gender": "women", "shape": "round", "ftype": "half-rim", "material": "metal", "color": "Rose Gold", "stock": 30, "rating": 4.3, "promo": None},
        {"name": "John Jacobs Geometric", "slug": "jj-geometric-blue", "brand": "John Jacobs", "cat": "eyeglasses", "price": 4299, "dp": 2149, "gender": "unisex", "shape": "round", "ftype": "full-rim", "material": "acetate", "color": "Navy Blue", "stock": 12, "rating": 4.8, "promo": "New Arrival"},
        {"name": "Lenskart Hustlr Square", "slug": "lk-hustlr-square", "brand": "Lenskart Hustlr", "cat": "eyeglasses", "price": 1699, "dp": 849, "gender": "men", "shape": "rectangle", "ftype": "full-rim", "material": "TR90", "color": "Gunmetal", "stock": 45, "rating": 4.0, "promo": "Buy 1 Get 1"},

        # Sunglasses (10)
        {"name": "Vincent Chase Polarized Aviator", "slug": "vc-polar-aviator", "brand": "Vincent Chase", "cat": "sunglasses", "price": 2499, "dp": 1249, "gender": "unisex", "shape": "aviator", "ftype": "full-rim", "material": "metal", "color": "Gold/Green", "stock": 30, "rating": 4.5, "promo": "Flat 50% Off"},
        {"name": "John Jacobs Polarized Wayfarer", "slug": "jj-polar-wayfarer", "brand": "John Jacobs", "cat": "sunglasses", "price": 3999, "dp": 1999, "gender": "unisex", "shape": "wayfarer", "ftype": "full-rim", "material": "acetate", "color": "Black/Grey", "stock": 25, "rating": 4.7, "promo": None},
        {"name": "Lenskart Studio Cat Eye Sun", "slug": "lk-studio-cateye-sun", "brand": "Lenskart Studio", "cat": "sunglasses", "price": 1999, "dp": 999, "gender": "women", "shape": "cat-eye", "ftype": "full-rim", "material": "acetate", "color": "Tortoise/Brown", "stock": 35, "rating": 4.3, "promo": "Buy 1 Get 1"},
        {"name": "Vincent Chase Sport Wrap", "slug": "vc-sport-wrap", "brand": "Vincent Chase", "cat": "sunglasses", "price": 1799, "dp": 899, "gender": "men", "shape": "rectangle", "ftype": "full-rim", "material": "TR90", "color": "Matte Black/Red", "stock": 40, "rating": 4.1, "promo": None},
        {"name": "John Jacobs Round Metal Sun", "slug": "jj-round-metal-sun", "brand": "John Jacobs", "cat": "sunglasses", "price": 4499, "dp": 2249, "gender": "unisex", "shape": "round", "ftype": "full-rim", "material": "metal", "color": "Gold/Blue Mirror", "stock": 18, "rating": 4.6, "promo": "Premium"},
        {"name": "Lenskart Studio Oversized", "slug": "lk-studio-oversized", "brand": "Lenskart Studio", "cat": "sunglasses", "price": 2299, "dp": 1149, "gender": "women", "shape": "round", "ftype": "full-rim", "material": "acetate", "color": "Black/Gradient", "stock": 22, "rating": 4.4, "promo": "Flat 50% Off"},
        {"name": "Vincent Chase Clubmaster", "slug": "vc-clubmaster-sun", "brand": "Vincent Chase", "cat": "sunglasses", "price": 2699, "dp": 1349, "gender": "unisex", "shape": "wayfarer", "ftype": "half-rim", "material": "metal", "color": "Black/Gold", "stock": 28, "rating": 4.5, "promo": None},
        {"name": "John Jacobs Shield", "slug": "jj-shield-sun", "brand": "John Jacobs", "cat": "sunglasses", "price": 5299, "dp": 2649, "gender": "men", "shape": "rectangle", "ftype": "rimless", "material": "titanium", "color": "Silver/Smoke", "stock": 10, "rating": 4.8, "promo": "New Arrival"},
        {"name": "Lenskart Active Sporty", "slug": "lk-active-sporty", "brand": "Lenskart Active", "cat": "sunglasses", "price": 1599, "dp": 799, "gender": "men", "shape": "rectangle", "ftype": "full-rim", "material": "TR90", "color": "Black/Yellow", "stock": 50, "rating": 4.0, "promo": "Buy 1 Get 1"},
        {"name": "Vincent Chase Retro Round", "slug": "vc-retro-round-sun", "brand": "Vincent Chase", "cat": "sunglasses", "price": 1999, "dp": 999, "gender": "unisex", "shape": "round", "ftype": "full-rim", "material": "metal", "color": "Rose Gold/Pink", "stock": 32, "rating": 4.3, "promo": None},

        # Contact Lenses (8)
        {"name": "Aqualens 24H Daily", "slug": "aqualens-24h-daily", "brand": "Aqualens", "cat": "contact-lenses", "price": 799, "dp": 599, "gender": "unisex", "shape": None, "ftype": None, "material": None, "color": "Clear", "stock": 200, "rating": 4.4, "promo": "Best Seller"},
        {"name": "Aqualens Comfort Monthly", "slug": "aqualens-comfort-monthly", "brand": "Aqualens", "cat": "contact-lenses", "price": 499, "dp": 349, "gender": "unisex", "shape": None, "ftype": None, "material": None, "color": "Clear", "stock": 150, "rating": 4.2, "promo": None},
        {"name": "Aqualens Turquoise Color", "slug": "aqualens-turquoise", "brand": "Aqualens", "cat": "contact-lenses", "price": 999, "dp": 699, "gender": "unisex", "shape": None, "ftype": None, "material": None, "color": "Turquoise", "stock": 80, "rating": 4.5, "promo": "Trending"},
        {"name": "Aqualens Brown Color", "slug": "aqualens-brown", "brand": "Aqualens", "cat": "contact-lenses", "price": 999, "dp": 699, "gender": "unisex", "shape": None, "ftype": None, "material": None, "color": "Brown", "stock": 75, "rating": 4.3, "promo": None},
        {"name": "Aqualens Grey Color", "slug": "aqualens-grey", "brand": "Aqualens", "cat": "contact-lenses", "price": 999, "dp": 699, "gender": "unisex", "shape": None, "ftype": None, "material": None, "color": "Grey", "stock": 60, "rating": 4.6, "promo": "Flat 30% Off"},
        {"name": "Aqualens Green Color", "slug": "aqualens-green", "brand": "Aqualens", "cat": "contact-lenses", "price": 999, "dp": 699, "gender": "unisex", "shape": None, "ftype": None, "material": None, "color": "Green", "stock": 55, "rating": 4.1, "promo": None},
        {"name": "Aqualens Toric Astigmatism", "slug": "aqualens-toric", "brand": "Aqualens", "cat": "contact-lenses", "price": 1299, "dp": 899, "gender": "unisex", "shape": None, "ftype": None, "material": None, "color": "Clear", "stock": 40, "rating": 4.7, "promo": None},
        {"name": "Aqualens Multi-focal", "slug": "aqualens-multifocal", "brand": "Aqualens", "cat": "contact-lenses", "price": 1499, "dp": 999, "gender": "unisex", "shape": None, "ftype": None, "material": None, "color": "Clear", "stock": 30, "rating": 4.4, "promo": None},

        # Kids (7)
        {"name": "Lenskart Junior Round", "slug": "lk-junior-round", "brand": "Lenskart Junior", "cat": "kids-glasses", "price": 1299, "dp": 649, "gender": "kids", "shape": "round", "ftype": "full-rim", "material": "TR90", "color": "Blue", "stock": 30, "rating": 4.5, "promo": "Buy 1 Get 1"},
        {"name": "Lenskart Junior Rectangle", "slug": "lk-junior-rectangle", "brand": "Lenskart Junior", "cat": "kids-glasses", "price": 1299, "dp": 649, "gender": "kids", "shape": "rectangle", "ftype": "full-rim", "material": "TR90", "color": "Red", "stock": 25, "rating": 4.3, "promo": None},
        {"name": "Lenskart Junior Cat Eye", "slug": "lk-junior-cateye", "brand": "Lenskart Junior", "cat": "kids-glasses", "price": 1499, "dp": 749, "gender": "kids", "shape": "cat-eye", "ftype": "full-rim", "material": "TR90", "color": "Purple", "stock": 20, "rating": 4.4, "promo": "New"},
        {"name": "Vincent Chase Kids Flex", "slug": "vc-kids-flex", "brand": "Vincent Chase", "cat": "kids-glasses", "price": 1599, "dp": 799, "gender": "kids", "shape": "rectangle", "ftype": "full-rim", "material": "TR90", "color": "Green", "stock": 18, "rating": 4.2, "promo": None},
        {"name": "Lenskart Junior Sporty", "slug": "lk-junior-sporty", "brand": "Lenskart Junior", "cat": "kids-glasses", "price": 999, "dp": 499, "gender": "kids", "shape": "rectangle", "ftype": "full-rim", "material": "TR90", "color": "Black/Yellow", "stock": 35, "rating": 4.0, "promo": "Best Seller"},
        {"name": "Vincent Chase Kids Round", "slug": "vc-kids-round-pink", "brand": "Vincent Chase", "cat": "kids-glasses", "price": 1399, "dp": 699, "gender": "kids", "shape": "round", "ftype": "full-rim", "material": "TR90", "color": "Pink", "stock": 22, "rating": 4.6, "promo": None},
        {"name": "Lenskart Junior Aviator", "slug": "lk-junior-aviator", "brand": "Lenskart Junior", "cat": "kids-glasses", "price": 1199, "dp": 599, "gender": "kids", "shape": "aviator", "ftype": "full-rim", "material": "metal", "color": "Silver", "stock": 15, "rating": 4.1, "promo": "Flat 50% Off"},
    ]

    for p_data in products_data:
        product = Product(
            category_id=cat_map[p_data["cat"]],
            name=p_data["name"],
            slug=p_data["slug"],
            brand=p_data["brand"],
            description=f"Premium {p_data['brand']} {p_data.get('shape', '')} eyewear. Lightweight and comfortable for all-day wear.",
            price=p_data["price"],
            discount_price=p_data["dp"],
            gender=p_data["gender"],
            frame_shape=p_data.get("shape"),
            frame_type=p_data.get("ftype"),
            frame_material=p_data.get("material"),
            color=p_data["color"],
            stock_quantity=p_data["stock"],
            rating_avg=p_data["rating"],
            promo_tag=p_data.get("promo"),
        )
        db.add(product)
        db.commit()
        db.refresh(product)

        # Add product images
        img_name = p_data["slug"].replace("-", "+")
        for i, suffix in enumerate(["Front", "Side", "Angle"]):
            db.add(ProductImage(
                product_id=product.id,
                image_url=f"{IMG}{img_name}+{suffix}",
                is_primary=1 if i == 0 else 0,
            ))
        db.commit()

    db.close()
    print(f"Seeded {len(products_data)} products across {len(categories)} categories.")


if __name__ == "__main__":
    seed()

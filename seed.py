from __future__ import annotations

from db import DatabaseManager
from models import Product, ElectronicsProduct, PerishableProduct

# simple script that seeds the database with a handful of sample items
# meant for development/demo purposes only


def seed_database() -> None:

    db = DatabaseManager()

    samples: list[Product] = [
        Product(product_id=1, name="Widget", price=10.99, stock_quantity=50),
        ElectronicsProduct(
            product_id=2,
            name="Headphones",
            price=59.99,
            stock_quantity=20,
            warranty_period=12,
        ),
        PerishableProduct(
            product_id=3,
            name="Milk",
            price=2.49,
            stock_quantity=100,
            expiration_date="2026-03-15",
        ),
    ]

    for product in samples:
        try:
            # ignore problems such as "already exists" so repeated runs are safe
            db.insert_product(product)
        except Exception:
            pass


if __name__ == "__main__":
    seed_database()
    print("Seeding complete.")

from __future__ import annotations

import sqlite3
from pathlib import Path

from models import ElectronicsProduct, PerishableProduct, Product


class DatabaseManager:
    def __init__(self, db_path: str = "inventory.db", schema_path: str = "schema.sql") -> None:
        self.db_path = Path(db_path)
        self.schema_path = Path(schema_path)
        self._initialize_database()

    def _get_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON;")
        return connection

    def _initialize_database(self) -> None:
        schema_sql = self.schema_path.read_text(encoding="utf-8")
        with self._get_connection() as connection:
            connection.executescript(schema_sql)

    def insert_product(self, product: Product) -> None:
        product_type = "general"
        with self._get_connection() as connection:
            if isinstance(product, ElectronicsProduct):
                product_type = "electronics"
            elif isinstance(product, PerishableProduct):
                product_type = "perishable"

            connection.execute(
                """
                INSERT INTO Products (product_id, name, price, stock_quantity, product_type)
                VALUES (?, ?, ?, ?, ?)
                """,
                (product.product_id, product.name, product.price, product.stock_quantity, product_type),
            )

            if isinstance(product, ElectronicsProduct):
                connection.execute(
                    "INSERT INTO Electronics (product_id, warranty_period) VALUES (?, ?)",
                    (product.product_id, product.warranty_period),
                )
            elif isinstance(product, PerishableProduct):
                connection.execute(
                    "INSERT INTO Perishables (product_id, expiration_date) VALUES (?, ?)",
                    (product.product_id, product.expiration_date),
                )

    def delete_product(self, product_id: int) -> None:
        with self._get_connection() as connection:
            connection.execute("DELETE FROM Products WHERE product_id = ?", (product_id,))

    def update_stock(self, product_id: int, stock_quantity: int) -> None:
        with self._get_connection() as connection:
            connection.execute(
                "UPDATE Products SET stock_quantity = ? WHERE product_id = ?",
                (stock_quantity, product_id),
            )

    def insert_sale(self, product_id: int, quantity: int, total_amount: float) -> None:
        with self._get_connection() as connection:
            connection.execute(
                """
                INSERT INTO Sales (product_id, quantity, total_amount)
                VALUES (?, ?, ?)
                """,
                (product_id, quantity, total_amount),
            )

    def fetch_all_products(self) -> list[Product]:
        query = """
            SELECT p.product_id, p.name, p.price, p.stock_quantity, p.product_type,
                   e.warranty_period, pe.expiration_date
            FROM Products p
            LEFT JOIN Electronics e ON p.product_id = e.product_id
            LEFT JOIN Perishables pe ON p.product_id = pe.product_id
            ORDER BY p.product_id;
        """

        products: list[Product] = []
        with self._get_connection() as connection:
            rows = connection.execute(query).fetchall()

        for row in rows:
            if row["product_type"] == "electronics":
                products.append(
                    ElectronicsProduct(
                        product_id=row["product_id"],
                        name=row["name"],
                        price=row["price"],
                        stock_quantity=row["stock_quantity"],
                        warranty_period=row["warranty_period"],
                    )
                )
            elif row["product_type"] == "perishable":
                products.append(
                    PerishableProduct(
                        product_id=row["product_id"],
                        name=row["name"],
                        price=row["price"],
                        stock_quantity=row["stock_quantity"],
                        expiration_date=row["expiration_date"],
                    )
                )
            else:
                products.append(
                    Product(
                        product_id=row["product_id"],
                        name=row["name"],
                        price=row["price"],
                        stock_quantity=row["stock_quantity"],
                    )
                )

        return products

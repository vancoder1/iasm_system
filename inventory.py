from __future__ import annotations

from models import Product, Sale


class Inventory:
    def __init__(self) -> None:
        self._products: dict[int, Product] = {}

    @property
    def products(self) -> dict[int, Product]:
        return self._products

    def add_product(self, product: Product) -> None:
        if product.product_id in self._products:
            raise ValueError(f"Product ID {product.product_id} already exists.")
        self._products[product.product_id] = product

    def remove_product(self, product_id: int) -> None:
        if product_id not in self._products:
            raise ValueError(f"Product ID {product_id} was not found.")
        del self._products[product_id]

    def get_product(self, product_id: int) -> Product:
        if product_id not in self._products:
            raise ValueError(f"Product ID {product_id} was not found.")
        return self._products[product_id]

    def list_all_products(self) -> list[Product]:
        return list(self._products.values())


class InventoryService:
    def __init__(self, db_manager) -> None:
        self._db = db_manager
        self.inventory = Inventory()
        self.load_from_database()

    def load_from_database(self) -> None:
        self.inventory.products.clear()
        for product in self._db.fetch_all_products():
            self.inventory.add_product(product)

    def add_product(self, product: Product) -> None:
        self.inventory.add_product(product)
        self._db.insert_product(product)

    def remove_product(self, product_id: int) -> None:
        self.inventory.remove_product(product_id)
        self._db.delete_product(product_id)

    def get_product(self, product_id: int) -> Product:
        return self.inventory.get_product(product_id)

    def list_products(self) -> list[Product]:
        return self.inventory.list_all_products()

    def restock_product(self, product_id: int, quantity: int) -> Product:
        if quantity <= 0:
            raise ValueError("Restock quantity must be greater than zero.")
        product = self.inventory.get_product(product_id)
        product.update_stock(quantity)
        self._db.update_stock(product_id, product.stock_quantity)
        return product

    def sell_product(self, product_id: int, quantity: int) -> Sale:
        product = self.inventory.get_product(product_id)
        sale = Sale(product, quantity)
        self._db.update_stock(product_id, product.stock_quantity)
        self._db.insert_sale(product_id, sale.quantity, sale.total_amount)
        return sale

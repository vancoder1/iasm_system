from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Product:
    product_id: int
    name: str
    price: float
    stock_quantity: int

    def __post_init__(self) -> None:
        if self.price <= 0:
            raise ValueError("Price must be greater than zero.")
        if self.stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")

    def update_price(self, new_price: float) -> None:
        if new_price <= 0:
            raise ValueError("Price must be greater than zero.")
        self.price = float(new_price)

    def update_stock(self, quantity: int) -> None:
        updated_stock = self.stock_quantity + quantity
        if updated_stock < 0:
            raise ValueError("Stock cannot become negative.")
        self.stock_quantity = updated_stock

    def is_in_stock(self, quantity: int) -> bool:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        return self.stock_quantity >= quantity

    def sell(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if not self.is_in_stock(quantity):
            raise ValueError("Insufficient stock.")
        self.stock_quantity -= quantity

    def get_product_details(self) -> str:
        return (
            f"ID: {self.product_id} | Name: {self.name} | Price: ${self.price:.2f} "
            f"| Stock: {self.stock_quantity}"
        )


@dataclass
class ElectronicsProduct(Product):
    warranty_period: int

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.warranty_period < 0:
            raise ValueError("Warranty period cannot be negative.")

    def get_product_details(self) -> str:
        base = super().get_product_details()
        return f"{base} | Warranty: {self.warranty_period} months"


@dataclass
class PerishableProduct(Product):
    expiration_date: str

    def __post_init__(self) -> None:
        super().__post_init__()
        datetime.strptime(self.expiration_date, "%Y-%m-%d")

    def get_product_details(self) -> str:
        base = super().get_product_details()
        return f"{base} | Expiration: {self.expiration_date}"


class Sale:
    def __init__(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if not product.is_in_stock(quantity):
            raise ValueError("Insufficient stock.")

        self.product = product
        self.quantity = quantity
        self.total_amount = round(product.price * quantity, 2)
        self.product.sell(quantity)

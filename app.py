from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from db import DatabaseManager
from inventory import InventoryService
from models import ElectronicsProduct, PerishableProduct, Product


class InventoryApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Inventory and Sales Management System")
        self.root.geometry("900x450")

        self.db = DatabaseManager()
        self.inventory_service = InventoryService(self.db)

        self._build_ui()
        self.refresh_product_list()

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=12)
        container.pack(fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(container)
        button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))

        ttk.Button(button_frame, text="Add Product", width=22, command=self.add_product).pack(pady=4)
        ttk.Button(button_frame, text="Remove Product", width=22, command=self.remove_product).pack(pady=4)
        ttk.Button(button_frame, text="List Products", width=22, command=self.refresh_product_list).pack(pady=4)
        ttk.Button(button_frame, text="Sales Summary", width=22, command=self.show_summary).pack(pady=4)
        ttk.Button(button_frame, text="Sell Product", width=22, command=self.sell_product).pack(pady=4)
        ttk.Button(button_frame, text="Restock Product", width=22, command=self.restock_product).pack(pady=4)
        ttk.Button(button_frame, text="Exit", width=22, command=self.root.quit).pack(pady=20)

        table_frame = ttk.Frame(container)
        table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        columns = ("product_id", "name", "type", "price", "stock", "details")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)

        self.table.heading("product_id", text="ID")
        self.table.heading("name", text="Name")
        self.table.heading("type", text="Type")
        self.table.heading("price", text="Price")
        self.table.heading("stock", text="Stock")
        self.table.heading("details", text="Details")

        self.table.column("product_id", width=70, anchor=tk.CENTER)
        self.table.column("name", width=140)
        self.table.column("type", width=110, anchor=tk.CENTER)
        self.table.column("price", width=90, anchor=tk.E)
        self.table.column("stock", width=70, anchor=tk.CENTER)
        self.table.column("details", width=320)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _ask_required_string(self, prompt: str) -> str:
        value = simpledialog.askstring("Input", prompt, parent=self.root)
        if value is None:
            raise ValueError("Operation cancelled.")
        value = value.strip()
        if not value:
            raise ValueError("Value is required.")
        return value

    def _ask_required_int(self, prompt: str) -> int:
        value = simpledialog.askinteger("Input", prompt, parent=self.root)
        if value is None:
            raise ValueError("Operation cancelled.")
        return value

    def _ask_required_float(self, prompt: str) -> float:
        raw_value = simpledialog.askstring("Input", prompt, parent=self.root)
        if raw_value is None:
            raise ValueError("Operation cancelled.")
        try:
            return float(raw_value)
        except ValueError as error:
            raise ValueError("Please enter a valid number.") from error

    @staticmethod
    def _product_type(product: Product) -> str:
        if isinstance(product, ElectronicsProduct):
            return "Electronics"
        if isinstance(product, PerishableProduct):
            return "Perishable"
        return "General"

    @staticmethod
    def _product_extra_details(product: Product) -> str:
        if isinstance(product, ElectronicsProduct):
            return f"Warranty: {product.warranty_period} months"
        if isinstance(product, PerishableProduct):
            return f"Expires: {product.expiration_date}"
        return "-"

    def add_product(self) -> None:
        try:
            product_type = self._ask_required_string(
                "Product type (general/electronics/perishable):"
            ).lower()
            if product_type not in {"general", "electronics", "perishable"}:
                raise ValueError("Type must be general, electronics, or perishable.")

            product_id = self._ask_required_int("Product ID (integer):")
            name = self._ask_required_string("Product name:")
            price = self._ask_required_float("Product price (greater than 0):")
            stock_quantity = self._ask_required_int("Initial stock quantity:")

            if product_type == "electronics":
                warranty_period = self._ask_required_int("Warranty period (months):")
                product = ElectronicsProduct(
                    product_id=product_id,
                    name=name,
                    price=price,
                    stock_quantity=stock_quantity,
                    warranty_period=warranty_period,
                )
            elif product_type == "perishable":
                expiration_date = self._ask_required_string("Expiration date (YYYY-MM-DD):")
                product = PerishableProduct(
                    product_id=product_id,
                    name=name,
                    price=price,
                    stock_quantity=stock_quantity,
                    expiration_date=expiration_date,
                )
            else:
                product = Product(
                    product_id=product_id,
                    name=name,
                    price=price,
                    stock_quantity=stock_quantity,
                )

            self.inventory_service.add_product(product)
            self.refresh_product_list()
            messagebox.showinfo("Success", "Product added successfully.")
        except ValueError as error:
            messagebox.showerror("Input Error", str(error))
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def remove_product(self) -> None:
        try:
            product_id = self._ask_required_int("Enter product ID to remove:")
            self.inventory_service.remove_product(product_id)
            self.refresh_product_list()
            messagebox.showinfo("Success", "Product removed successfully.")
        except ValueError as error:
            messagebox.showerror("Input Error", str(error))
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def refresh_product_list(self) -> None:
        for row in self.table.get_children():
            self.table.delete(row)

        products = self.inventory_service.list_products()
        for product in products:
            self.table.insert(
                "",
                tk.END,
                values=(
                    product.product_id,
                    product.name,
                    self._product_type(product),
                    f"${product.price:.2f}",
                    product.stock_quantity,
                    self._product_extra_details(product),
                ),
            )

    def sell_product(self) -> None:
        try:
            product_id = self._ask_required_int("Enter product ID to sell:")
            quantity = self._ask_required_int("Enter quantity to sell:")

            sale = self.inventory_service.sell_product(product_id, quantity)
            self.refresh_product_list()
            messagebox.showinfo(
                "Sale Completed",
                f"Sale recorded. Total amount: ${sale.total_amount:.2f}",
            )
        except ValueError as error:
            messagebox.showerror("Input Error", str(error))
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def restock_product(self) -> None:
        try:
            product_id = self._ask_required_int("Enter product ID to restock:")
            quantity = self._ask_required_int("Enter quantity to add:")

            self.inventory_service.restock_product(product_id, quantity)
            self.refresh_product_list()
            messagebox.showinfo("Success", "Product restocked successfully.")
        except ValueError as error:
            messagebox.showerror("Input Error", str(error))
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def show_summary(self) -> None:
        try:
            total_sales, total_items, transaction_count = self.inventory_service.get_daily_sales_summary()
            messagebox.showinfo(
                "Daily Sales Summary",
                (
                    "Summary for today:\n"
                    f"Transactions: {transaction_count}\n"
                    f"Items sold: {total_items}\n"
                    f"Total sales: ${total_sales:.2f}"
                ),
            )
        except Exception as error:
            messagebox.showerror("Error", str(error))


def main() -> None:
    root = tk.Tk()
    InventoryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

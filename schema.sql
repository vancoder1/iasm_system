PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL CHECK (price > 0),
    stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0),
    product_type TEXT NOT NULL CHECK (product_type IN ('general', 'electronics', 'perishable'))
);

CREATE TABLE IF NOT EXISTS Electronics (
    product_id INTEGER PRIMARY KEY,
    warranty_period INTEGER NOT NULL CHECK (warranty_period >= 0),
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Perishables (
    product_id INTEGER PRIMARY KEY,
    expiration_date TEXT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    total_amount REAL NOT NULL CHECK (total_amount > 0),
    sale_date TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

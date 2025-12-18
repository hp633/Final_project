import sqlite3
import json
import os

DB_FILE = "db.sqlite"
JSON_FILE = "example_orders.json"

def init_db():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print("🗑 Old db.sqlite removed")

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        timestamp INTEGER,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )
    """)

    cur.execute("""
    CREATE TABLE order_items (
        order_id INTEGER,
        item_id INTEGER,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (item_id) REFERENCES items(id)
    )
    """)

    conn.commit()
    print("Database and tables created")

    if not os.path.exists(JSON_FILE):
        print(f"{JSON_FILE} not found. Skipping data load.")
        conn.close()
        return

    with open(JSON_FILE) as f:
        data = json.load(f)

    orders_data = data if isinstance(data, list) else [data]

    for order in orders_data:
        name = order.get("name")
        phone = order.get("phone")
        timestamp = order.get("timestamp")
        items = order.get("items", [])

        # Insert customer
        cur.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (name, phone))
        customer_id = cur.lastrowid

        # Insert order
        cur.execute("INSERT INTO orders (customer_id, timestamp) VALUES (?, ?)", (customer_id, timestamp))
        order_id = cur.lastrowid

        for item in items:
            item_name = item.get("name")
            price = item.get("price")

            # Check if item already exists to avoid duplicates
            cur.execute("SELECT id FROM items WHERE name=? AND price=?", (item_name, price))
            item_row = cur.fetchone()
            if item_row:
                item_id = item_row[0]
            else:
                cur.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item_name, price))
                item_id = cur.lastrowid

            # Link item to order
            cur.execute("INSERT INTO order_items (order_id, item_id) VALUES (?, ?)", (order_id, item_id))

    conn.commit()
    conn.close()
    print(f"All data from {JSON_FILE} inserted successfully")

if __name__ == "__main__":
    init_db()
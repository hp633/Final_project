import json
import sqlite3

def load_orders(conn):
    with open("example_orders.json") as f:
        orders = json.load(f)

    cur = conn.cursor()

    for order in orders:
        # insert or get customer
        cur.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", 
                    (order["name"], order.get("phone")))
        customer_id = cur.lastrowid

        # insert order
        cur.execute("INSERT INTO orders (customer_id, timestamp) VALUES (?, ?)", 
                    (customer_id, order["timestamp"]))
        order_id = cur.lastrowid

        # insert items
        for item in order["items"]:
            cur.execute("INSERT INTO items (name, price) VALUES (?, ?)", 
                        (item["name"], item["price"]))
            item_id = cur.lastrowid
            cur.execute("INSERT INTO order_items (order_id, item_id) VALUES (?, ?)", 
                        (order_id, item_id))

    conn.commit()
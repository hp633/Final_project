# Dosa Restaurant REST API - Final Project

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

DB_NAME = "db.sqlite"

app = FastAPI(title="Dosa Restaurant API")

# ------------------------
# Database Helper
# ------------------------
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# ------------------------
# Schemas
# ------------------------
class Customer(BaseModel):
    name: str
    email: str

class Item(BaseModel):
    name: str
    price: float

class Order(BaseModel):
    customer_id: int
    item_id: int
    quantity: int

@app.post("/customers", tags=["Customers"])
def create_customer(customer: Customer):
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO customers (name, email) VALUES (?, ?)",
            (customer.name, customer.email)
        )
        conn.commit()
        return {"id": cursor.lastrowid, **customer.dict()}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")
    finally:
        conn.close()

@app.get("/customers/{id}", tags=["Customers"])
def get_customer(id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Customer not found")
    return dict(row)

@app.put("/customers/{id}", tags=["Customers"])
def update_customer(id: int, customer: Customer):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE customers SET name = ?, email = ? WHERE id = ?",
        (customer.name, customer.email, id)
    )
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"id": id, **customer.dict()}

@app.delete("/customers/{id}", tags=["Customers"])
def delete_customer(id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted"}


@app.post("/items", tags=["Items"])
def create_item(item: Item):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO items (name, price) VALUES (?, ?)",
        (item.name, item.price)
    )
    conn.commit()
    conn.close()
    return {"id": cursor.lastrowid, **item.dict()}

@app.get("/items/{id}", tags=["Items"])
def get_item(id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Item not found")
    return dict(row)

@app.put("/items/{id}", tags=["Items"])
def update_item(id: int, item: Item):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE items SET name = ?, price = ? WHERE id = ?",
        (item.name, item.price, id)
    )
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": id, **item.dict()}

@app.delete("/items/{id}", tags=["Items"])
def delete_item(id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}


@app.post("/orders", tags=["Orders"])
def create_order(order: Order):
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orders (customer_id, item_id, quantity) VALUES (?, ?, ?)",
            (order.customer_id, order.item_id, order.quantity)
        )
        conn.commit()
        return {"id": cursor.lastrowid, **order.dict()}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Invalid customer or item ID")
    finally:
        conn.close()

@app.get("/orders/{id}", tags=["Orders"])
def get_order(id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Order not found")
    return dict(row)

@app.put("/orders/{id}", tags=["Orders"])
def update_order(id: int, order: Order):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE orders
        SET customer_id = ?, item_id = ?, quantity = ?
        WHERE id = ?
        """,
        (order.customer_id, order.item_id, order.quantity, id)
    )
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"id": id, **order.dict()}

@app.delete("/orders/{id}", tags=["Orders"])
def delete_order(id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted"}

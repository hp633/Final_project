# dosa.py
from fastapi import FastAPI
app = FastAPI()


import sqlite3

def count_customers():
    conn = sqlite3.connect("db.sqlite")  # should match the file in final_project
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM customers;")
    count = cur.fetchone()[0]
    conn.close()
    return count
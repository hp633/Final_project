\# Dosa Restaurant REST API



\## Project Overview

This project is a REST API backend for a fictional Dosa Restaurant, built using FastAPI and SQLite.

The API provides full CRUD (Create, Read, Update, Delete) functionality for customers, items,

and orders.



The application uses a relational SQLite database with primary and foreign key constraints to

maintain data integrity between customers, items, and orders.



---

\## Technologies Used

\- Python 3

\- FastAPI

\- SQLite

\- Uvicorn

\- Git / GitHub



---



\## Project Structure

exercise\_7/

├── main.py

├── init\_db.py

├── db.sqlite

├── example\_orders.json

└── README.md



---



\## Database Design



\### Customers Table

\- id (Primary Key)

\- name

\- email



\### Items Table

\- id (Primary Key)

\- name

\- price



\### Orders Table

\- id (Primary Key)

\- customer\_id (Foreign Key referencing Customers)

\- item\_id (Foreign Key referencing Items)

\- quantity



---



\## Setup Instructions



\### 1. Install Dependencies

Run the following command to install required packages:



py -m pip install fastapi uvicorn



---



\### 2. Initialize the Database

This script creates the SQLite database and populates it using example\_orders.json.



py init\_db.py



---



\### 3. Run the Application

Start the FastAPI server using:



py -m uvicorn main:app --reload



---



\### 4. API Documentation

Open a browser and go to:



http://127.0.0.1:8000/docs



Swagger UI provides interactive documentation for all available endpoints.



---



\## API Endpoints



\### Customers

\- POST /customers

\- GET /customers/{id}

\- PUT /customers/{id}

\- DELETE /customers/{id}



\### Items

\- POST /items

\- GET /items/{id}

\- PUT /items/{id}

\- DELETE /items/{id}



\### Orders

\- POST /orders

\- GET /orders/{id}

\- PUT /orders/{id}

\- DELETE /orders/{id}



---



\## Version Control

This project is hosted on GitHub and uses Git for version control.

The repository contains multiple commits demonstrating incremental development progress.



---



\## Author

Hinal Prabhu

IS 601 – Final Project




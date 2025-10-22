# HYPECULTURE 👟

**HYPECULTURE** is a command-line interface (CLI) application that simulates a complete marketplace for shoe reselling, built entirely with Python and MySQL. It's a "StockX" or "Amazon for shoes" built on a robust SQL backend, managing users, products, inventory, and orders from end to end.

This project was built as a comprehensive demonstration of database management principles, including relational schema design, SQL transactions, procedures, triggers (if added), and a multi-user application interface.


---

## ✨ Core Features

The application supports three distinct user roles, each with its own set of permissions and functionalities.

### 👤 Customer
* Log in and maintain a persistent session.
* Browse shoes by category (Sneakers, Boots, etc.).
* View all sellers for a specific shoe, sorted with the cheapest price first.
* Add items to an accumulating shopping cart.
* View and manage the shopping cart.
* Complete a full checkout process by providing shipping details.
* View a detailed history of all past orders.

### 💼 Seller
* Log in and manage their personal inventory.
* View all current listings.
* Add a new listing for a product that exists in the master catalog.
* Update the price or stock quantity for an existing listing.
* Remove a listing from the marketplace.

### 👑 Admin
* Log in to the system's management panel.
* View all users, products, and orders in the database.
* **Add new products** to the master product catalog.
* **Add new users** (customers or sellers) to the system.
* **Remove users** (sellers or customers) from the system.

---

## 💻 Tech Stack

* **Frontend (Interface):** Python 3
* **Backend (Database):** MySQL
* **Connector:** `mysql-connector-python`

---

## 🚀 How to Run

For detailed, step-by-step instructions on how to set up the database and run the application, please see the **[SETUP.md](SETUP.md)** file.

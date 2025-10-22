# 🚀 HYPECULTURE Setup Guide

Follow these steps to get the HYPECULTURE application running on your local machine.

---

## 1. Prerequisites

Before you begin, ensure you have the following software installed:

* **Python 3:** (You have this)
* **MySQL Server:** (You have this)
* **MySQL Workbench:** (Optional, but recommended for managing the database)

---

## 2. Set Up the Database

This is the most important step. You must create and populate the database for the app to work.

1.  **Start Your MySQL Server:**
    * Open **System Settings** > **MySQL** and click "Start MySQL Server".
    * *Alternatively, via Terminal (if you used the official installer):*
        ```bash
        sudo /usr/local/mysql/support-files/mysql.server start
        ```

2.  **Run the SQL Script:**
    * Open **MySQL Workbench** and connect to your local server.
    * Open the `hypeculture_db.sql` file (or whichever file contains your final `CREATE TABLE` and `INSERT` statements).
    * Execute the **entire script** (using the ⚡️ icon). This will create the `hypeculture_db` database, all the tables, and insert your sample users and products.

---

## 3. Set Up the Python Environment

1.  **Navigate to the Project Folder:**
    Open your terminal and `cd` into the `hypeculture` project directory.
    ```bash
    cd /path/to/your/hypeculture
    ```

2.  **Activate Your Virtual Environment:**
    You've already set one up, so just activate it:
    ```bash
    source .venv/bin/activate
    ```

3.  **Install the Required Library:**
    If you haven't already, install the MySQL connector:
    ```bash
    pip install mysql-connector-python
    ```

---

## 4. Configure the Connection

The Python app needs to know your MySQL password.

1.  Open the **`db_connector.py`** file in your code editor.
2.  Update the `password` field to match your MySQL `root` password:
    ```python
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_ACTUAL_PASSWORD_HERE",  # <-- UPDATE THIS LINE
        database="hypeculture_db"
    )
    ```
3.  Save the file.

---

## 5. Run the Application

You're all set! Run the main Python file from your terminal:

```bash
python main.py

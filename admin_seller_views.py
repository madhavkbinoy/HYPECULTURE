# admin_seller_views.py (Final Version with all features)

# NEW FUNCTION to add a product to the master catalog
def add_new_product(connection):
    """ Helper function for admin to add a new product to the Products table. """
    cursor = connection.cursor()
    try:
        print("\n--- Add New Product to Catalog ---")
        
        # First, show the available categories so the admin knows which ID to use
        cursor.execute("SELECT category_id, category_name FROM Categories")
        categories = cursor.fetchall()
        print("Available Categories:")
        for cat_id, cat_name in categories:
            print(f"  ID: {cat_id}, Name: {cat_name}")

        product_name = input("Enter new product name (e.g., New Balance 550): ")
        brand = input("Enter brand name: ")
        category_id = input("Enter the category_id for this product: ")

        if not all([product_name, brand, category_id]):
            print("All fields are required.")
            return

        query = "INSERT INTO Products (product_name, brand, category_id) VALUES (%s, %s, %s)"
        cursor.execute(query, (product_name, brand, int(category_id)))
        connection.commit()
        print(f"✅ Product '{product_name}' added to the catalog successfully.")

    except Exception as e:
        print(f"❌ Error adding product: {e}")
        connection.rollback()
    finally:
        cursor.close()


def add_new_user(connection):
    """ Helper function for admin to add a new user. """
    cursor = connection.cursor()
    try:
        print("\n--- Add New User ---")
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        role = input("Enter role ('customer' or 'seller'): ").lower()

        if role not in ['customer', 'seller']:
            print("Invalid role. Please choose 'customer' or 'seller'.")
            return

        if not all([first_name, last_name, email, password, role]):
            print("All fields are required.")
            return

        query = "INSERT INTO Users (first_name, last_name, email, password_hash, user_role) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (first_name, last_name, email, password, role))
        connection.commit()
        print(f"✅ User '{email}' created successfully as a '{role}'.")

    except Exception as e:
        print(f"❌ Error adding user: {e}")
        connection.rollback()
    finally:
        cursor.close()

def remove_user(connection):
    """ Helper function for admin to remove a user. """
    cursor = connection.cursor()
    try:
        print("\n--- Remove User ---")
        user_id_to_remove = input("Enter the user_id to remove: ")
        
        query = "DELETE FROM Users WHERE user_id = %s"
        cursor.execute(query, (int(user_id_to_remove),))

        if cursor.rowcount > 0:
            connection.commit()
            print(f"✅ User with ID {user_id_to_remove} has been removed.")
        else:
            print("User ID not found.")

    except Exception as e:
        print(f"❌ Error removing user: {e}")
        print("  (Note: You cannot remove a user who has existing orders or inventory listings.)")
        connection.rollback()
    finally:
        cursor.close()


def show_admin_menu(connection):
    """ Main menu for the admin. """
    while True:
        print("\n--- 👑 Admin Menu ---")
        print("1. View All Users")
        print("2. View All Products in Master Catalog")
        print("3. View All Orders")
        print("4. Add New Product to Catalog")    # NEW
        print("5. Add New User")                  # Re-numbered
        print("6. Remove User")                   # Re-numbered
        print("7. Logout")                        # Re-numbered
        choice = input("Enter your choice: ")
        
        if choice == '1':
            cursor = connection.cursor()
            cursor.execute("SELECT user_id, first_name, last_name, email, user_role FROM Users")
            users = cursor.fetchall()
            print("\n--- All Users ---")
            for uid, fname, lname, email, role in users:
                print(f"ID: {uid}, Name: {fname} {lname}, Email: {email}, Role: {role}")
            cursor.close()
        elif choice == '2':
            cursor = connection.cursor()
            cursor.execute("SELECT product_id, product_name, brand, category_id FROM Products")
            products = cursor.fetchall()
            print("\n--- All Products ---")
            for pid, name, brand, cid in products:
                print(f"ID: {pid}, Name: {name}, Brand: {brand}, Category ID: {cid}")
            cursor.close()
        elif choice == '3':
            cursor = connection.cursor()
            cursor.execute("SELECT order_id, customer_id, total_amount, order_status, order_date FROM Orders")
            orders = cursor.fetchall()
            print("\n--- All Orders ---")
            for oid, cid, total, status, date in orders:
                print(f"ID: {oid}, CustomerID: {cid}, Total: ${total:.2f}, Status: {status}, Date: {date}")
            cursor.close()
        elif choice == '4':
            add_new_product(connection)
        elif choice == '5':
            add_new_user(connection)
        elif choice == '6':
            remove_user(connection)
        elif choice == '7':
            print("Logging out...")
            break
        else:
            print("Invalid choice.")


def show_seller_menu(connection, user_id):
    """ Main menu for the seller, updated for the new schema and features. """
    while True:
        print("\n--- 💼 Seller Menu ---")
        print("1. View My Listings")
        print("2. Add New Listing")
        print("3. Update a Listing (Stock/Price)")
        print("4. Remove a Listing")
        print("5. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            cursor = connection.cursor()
            try:
                query = """
                SELECT i.inventory_id, p.product_name, i.price, i.stock_quantity
                FROM Inventory AS i
                JOIN Products AS p ON i.product_id = p.product_id
                WHERE i.seller_id = %s;
                """
                cursor.execute(query, (user_id,))
                listings = cursor.fetchall()
                print("\n--- My Listings ---")
                for inv_id, name, price, stock in listings:
                    print(f"Inventory ID: {inv_id} | {name} | Price: ${price:.2f} | Stock: {stock}")
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                cursor.close()

        elif choice == '2':
            cursor = connection.cursor()
            try:
                prod_id = input("Enter the Master Product ID to list: ")
                price = input("Enter your price: ")
                stock = input("Enter stock quantity: ")
                cursor.execute(
                    "INSERT INTO Inventory (seller_id, product_id, price, stock_quantity) VALUES (%s, %s, %s, %s)",
                    (user_id, int(prod_id), float(price), int(stock))
                )
                connection.commit()
                print("✅ Listing added successfully!")
            except Exception as e:
                print(f"Error adding listing: {e}")
                connection.rollback()
            finally:
                cursor.close()

        elif choice == '3':
            cursor = connection.cursor()
            try:
                listing_id = input("Enter Inventory ID to update: ")
                new_price = input("Enter new price (leave blank to skip): ")
                new_stock = input("Enter new stock (leave blank to skip): ")
                
                if new_price.strip():
                    cursor.execute("UPDATE Inventory SET price = %s WHERE inventory_id = %s AND seller_id = %s",
                                 (float(new_price), int(listing_id), user_id))
                if new_stock.strip():
                    cursor.execute("UPDATE Inventory SET stock_quantity = %s WHERE inventory_id = %s AND seller_id = %s",
                                 (int(new_stock), int(listing_id), user_id))
                
                connection.commit()
                print("✅ Listing updated!")
            except Exception as e:
                 print(f"Error updating listing: {e}")
                 connection.rollback()
            finally:
                cursor.close()

        elif choice == '4':
            cursor = connection.cursor()
            try:
                listing_id = input("Enter Inventory ID of the listing to remove: ")
                # The 'AND seller_id = %s' is a crucial security check
                query = "DELETE FROM Inventory WHERE inventory_id = %s AND seller_id = %s"
                cursor.execute(query, (int(listing_id), user_id))
                
                if cursor.rowcount > 0:
                    connection.commit()
                    print(f"✅ Listing with ID {listing_id} has been removed.")
                else:
                    print("Listing ID not found or you do not have permission to remove it.")
            except Exception as e:
                print(f"Error removing listing: {e}")
                connection.rollback()
            finally:
                cursor.close()

        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice.")
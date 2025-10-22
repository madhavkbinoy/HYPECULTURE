# customer_view.py (Corrected Version)
import time

def show_customer_menu(connection, user_id):
    """ Main menu for the logged-in customer. """
    while True:
        print("\n--- 👟 Customer Menu ---")
        print("1. Browse Products by Category")
        print("2. View My Cart")
        print("3. Checkout")
        print("4. View My Order History")
        print("5. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            browse_products(connection, user_id)
        elif choice == '2':
            view_cart(connection, user_id)
        elif choice == '3':
            checkout(connection, user_id)
        elif choice == '4':
            view_order_history(connection, user_id)
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def browse_products(connection, user_id):
    """ Allows customer to browse categories and then products. """
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT category_id, category_name FROM Categories")
        categories = cursor.fetchall()
        print("\n--- Select a Category ---")
        for cat_id, cat_name in categories:
            print(f"{cat_id}. {cat_name}")

        chosen_cat_id = int(input("Enter category number: "))
        if not any(c[0] == chosen_cat_id for c in categories):
            print("Invalid category.")
            return

        query = "SELECT product_id, product_name FROM Products WHERE category_id = %s"
        cursor.execute(query, (chosen_cat_id,))
        products = cursor.fetchall()
        print(f"\n--- Shoes in {dict(categories)[chosen_cat_id]} ---")
        for prod_id, prod_name in products:
            print(f"{prod_id}. {prod_name}")
        
        chosen_prod_id = int(input("Enter shoe number to see sellers: "))
        if not any(p[0] == chosen_prod_id for p in products):
            print("Invalid shoe.")
            return
        
        view_product_sellers(connection, user_id, chosen_prod_id)

    except (ValueError, TypeError):
        print("Invalid input. Please enter a number.")
    finally:
        cursor.close()

def view_product_sellers(connection, user_id, product_id):
    """ View sellers for a specific product, cheapest first. """
    cursor = connection.cursor()
    try:
        query = """
        SELECT sp.inventory_id, u.first_name, u.last_name, sp.price, sp.stock_quantity
        FROM Inventory sp
        JOIN Users u ON sp.seller_id = u.user_id
        WHERE sp.product_id = %s AND sp.stock_quantity > 0
        ORDER BY sp.price ASC;
        """
        cursor.execute(query, (product_id,))
        sellers = cursor.fetchall()
    finally:
        cursor.close()

    if not sellers:
        print("Sorry, this product is currently out of stock or not sold.")
        return

    print("\n--- Sellers for this Shoe (Cheapest First) ---")
    cheapest_seller = sellers[0]
    print(f"**Best Price**: ${cheapest_seller[3]:.2f} from {cheapest_seller[1]} {cheapest_seller[2]} (Stock: {cheapest_seller[4]})")

    while True:
        print("\nOptions:")
        print("1. Add to Cart (Best Price)")
        print("2. View all sellers")
        print("3. Back to main menu")
        choice = input("Enter your choice: ")
        if choice == '1':
            add_to_cart(connection, user_id, cheapest_seller[0])
            break
        elif choice == '2':
            print("\n--- All Available Sellers ---")
            for i, seller in enumerate(sellers):
                print(f"{i+1}. Seller: {seller[1]} {seller[2]}, Price: ${seller[3]:.2f}, Stock: {seller[4]}")
            
            try:
                seller_choice = int(input("Enter seller number to add to cart (or 0 to go back): "))
                if 1 <= seller_choice <= len(sellers):
                    add_to_cart(connection, user_id, sellers[seller_choice-1][0])
                    break
                elif seller_choice == 0:
                    continue
                else:
                    print("Invalid seller number.")
            except ValueError:
                print("Invalid input.")
        elif choice == '3':
            break
        else:
            print("Invalid choice.")

def add_to_cart(connection, user_id, inventory_id):
    """ Adds a selected product from a seller to the user's cart. """
    cursor = connection.cursor()
    try:
        quantity = int(input("Enter quantity: "))
        if quantity <= 0:
            print("Quantity must be positive.")
            return

        cursor.execute(
            "SELECT cart_id, quantity FROM Cart WHERE customer_id = %s AND inventory_id = %s",
            (user_id, inventory_id)
        )
        item = cursor.fetchone()

        if item:
            cart_id, current_quantity = item
            new_quantity = current_quantity + quantity
            cursor.execute("UPDATE Cart SET quantity = %s WHERE cart_id = %s", (new_quantity, cart_id))
        else:
            cursor.execute(
                "INSERT INTO Cart (customer_id, inventory_id, quantity) VALUES (%s, %s, %s)",
                (user_id, inventory_id, quantity)
            )
        
        connection.commit()
        print("✅ Item added to cart successfully!")

    except ValueError:
        print("Invalid quantity.")
    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
    finally:
        cursor.close()

def view_cart(connection, user_id):
    """ Displays the contents of the user's cart, updated for the new schema. """
    cursor = connection.cursor()
    query = """
    SELECT
        p.product_name,
        u.first_name AS seller_name,
        i.price,
        c.quantity,
        (i.price * c.quantity) AS subtotal
    FROM
        Cart AS c
    JOIN
        Inventory AS i ON c.inventory_id = i.inventory_id
    JOIN
        Products AS p ON i.product_id = p.product_id
    JOIN
        Users AS u ON i.seller_id = u.user_id
    WHERE
        c.customer_id = %s;
    """
    try:
        cursor.execute(query, (user_id,))
        cart_items = cursor.fetchall()
        
        if not cart_items:
            print("\nYour cart is empty.")
            return
            
        print("\n--- 🛒 Your Shopping Cart ---")
        total = 0
        for name, seller, price, qty, subtotal in cart_items:
            print(f"- {name} (Sold by {seller}) | Qty: {qty} @ ${price:.2f} each | Subtotal: ${subtotal:.2f}")
            total += subtotal
        print("---------------------------------")
        print(f"TOTAL: ${total:.2f}")

    except Exception as e:
        print(f"An error occurred while viewing cart: {e}")
    finally:
        cursor.close()

def checkout(connection, user_id):
    """ Guides the user through the checkout process using a transaction. """
    cursor = connection.cursor(buffered=True) # Buffered cursor is good for multiple queries

    try:
        # 1. Get all cart items for the user
        cart_query = """
        SELECT c.inventory_id, c.quantity, i.price, i.stock_quantity
        FROM Cart c JOIN Inventory i ON c.inventory_id = i.inventory_id
        WHERE c.customer_id = %s;
        """
        cursor.execute(cart_query, (user_id,))
        cart_items = cursor.fetchall()

        if not cart_items:
            print("\nYour cart is empty. Nothing to check out.")
            return

        # 2. Check if there is enough stock for all items BEFORE starting
        total_amount = 0
        for inv_id, qty, price, stock in cart_items:
            if qty > stock:
                print(f"❌ Checkout failed: Not enough stock for item ID {inv_id}. Only {stock} left.")
                return
            total_amount += (qty * price)
        
        print(f"\nYour order total is: ${total_amount:.2f}")

        # 3. Get shipping details from the user
        print("Please enter your shipping details:")
        address_line = input("Address Line 1: ")
        city = input("City: ")
        state = input("State: ")
        postal_code = input("Postal Code: ")
        
        if not all([address_line, city, state, postal_code]):
            print("All fields are required. Checkout cancelled.")
            return

        confirm = input("Confirm and 'Pay Now'? (y/n): ").lower()
        if confirm != 'y':
            print("Checkout cancelled.")
            return

        # --- START TRANSACTION ---
        # 4. Create a new address entry
        cursor.execute(
            "INSERT INTO Addresses (user_id, address_line1, city, state, postal_code) VALUES (%s, %s, %s, %s, %s)",
            (user_id, address_line, city, state, postal_code)
        )
        address_id = cursor.lastrowid

        # 5. Create the main order entry
        cursor.execute(
            "INSERT INTO Orders (customer_id, address_id, total_amount) VALUES (%s, %s, %s)",
            (user_id, address_id, total_amount)
        )
        order_id = cursor.lastrowid

        # 6. Loop through cart items again to create OrderItems and update stock
        for inv_id, qty, price, stock in cart_items:
            # Add to OrderItems
            cursor.execute(
                "INSERT INTO OrderItems (order_id, inventory_id, quantity, price_per_unit) VALUES (%s, %s, %s, %s)",
                (order_id, inv_id, qty, price)
            )
            # Update stock in Inventory
            new_stock = stock - qty
            cursor.execute("UPDATE Inventory SET stock_quantity = %s WHERE inventory_id = %s", (new_stock, inv_id))

        # 7. Clear the user's cart
        cursor.execute("DELETE FROM Cart WHERE customer_id = %s", (user_id,))
        
        # --- COMMIT TRANSACTION ---
        connection.commit()
        print(f"\nProcessing payment...")
        time.sleep(1)
        print(f"✅ Payment successful! Your order #{order_id} has been placed.")

    except Exception as e:
        # --- ROLLBACK TRANSACTION ---
        connection.rollback()
        print(f"❌ An error occurred during checkout: {e}. The transaction has been rolled back.")
    finally:
        cursor.close()
        

def view_order_history(connection, user_id):
    """ Displays the user's past orders and the items in each order. """
    cursor = connection.cursor()
    try:
        # First, get all orders for this user
        orders_query = """
        SELECT o.order_id, o.order_date, o.total_amount, a.address_line1, a.city
        FROM Orders o JOIN Addresses a ON o.address_id = a.address_id
        WHERE o.customer_id = %s ORDER BY o.order_date DESC;
        """
        cursor.execute(orders_query, (user_id,))
        orders = cursor.fetchall()

        if not orders:
            print("\nYou have no past orders.")
            return

        print("\n--- 📜 Your Order History ---")
        for order_id, date, total, address, city in orders:
            print(f"\nOrder #{order_id} | Date: {date.strftime('%Y-%m-%d')} | Total: ${total:.2f}")
            print(f"  Shipped to: {address}, {city}")
            
            # Now, for each order, get its items
            items_query = """
            SELECT p.product_name, u.first_name AS seller_name, oi.quantity, oi.price_per_unit
            FROM OrderItems oi
            JOIN Inventory i ON oi.inventory_id = i.inventory_id
            JOIN Products p ON i.product_id = p.product_id
            JOIN Users u ON i.seller_id = u.user_id
            WHERE oi.order_id = %s;
            """
            # Use a new cursor for this nested query
            item_cursor = connection.cursor()
            item_cursor.execute(items_query, (order_id,))
            items = item_cursor.fetchall()
            item_cursor.close()

            for name, seller, qty, price in items:
                print(f"  - {name} (Sold by {seller}) | Qty: {qty} @ ${price:.2f} each")

    except Exception as e:
        print(f"An error occurred while fetching order history: {e}")
    finally:
        cursor.close()
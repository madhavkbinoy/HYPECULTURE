#main.py
from db_connector import create_connection
from customer_view import show_customer_menu
from admin_seller_views import show_admin_menu, show_seller_menu

def login(connection, cursor):
    """ Handles the user login process. """
    print("\n--- Welcome to HYPEculture Login ---")

    ch = input("Are you a new user? (y/n): ").lower()
    if ch == 'y':
        print("Please enter your details to register.")
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        insert_query = "INSERT INTO Users (first_name, last_name, email, password_hash, user_role) VALUES (%s, %s, %s, %s, %s)"
        try:
            cursor.execute(insert_query, (first_name, last_name, email, password, 'customer'))
            connection.commit()
            print("Registration successful! You are now logged in.")
            user_id = cursor.lastrowid
            return (user_id, 'customer', first_name)
        except Exception as e:
            print(f"An error occurred during registration: {e}")
            return None

    # This part handles login for existing users
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    query = "SELECT user_id, user_role, first_name FROM Users WHERE email = %s AND password_hash = %s"
    user = None
    try:
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
    except Exception as e:
        print(f"An error occurred during login: {e}")

    return user

def main():
    """ Main function to run the application. """
    connection = create_connection()
    if not connection:
        return

    cursor = connection.cursor()

    print("=" * 40)
    print("👟 WELCOME TO HYPECULTURE 👟")
    print("     Your Ultimate Shoe Marketplace")
    print("=" * 40)

    while True:
        user_data = login(connection, cursor)

        if user_data:
            user_id, role, name = user_data
            print(f"\nWelcome back, {name}!")

            if role == 'customer':
                show_customer_menu(connection, user_id)
            elif role == 'seller':
                show_seller_menu(connection, user_id)
            elif role == 'admin':
                show_admin_menu(connection)
        else:
            print("Login failed. Invalid email or password.")

        cont = input("\nReturn to login screen? (y/n): ").lower()
        if cont != 'y':
            break

    cursor.close()
    connection.close()
    print("Thank you for using HYPECULTURE. Goodbye!")

if __name__ == "__main__":
    main()

# main.py
from db_connector import create_connection
from customer_view import show_customer_menu
from admin_seller_views import show_admin_menu, show_seller_menu

def login(cursor):
    """ Handles the user login process. """
    print("\n--- Welcome to HYPEculture Login ---")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    # This query now checks the password the user actually types
    query = "SELECT user_id, user_role, first_name FROM Users WHERE email = %s AND password_hash = %s"

    try:
        # Pass both the email and password to the query
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
    except Exception as e:
        print(f"An error occurred during login: {e}")
        user = None

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
        user_data = login(cursor)
        
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
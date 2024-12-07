import pymysql as sql
from time import sleep
from datetime import datetime
import pyfiglet
from termcolor import colored
import sys
import os

# Global variable to store logged-in user's info (userId and userName)
logged_user = None

# Helper function to print banners with ASCII art and color
def print_banner(text, color='cyan'):
    ascii_banner = pyfiglet.figlet_format(text, font='slant')  # Use 'slant' for an even cooler font
    print(colored(ascii_banner, color))

# Cool typing animation for prompts
def typing_animation(text, delay=0.05):
    for char in text:
        print(char, end="", flush=True)
        sleep(delay)
    print()

# Fancy loading animation with a cool rotating spinner
def loading_animation(message="LOADING...", symbol='*', duration=5):
    symbols = ['|', '/', '-', '\\']
    print(colored(f"\n{message}", 'yellow'))
    for _ in range(duration):
        for symbol in symbols:
            print(f"{message} {symbol}", end="", flush=True)
            sleep(0.2)
            print("\r", end="", flush=True)
    print("\n" + colored("Done!", 'green'))

# Start function (Intro text)
def start():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal (Windows or Mac/Linux)
    print_banner("LIBRARY MANAGEMENT SYSTEM", 'yellow')
    print("="*50)
    typing_animation("Connecting to the MySQL database...")
    loading_animation("Connecting", symbol="~")
    Connection()

# Connection to MySQL database
def Connection():
    print(colored("\nCONNECTING TO MYSQL . . .", 'green'))
    try:
        con = sql.connect(host="localhost", user="root", passwd="1928374655", database="library")
    except sql.MySQLError as e:
        print(colored(f"Error: {e}", 'red'))
        print("="*50)
        print("'1' to reconnect\n'2' to exit")
        try:
            user_in = int(input("Enter the command >"))
        except ValueError:
            print(colored("INVALID INPUT, EXITING PROGRAM . . .", 'red'))
            exit()
        if user_in == 1:
            print("RECONNECTING . . .")
            loading_animation("Reconnecting", symbol="*")
            Connection()
        elif user_in == 2:
            exiting()
        else:
            print(colored("INVALID INPUT, EXITING PROGRAM . . .", 'red'))
            exit()
    
    if con:
        print(colored("CONNECTED SUCCESSFULLY!", 'green'))
        login(con)

# Exiting the program gracefully
def exiting():
    print_banner("EXITING THE PROGRAM", 'red')
    sleep(1)
    sys.exit()

# Login function with enhanced UI
def login(con):
    global logged_user
    cur = con.cursor()
    print("="*50)
    print(colored("LOG IN", 'magenta'))
    print(colored("\nEnter your credentials:", 'cyan'))
    print("\nuserId 3| userName Admin| password 1234|\n")
    print("'1' to log in")
    print("'2' to create account")
    print("'3' to exit")
    print("WARNING: Invalid input results in exiting the program!")

    try:
        user_com = int(input("Enter command> "))
    except ValueError:
        print(colored("INVALID INPUT, EXITING PROGRAM . . .", 'red'))
        exit()

    if user_com == 1:
        name = input("Enter your name: ")
        passw = input("Enter your password: ")

        cur.execute(f"SELECT * FROM users WHERE userName='{name}' AND password='{passw}'")
        user = cur.fetchone()

        if user:
            logged_user = {'userId': user[0], 'userName': user[1]}  # Store logged user info
            typing_animation(f"Welcome {logged_user['userName']}!", delay=0.05)
            if user[5] == 'admin':
                usr_admin(cur)
            else:
                usr_customer(cur)
        else:
            print(colored("No user found with the given credentials.", 'red'))
            login(con)

    elif user_com == 2:
        create_acc(cur)
    elif user_com == 3:
        exiting()

# Create a new account with cool form and validation
def create_acc(cur):
    print("\nCreate Account")
    print("="*50)
    name = input("Enter your name (required): ")
    phnum = input("Enter your phone number (optional): ")
    email = input("Enter your email (required): ")
    passwd = input("Create your password (required): ")

    if not name or not email or not passwd:
        print(colored("WARNING: Required fields are missing!", 'red'))
        login(cur)
    else:
        cur.execute("SELECT COUNT(*) FROM users")
        user_id = cur.fetchone()[0] + 1
        try:
            cur.execute(f"INSERT INTO users (userId, userName, phoneNumber, emailId, password, adminStatus) VALUES ({user_id}, '{name}', '{phnum}', '{email}', '{passwd}', 'not admin')")
            print(colored("Account created successfully!", 'green'))
            loading_animation("Creating Account", symbol="~")
            cur.connection.commit()
            login(cur)  # Log the user in after account creation
        except sql.MySQLError as e:
            print(colored(f"ERROR: {e}", 'red'))
            login(cur)

# Admin Panel
def usr_admin(cur):
    print_banner("ADMIN PANEL", 'magenta')
    while True:
        print("="*50)
        print(colored("WELCOME ADMIN", 'yellow'))
        print("'1' to manage books")
        print("'2' to manage issued books")
        print("'3' to manage users")
        print("'4' to log out")

        try:
            option = int(input("Choose an option> "))
        except ValueError:
            print(colored("Invalid input! Returning to admin panel...", 'red'))
            continue

        if option == 1:
            manage_books(cur)
        elif option == 2:
            manage_issued_books(cur)
        elif option == 3:
            manage_users(cur)
        elif option == 4:
            exiting()
        else:
            print(colored("Invalid option! Returning to admin panel...", 'red'))

# Manage Books
def manage_books(cur):
    print_banner("BOOK MANAGEMENT", 'cyan')
    while True:
        print("="*50)
        print("'1' to view all books")
        print("'2' to add a new book")
        print("'3' to delete a book")
        print("'4' to return to admin panel")

        try:
            option = int(input("Choose an option> "))
        except ValueError:
            print(colored("Invalid input! Returning to admin panel...", 'red'))
            return

        if option == 1:
            view_books(cur)
        elif option == 2:
            add_book(cur)
        elif option == 3:
            delete_book(cur)
        elif option == 4:
            break  # Return to admin panel
        else:
            print(colored("Invalid option. Returning to admin panel...", 'red'))

# View books
def view_books(cur):
    print(colored("\nFetching all books...", 'yellow'))
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    if books:
        print(colored("\nID | Book Name | Author | Year | Quantity", 'cyan'))
        for book in books:
            print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]}")
    else:
        print(colored("No books found.", 'red'))

# Add book
def add_book(cur):
    print(colored("\nEnter the book details:", 'cyan'))
    name = input("Book Name: ")
    author = input("Author: ")
    year = input("Publication Year: ")
    quantity = input("Quantity: ")
    try:
        cur.execute(f"INSERT INTO books (bookName, author, year, quantity) VALUES ('{name}', '{author}', {year}, {quantity})")
        cur.connection.commit()
        print(colored(f"\nBook '{name}' added successfully!", 'green'))
    except sql.MySQLError as e:
        print(colored(f"ERROR: {e}", 'red'))


# Customer Panel
def usr_customer(cur):
    while True:
        print("="*50)
        print("WELCOME USER")
        print("'1' to view all books")
        print("'2' to borrow a book")
        print("'3' to return a book")
        print("'4' to log out")

        try:
            option = int(input("Choose an option> "))
        except ValueError:
            print("Invalid input! Returning to user panel...")
            continue

        if option == 1:
            view_books(cur)
        elif option == 2:
            issue_book(cur)
        elif option == 3:
            return_book(cur)
        elif option == 4:
            exiting()
        else:
            print("Invalid option! Returning to user panel...")

# Issue a book to a user (using logged userId automatically)
def issue_book(cur):
    book_id = input("Enter book ID to issue: ")
    issue_date = datetime.now().strftime('%Y-%m-%d')
    issue_time = datetime.now().strftime('%H:%M:%S')

    # Check if the book is available
    cur.execute(f"SELECT issueStatus FROM books WHERE bookId = {book_id}")
    book_status = cur.fetchone()

    if book_status and book_status[0] == "not issued":
        # Update book status and insert into issuedbooksdetails
        cur.execute(f"UPDATE books SET issueStatus = 'issued', issuedUserId = {logged_user['userId']}, issueDate = '{issue_date}', issueTime = '{issue_time}' WHERE bookId = {book_id}")
        cur.execute(f"INSERT INTO issuedbooksdetails (userId, bookId, bookName, issueDate, issueTime, fineInRs) SELECT {logged_user['userId']}, bookId, bookName, '{issue_date}', '{issue_time}', 0 FROM books WHERE bookId = {book_id}")
        print("Book issued successfully!")
        cur.connection.commit()
    else:
        print("This book is already issued or does not exist.")

# Return an issued book
def return_book(cur):
    book_id = input("Enter book ID to return: ")
    return_date = datetime.now().strftime('%Y-%m-%d')
    return_time = datetime.now().strftime('%H:%M:%S')

    # Check if the book is issued to the user
    cur.execute(f"SELECT issuedUserId FROM books WHERE bookId = {book_id}")
    issued_user = cur.fetchone()

    if issued_user and issued_user[0] == logged_user['userId']:
        # Update book status to "not issued" and insert return details
        cur.execute(f"UPDATE books SET issueStatus = 'not issued', issuedUserId = NULL, returnDate = '{return_date}', returnTime = '{return_time}' WHERE bookId = {book_id}")
        print("Book returned successfully!")
        cur.connection.commit()
    else:
        print("This book is not issued to you or does not exist.")

# Delete a book
def delete_book(cur):
    book_id = input("Enter book ID to delete: ")
    query = f"DELETE FROM books WHERE bookId = {book_id}"
    cur.execute(query)
    print("Book deleted successfully!")
    cur.connection.commit()


# Managing Issued Books (View, Issue, Return)
def manage_issued_books(cur):
    while True:
        print("="*50)
        print("ISSUED BOOK MANAGEMENT")
        print("'1' to view issued books")
        print("'2' to issue a book to a user")
        print("'3' to return a book")
        print("'4' to return to admin panel")

        try:
            option = int(input("Choose an option> "))
        except ValueError:
            print("Invalid input! Returning to admin panel...")
            return

        if option == 1:
            view_issued_books(cur)
        elif option == 2:
            issue_book(cur)
        elif option == 3:
            return_book(cur)
        elif option == 4:
            break  # Return to admin panel
        else:
            print("Invalid option. Returning to admin panel...")

# View all issued books
def view_issued_books(cur):
    print("\nIssued Books in the library:")
    
    # Correct query to get issued books details
    query = """
    SELECT ibd.bookId, ibd.bookName, u.userName, ibd.issueDate, ibd.issueTime, ibd.returnDate
    FROM issuedbooksdetails ibd
    JOIN users u ON ibd.userId = u.userId
    WHERE ibd.returnDate IS NULL  -- Only show books that have not been returned
    """
    
    cur.execute(query)
    issued_books = cur.fetchall()
    
    if not issued_books:
        print("No books are currently issued.")
    else:
        for book in issued_books:
            print(f"Book ID: {book[0]}, Book Name: {book[1]}, Issued To: {book[2]}, Issue Date: {book[3]}, Issue Time: {book[4]}")
            if book[5]:
                print(f"Return Date: {book[5]}")
            else:
                print("Return Date: Not yet returned")
            print("="*50)

# Manage users (Admin can view, delete users)
def manage_users(cur):
    while True:
        print("="*50)
        print("USER MANAGEMENT")
        print("'1' to view all users")
        print("'2' to delete a user")
        print("'3' to return to admin panel")

        try:
            option = int(input("Choose an option> "))
        except ValueError:
            print("Invalid input! Returning to admin panel...")
            return

        if option == 1:
            view_users(cur)
        elif option == 2:
            delete_user(cur)
        elif option == 3:
            break  # Return to admin panel
        else:
            print("Invalid option. Returning to admin panel...")

# View all users
def view_users(cur):
    print("\nList of all users:")
    query = "SELECT userId, userName, phoneNumber, emailId, adminStatus FROM users"
    cur.execute(query)
    users = cur.fetchall()
    
    if not users:
        print("No users found.")
    else:
        for user in users:
            print(f"User ID: {user[0]}, Name: {user[1]}, Phone: {user[2]}, Email: {user[3]}, Status: {user[4]}")
    print("="*50)

# Delete a user
def delete_user(cur):
    user_id = input("Enter user ID to delete: ")
    try:
        cur.execute(f"DELETE FROM users WHERE userId = {user_id}")
        print("User deleted successfully!")
        cur.connection.commit()
    except sql.MySQLError as e:
        print(f"Error deleting user: {e}")
        

start()
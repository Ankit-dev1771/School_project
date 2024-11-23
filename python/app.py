import pymysql as sql
from time import sleep
from datetime import datetime

# Global variable to store logged-in user's info (userId and userName)
logged_user = None

# Start function (Intro text)
def start():
    font = " LIBRARY MANAGEMENT SYSTEM "
    for i in range(1, 50, 1):
        sleep(0.025)
        print("=", end="")
    print()
    for i in range(1, 12, 1):
        sleep(0.025)
        print("=", end="")
    for i in font:
        sleep(0.025)
        print(i, end="")
    for i in range(1, 12, 1):
        sleep(0.025)
        print("=", end="")
    print()
    for i in range(1, 50, 1):
        sleep(0.025)
        print("=", end="")
    print("\n")
    Connection()

# Connection to MySQL database
def Connection():
    font = "CONNECTING TO MYSQL . . . "
    for i in font:
        sleep(0.05)
        print(i, end="")
    print()
    try:
        con = sql.connect(host="localhost", user="root", passwd="1928374655", database="library")
    except sql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        print("="*50)
        print("'1' to reconnect")
        print("'2' to exit")
        try:
            user_in = int(input("Enter the command >"))
        except ValueError:
            print("INVALID INPUT \n EXITING PROGRAM . . . ")
            exit()
        if user_in == 1:
            print("RECONNECTING . . .")
            Connection()
        elif user_in == 2:
            exiting()
        else:
            print("INVALID INPUT \n EXITING PROGRAM . . . ")
            exit()
    
    if con:
        print("CONNECTED SUCCESSFULLY!")
        login(con)

# Exiting the program gracefully
def exiting():
    font = "   EXITING THE PROGRAM ...   \n   GOOD BYE!   "
    for i in range(1, 50, 1):
        sleep(0.025)
        print("=", end="")
    print()
    for i in font:
        sleep(0.025)
        print(i, end="")
    exit()

# Login function
def login(con):
    global logged_user
    cur = con.cursor()
    print("="*50)
    print("="*21, " LOG IN ", "="*21)
    print("\n userId 3| userName Admin| password 1234| \n")
    print("'1' to login")
    print("'2' to create account")
    print("'3' to exit")
    print("WARNING: Invalid input results in exiting the program!")

    try:
        user_com = int(input("Enter command> "))
    except ValueError:
        print("INVALID INPUT \n EXITING PROGRAM . . . ")
        exit()

    if user_com == 1:
        name = input("Enter your name: ")
        passw = input("Enter your password: ")

        cur.execute(f"SELECT * FROM users WHERE userName='{name}' AND password='{passw}'")
        user = cur.fetchone()

        if user:
            logged_user = {'userId': user[0], 'userName': user[1]}  # Store logged user info
            print(f"Welcome {logged_user['userName']}!")
            if user[5] == 'admin':
                usr_admin(cur)
            else:
                usr_customer(cur)
        else:
            print("No user found with the given credentials.")
            login(con)

    elif user_com == 2:
        create_acc(cur)
    elif user_com == 3:
        exiting()

# Create a new account (non-admin)
def create_acc(cur):
    print("\nCreate Account")
    name = input("Enter your name (required): ")
    phnum = input("Enter your phone number (optional): ")
    email = input("Enter your email (required): ")
    passwd = input("Create your password (required): ")

    if not name or not email or not passwd:
        print("WARNING: Required fields are missing!")
        login(cur)
    else:
        cur.execute("SELECT COUNT(*) FROM users")
        user_id = cur.fetchone()[0] + 1
        try:
            cur.execute(f"INSERT INTO users (userId, userName, phoneNumber, emailId, password, adminStatus) VALUES ({user_id}, '{name}', '{phnum}', '{email}', '{passwd}', 'not admin')")
            print("Account created successfully!")
            cur.connection.commit()
            login(cur)  # Log the user in after account creation
        except sql.MySQLError as e:
            print(f"ERROR: {e}")
            login(cur)

# Admin Panel
def usr_admin(cur):
    while True:
        print("="*50)
        print("WELCOME ADMIN")
        print("'1' to manage books")
        print("'2' to manage issued books")
        print("'3' to manage users")
        print("'4' to manage notes")
        print("'5' to log out")
        
        try:
            option = int(input("Choose an option> "))
        except ValueError:
            print("Invalid input! Returning to admin panel...")
            continue

        if option == 1:
            manage_books(cur)
        elif option == 2:
            manage_issued_books(cur)
        elif option == 3:
            manage_users(cur)
        elif option == 4:
            manage_notes(cur)
        elif option == 5:
            exiting()
        else:
            print("Invalid option! Returning to admin panel...")

# Managing Books (Admin can view, add, delete books)
def manage_books(cur):
    while True:
        print("="*50)
        print("BOOK MANAGEMENT")
        print("'1' to view all books")
        print("'2' to add a new book")
        print("'3' to delete a book")
        print("'4' to return to admin panel")

        try:
            option = int(input("Choose an option> "))
        except ValueError:
            print("Invalid input! Returning to admin panel...")
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
            print("Invalid option. Returning to admin panel...")

# View all books
def view_books(cur):
    print("\nBooks in the library:")
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    for book in books:
        print(f"Book ID: {book[0]}, Book Name: {book[1]}, Author: {book[7]}, Status: {book[8]}")

# Add a new book
def add_book(cur):
    print("\nAdd New Book")
    book_name = input("Enter book name: ")
    author = input("Enter author name: ")
    publication_year = input("Enter publication year: ")
    
    query = f"INSERT INTO books (bookName, author, publicationYear, issueStatus) VALUES ('{book_name}', '{author}', {publication_year}, 'not issued')"
    cur.execute(query)
    print("Book added successfully!")
    cur.connection.commit()

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

start()

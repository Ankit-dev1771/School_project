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
        con = 1
        sql.connect(host="localhost", user="root", passwd="1928374655", database="library")
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
    book_id = int(input("Enter the id: "))
    book_name = input("Enter book name: ")
    author = input("Enter author name: ")
    publication_year = input("Enter publication year: ")
    
    query = f"INSERT INTO books (bookId, bookName, author, publicationYear, issueStatus) VALUES ({book_id}, '{book_name}', '{author}', {publication_year}, 'not issued')"
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

# Manage notes (Admin can view or add notes to books)
def manage_notes(cur):
    while True:
        print("="*50)
        print("NOTES MANAGEMENT")
        print("'1' to view notes")
        print("'2' to add a note to a book")
        print("'3' to delete note")
        print("'4' to return to admin panel")

        try:
            option = int(input("Choose an option> "))
        except ValueError:
            print("Invalid input! Returning to admin panel...")
            return

        if option == 1:
            view_notes(cur)
        elif option == 2:
            add_note_to_book(cur)
        elif option == 3:
            delete_notes(cur)
        elif option == 4:
            break  # Return to admin panel
        else:
            print("Invalid option. Returning to admin panel...")

# View all notes
def view_notes(cur):
    print("\nList of all notes:")
    query = """
    select * from notes
    """
    cur.execute(query)
    notes = cur.fetchall()
    
    if not notes:
        print("No notes found.")
    else:
        for note in notes:
            print("-"*50,"\n", note)
    print("="*50)

def add_note_to_book(cur):
    # Get the userId from the logged_user object
    user_id = int(input("Enter the user id: "))
    
    # Ask user for the title and description of the note
    note_title = input("Enter the note title: ")
    note_description = input("Enter the note description: ")
    
    # Basic validation: Check if the title or description is empty
    if not note_title.strip() or not note_description.strip():
        print("Both title and description must be provided!")
        return
    
    # Ensure the description is within a reasonable length (e.g., 10000 characters)
    if len(note_description) > 10000:
        print("Note description is too long. Please keep it under 10000 characters.")
        return
    
    # Get the current date and time
    update_date = datetime.now().strftime('%Y-%m-%d')
    update_time = datetime.now().strftime('%H:%M:%S')
    
    try:
        # Insert the new note into the database
        query = """
            INSERT INTO notes (userId, noteTitle, noteDescription, updateDate, updateTime)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        # Execute the query with the provided data
        cur.execute(query, (user_id, note_title, note_description, update_date, update_time))
        
        # Commit the changes to the database
        cur.commit()
        print("Note added successfully!")
    
    except sql.MySQLError as e:
        # Print a more specific error message
        print(f"Error adding note: {e}")

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
def delete_notes(cur):
    n_id = int(input("Enter the user_id: "))
    cur.execute(f"delete from notes where userId={n_id}")

start()

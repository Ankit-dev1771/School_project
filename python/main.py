import pymysql.cursors

# Function to establish the connection to MySQL
def connect_to_db(host, user, password, db):
    connection = pymysql.connect(host=host,
                                  user=user,
                                  password=password,
                                  database=db,
                                  cursorclass=pymysql.cursors.DictCursor)
    return connection

# Functions for CRUD operations on the 'books' table
def add_book(connection, bookId, bookName, publicationYear, issueDate, issueTime, returnDate, returnTime, author, issueStatus, issuedUserId):
    try:
        with connection.cursor() as cursor:
            sql = '''INSERT INTO books (bookId, bookName, publicationYear, issueDate, issueTime, returnDate, returnTime, author, issueStatus, issuedUserId)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(sql, (bookId, bookName, publicationYear, issueDate, issueTime, returnDate, returnTime, author, issueStatus, issuedUserId))
        connection.commit()
        print("Book added successfully!")
    except Exception as e:
        print(f"Error: {e}")

def remove_book(connection, bookId):
    try:
        with connection.cursor() as cursor:
            sql = 'DELETE FROM books WHERE bookId = %s'
            cursor.execute(sql, (bookId,))
        connection.commit()
        print("Book removed successfully!")
    except Exception as e:
        print(f"Error: {e}")

def search_book(connection, bookId):
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM books WHERE bookId = %s'
            cursor.execute(sql, (bookId,))
            result = cursor.fetchone()
            if result:
                print(result)
            else:
                print("No book found with that ID.")
    except Exception as e:
        print(f"Error: {e}")

def display_all_books(connection):
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM books'
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                print(row)
    except Exception as e:
        print(f"Error: {e}")

# Functions for CRUD operations on the 'issuedbooksdetails' table
def add_issued_book(connection, userId, bookId, bookName, issueDate, issueTime, returnDate, returnTime, fineInRs):
    try:
        with connection.cursor() as cursor:
            sql = '''INSERT INTO issuedbooksdetails (userId, bookId, bookName, issueDate, issueTime, returnDate, returnTime, fineInRs)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(sql, (userId, bookId, bookName, issueDate, issueTime, returnDate, returnTime, fineInRs))
        connection.commit()
        print("Issued book details added successfully!")
    except Exception as e:
        print(f"Error: {e}")

def remove_issued_book(connection, userId, bookId):
    try:
        with connection.cursor() as cursor:
            sql = 'DELETE FROM issuedbooksdetails WHERE userId = %s AND bookId = %s'
            cursor.execute(sql, (userId, bookId))
        connection.commit()
        print("Issued book details removed successfully!")
    except Exception as e:
        print(f"Error: {e}")

def display_all_issued_books(connection):
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM issuedbooksdetails'
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                print(row)
    except Exception as e:
        print(f"Error: {e}")

# Functions for CRUD operations on the 'notes' table
def add_note(connection, userId, noteNumber, noteTitle, noteDescription, updateDate, updateTime):
    try:
        with connection.cursor() as cursor:
            sql = '''INSERT INTO notes (userId, noteNumber, noteTitle, noteDescription, updateDate, updateTime)
                     VALUES (%s, %s, %s, %s, %s, %s)'''
            cursor.execute(sql, (userId, noteNumber, noteTitle, noteDescription, updateDate, updateTime))
        connection.commit()
        print("Note added successfully!")
    except Exception as e:
        print(f"Error: {e}")

def display_user_notes(connection, userId):
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM notes WHERE userId = %s'
            cursor.execute(sql, (userId,))
            result = cursor.fetchall()
            for row in result:
                print(row)
    except Exception as e:
        print(f"Error: {e}")

# Functions for CRUD operations on the 'users' table
def add_user(connection, userId, userName, phoneNumber, emailId, password, adminStatus):
    try:
        with connection.cursor() as cursor:
            sql = '''INSERT INTO users (userId, userName, phoneNumber, emailId, password, adminStatus)
                     VALUES (%s, %s, %s, %s, %s, %s)'''
            cursor.execute(sql, (userId, userName, phoneNumber, emailId, password, adminStatus))
        connection.commit()
        print("User added successfully!")
    except Exception as e:
        print(f"Error: {e}")

def display_all_users(connection):
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM users'
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                print(row)
    except Exception as e:
        print(f"Error: {e}")

# Main program loop
def main():
    # Ask user for MySQL connection details
    host = input("Enter MySQL Host: ")
    user = input("Enter MySQL Username: ")
    password = input("Enter MySQL Password: ")
    db = input("Enter MySQL Database Name: ")

    connection = connect_to_db(host, user, password, db)

    while True:
        print("\n--- Library Management System ---")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Search Book")
        print("4. Display All Books")
        print("5. Add Issued Book Details")
        print("6. Remove Issued Book Details")
        print("7. Display All Issued Books")
        print("8. Add Note")
        print("9. Display User Notes")
        print("10. Add User")
        print("11. Display All Users")
        print("12. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            # Add a Book
            bookId = int(input("Enter book ID: "))
            bookName = input("Enter book name: ")
            publicationYear = int(input("Enter publication year: "))
            issueDate = input("Enter issue date (YYYY-MM-DD): ")
            issueTime = input("Enter issue time (HH:MM:SS): ")
            returnDate = input("Enter return date (YYYY-MM-DD): ")
            returnTime = input("Enter return time (HH:MM:SS): ")
            author = input("Enter author name: ")
            issueStatus = input("Enter issue status (e.g., 'not issued'): ")
            issuedUserId = int(input("Enter issued user ID: "))
            add_book(connection, bookId, bookName, publicationYear, issueDate, issueTime, returnDate, returnTime, author, issueStatus, issuedUserId)

        elif choice == '2':
            # Remove a Book
            bookId = int(input("Enter book ID to remove: "))
            remove_book(connection, bookId)

        elif choice == '3':
            # Search for a Book
            bookId = int(input("Enter book ID to search: "))
            search_book(connection, bookId)

        elif choice == '4':
            # Display All Books
            display_all_books(connection)

        elif choice == '5':
            # Add Issued Book Details
            userId = int(input("Enter user ID: "))
            bookId = int(input("Enter book ID: "))
            bookName = input("Enter book name: ")
            issueDate = input("Enter issue date (YYYY-MM-DD): ")
            issueTime = input("Enter issue time (HH:MM:SS): ")
            returnDate = input("Enter return date (YYYY-MM-DD): ")
            returnTime = input("Enter return time (HH:MM:SS): ")
            fineInRs = int(input("Enter fine in Rs: "))
            add_issued_book(connection, userId, bookId, bookName, issueDate, issueTime, returnDate, returnTime, fineInRs)

        elif choice == '6':
            # Remove Issued Book Details
            userId = int(input("Enter user ID: "))
            bookId = int(input("Enter book ID: "))
            remove_issued_book(connection, userId, bookId)

        elif choice == '7':
            # Display All Issued Books
            display_all_issued_books(connection)

        elif choice == '8':
            # Add Note
            userId = int(input("Enter user ID: "))
            noteNumber = int(input("Enter note number: "))
            noteTitle = input("Enter note title: ")
            noteDescription = input("Enter note description: ")
            updateDate = input("Enter update date (YYYY-MM-DD): ")
            updateTime = input("Enter update time (HH:MM:SS): ")
            add_note(connection, userId, noteNumber, noteTitle, noteDescription, updateDate, updateTime)

        elif choice == '9':
            # Display User Notes
            userId = int(input("Enter user ID: "))
            display_user_notes(connection, userId)

        elif choice == '10':
            # Add User
            userId = int(input("Enter user ID: "))
            userName = input("Enter user name: ")
            phoneNumber = input("Enter phone number: ")
            emailId = input("Enter email ID: ")
            password = input("Enter password: ")
            adminStatus = input("Enter admin status (e.g., 'admin', 'not admin'): ")
            add_user(connection, userId, userName, phoneNumber, emailId, password, adminStatus)

        elif choice == '11':
            # Display All Users
            display_all_users(connection)

        elif choice == '12':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

    connection.close()

if __name__ == "__main__":
    main()

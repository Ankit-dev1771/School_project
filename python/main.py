import pymysql.cursors

# Function to establish the connection to MySQL
def connect_to_db(host, user, password, db):
    try:
        connection = pymysql.connect(host=host,
                                      user=user,
                                      password=password,
                                      database=db,
                                      cursorclass=pymysql.cursors.DictCursor)
        return connection
    except Exception as e:
        print(f"Error: Could not connect to database. {e}")
        return None

# Helper function to display a dictionary record in a human-readable way
def print_record(record):
    for key, value in record.items():
        print(f"{key}: {value}")
    print("-" * 40)

# Function to safely convert user input to an INT or None
def safe_int(value):
    try:
        return int(value) if value else None
    except ValueError:
        return None

# CRUD operations for the 'notes' table
def add_note(connection):
    try:
        print("\n--- Add Note ---")
        userId = safe_int(input("Enter user ID: "))
        noteNumber = safe_int(input("Enter note number: "))
        noteTitle = input("Enter note title: ")
        noteDescription = input("Enter note description: ")
        updateDate = input("Enter update date (YYYY-MM-DD): ")
        updateTime = input("Enter update time (HH:MM:SS): ")

        with connection.cursor() as cursor:
            sql = '''INSERT INTO notes (userId, noteNumber, noteTitle, noteDescription, updateDate, updateTime)
                     VALUES (%s, %s, %s, %s, %s, %s)'''
            cursor.execute(sql, (userId, noteNumber, noteTitle, noteDescription, updateDate, updateTime))
        connection.commit()
        print("Note added successfully!")
    except Exception as e:
        print(f"Error: {e}")

def update_note(connection):
    try:
        print("\n--- Update Note ---")
        userId = safe_int(input("Enter user ID to update note: "))
        noteNumber = safe_int(input("Enter note number to update: "))
        new_title = input("Enter new note title (leave blank to keep current): ")
        new_description = input("Enter new note description (leave blank to keep current): ")
        new_update_date = input("Enter new update date (leave blank to keep current): ")
        new_update_time = input("Enter new update time (leave blank to keep current): ")

        with connection.cursor() as cursor:
            sql = 'UPDATE notes SET '
            updates = []
            params = []
            if new_title:
                updates.append('noteTitle = %s')
                params.append(new_title)
            if new_description:
                updates.append('noteDescription = %s')
                params.append(new_description)
            if new_update_date:
                updates.append('updateDate = %s')
                params.append(new_update_date)
            if new_update_time:
                updates.append('updateTime = %s')
                params.append(new_update_time)
            sql += ', '.join(updates)
            sql += ' WHERE userId = %s AND noteNumber = %s'
            params.extend([userId, noteNumber])

            cursor.execute(sql, tuple(params))
        connection.commit()
        print("Note updated successfully!")
    except Exception as e:
        print(f"Error: {e}")

def search_note(connection):
    try:
        print("\n--- Search Note ---")
        userId = safe_int(input("Enter user ID to search notes: "))
        noteNumber = safe_int(input("Enter note number to search: "))

        with connection.cursor() as cursor:
            sql = 'SELECT * FROM notes WHERE userId = %s AND noteNumber = %s'
            cursor.execute(sql, (userId, noteNumber))
            result = cursor.fetchone()
            if result:
                print_record(result)
            else:
                print("No note found with that user ID and note number.")
    except Exception as e:
        print(f"Error: {e}")

def display_notes(connection):
    try:
        print("\n--- Display All Notes ---")
        userId = safe_int(input("Enter user ID to display their notes: "))

        with connection.cursor() as cursor:
            sql = 'SELECT * FROM notes WHERE userId = %s'
            cursor.execute(sql, (userId,))
            notes = cursor.fetchall()
            if notes:
                for note in notes:
                    print_record(note)
            else:
                print("No notes found for that user.")
    except Exception as e:
        print(f"Error: {e}")

# CRUD operations for the 'books' table
def add_book(connection):
    try:
        print("\n--- Add Book ---")
        bookId = safe_int(input("Enter book ID: "))
        bookName = input("Enter book name: ")
        publicationYear = safe_int(input("Enter publication year: "))
        issueDate = input("Enter issue date (YYYY-MM-DD): ")
        issueTime = input("Enter issue time (HH:MM:SS): ")
        returnDate = input("Enter return date (YYYY-MM-DD): ")
        returnTime = input("Enter return time (HH:MM:SS): ")
        author = input("Enter author name: ")
        issueStatus = input("Enter issue status (e.g., 'not issued'): ")
        issuedUserId = safe_int(input("Enter issued user ID (or leave blank if not issued): "))

        with connection.cursor() as cursor:
            sql = '''INSERT INTO books (bookId, bookName, publicationYear, issueDate, issueTime, returnDate, returnTime, author, issueStatus, issuedUserId)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(sql, (bookId, bookName, publicationYear, issueDate, issueTime, returnDate, returnTime, author, issueStatus, issuedUserId))
        connection.commit()
        print("Book added successfully!")
    except Exception as e:
        print(f"Error: {e}")

# CRUD operations for the 'users' table
def add_user(connection):
    try:
        print("\n--- Add User ---")
        userId = safe_int(input("Enter user ID: "))
        userName = input("Enter user name: ")
        phoneNumber = input("Enter phone number: ")
        emailId = input("Enter email ID: ")
        password = input("Enter password: ")
        adminStatus = input("Enter admin status (e.g., 'admin', 'not admin'): ")

        with connection.cursor() as cursor:
            sql = '''INSERT INTO users (userId, userName, phoneNumber, emailId, password, adminStatus)
                     VALUES (%s, %s, %s, %s, %s, %s)'''
            cursor.execute(sql, (userId, userName, phoneNumber, emailId, password, adminStatus))
        connection.commit()
        print("User added successfully!")
    except Exception as e:
        print(f"Error: {e}")

def update_user(connection):
    try:
        print("\n--- Update User ---")
        userId = safe_int(input("Enter user ID to update: "))
        new_userName = input("Enter new user name (leave blank to keep current): ")
        new_phoneNumber = input("Enter new phone number (leave blank to keep current): ")
        new_emailId = input("Enter new email ID (leave blank to keep current): ")
        new_password = input("Enter new password (leave blank to keep current): ")
        new_adminStatus = input("Enter new admin status (leave blank to keep current): ")

        with connection.cursor() as cursor:
            sql = 'UPDATE users SET '
            updates = []
            params = []
            if new_userName:
                updates.append('userName = %s')
                params.append(new_userName)
            if new_phoneNumber:
                updates.append('phoneNumber = %s')
                params.append(new_phoneNumber)
            if new_emailId:
                updates.append('emailId = %s')
                params.append(new_emailId)
            if new_password:
                updates.append('password = %s')
                params.append(new_password)
            if new_adminStatus:
                updates.append('adminStatus = %s')
                params.append(new_adminStatus)
            sql += ', '.join(updates)
            sql += ' WHERE userId = %s'
            params.append(userId)

            cursor.execute(sql, tuple(params))
        connection.commit()
        print("User updated successfully!")
    except Exception as e:
        print(f"Error: {e}")

def remove_user(connection):
    try:
        print("\n--- Remove User ---")
        userId = safe_int(input("Enter user ID to remove: "))

        with connection.cursor() as cursor:
            sql = 'DELETE FROM users WHERE userId = %s'
            cursor.execute(sql, (userId,))
        connection.commit()
        print("User removed successfully!")
    except Exception as e:
        print(f"Error: {e}")

def display_users(connection):
    try:
        print("\n--- All Users ---")
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users')
            users = cursor.fetchall()
            if users:
                for user in users:
                    print_record(user)
            else:
                print("No users found.")
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
        print("2. Search Book")
        print("3. Update Book")
        print("4. Remove Book")
        print("5. Display All Books")
        print("6. Add Issued Book")
        print("7. Update Issued Book")
        print("8. Search Issued Book")
        print("9. Display All Issued Books")
        print("10. Add Note")
        print("11. Update Note")
        print("12. Search Note")
        print("13. Display Notes")
        print("14. Add User")
        print("15. Update User")
        print("16. Remove User")
        print("17. Display Users")
        print("18. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_book(connection)
        elif choice == '2':
            search_book(connection)
        elif choice == '3':
            update_book(connection)
        elif choice == '4':
            remove_book(connection)
        elif choice == '5':
            display_all_books(connection)
        elif choice == '6':
            add_issued_book(connection)
        elif choice == '7':
            update_issued_book(connection)
        elif choice == '8':
            search_issued_book(connection)
        elif choice == '9':
            display_issued_books(connection)
        elif choice == '10':
            add_note(connection)
        elif choice == '11':
            update_note(connection)
        elif choice == '12':
            search_note(connection)
        elif choice == '13':
            display_notes(connection)
        elif choice == '14':
            add_user(connection)
        elif choice == '15':
            update_user(connection)
        elif choice == '16':
            remove_user(connection)
        elif choice == '17':
            display_users(connection)
        elif choice == '18':
            print("Exiting... Goodbye!")
            connection.close()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

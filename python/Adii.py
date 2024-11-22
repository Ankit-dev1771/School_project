import pymysql as myq

print("Welcome to the Medical Management System")

# Establish database connection
con = myq.connect(host="localhost", user="root", passwd="", database="")
if con.open:
    print("Connected successfully")
else:
    print("Error")

mycursor = con.cursor()

# Create database and tables if not exist
mycursor.execute("CREATE DATABASE IF NOT EXISTS sales_vdo")
mycursor.execute("USE sales_vdo")

# Fix missing closing parenthesis in the login table creation statement
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS login (
        username VARCHAR(25) NOT NULL,
        password VARCHAR(25) NOT NULL
    )
""")

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS purchase (
        odate DATE NOT NULL,
        name VARCHAR(25) NOT NULL,
        pcode INT NOT NULL,
        amount INT NOT NULL
    )
""")

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS stock (
        pcode INT NOT NULL,
        pname VARCHAR(25) NOT NULL,
        quantity INT NOT NULL,
        price INT NOT NULL
    )
""")

con.commit()

# Initialize login check
z = 0
mycursor.execute("SELECT * FROM login")
for _ in mycursor:
    z += 1

# Insert default admin if no records exist
if z == 0:
    mycursor.execute("INSERT INTO login (username, password) VALUES ('admin', 'aditya')")
    con.commit()

# Main menu
while True:
    print("""1. Admin
2. Customer
3. Exit""")
    ch = int(input("Enter your choice: "))

    if ch == 1:  # Admin section
        password_input = input("Enter password: ")
        mycursor.execute("SELECT * FROM login")
        username, password = mycursor.fetchone()  # Assuming only one admin user

        if password_input == password:
            print("Welcome Admin")
            loop2 = 'y'
            while loop2.lower() == 'y':
                print("""
                1. Add new item
                2. Update price
                3. Delete item
                4. Display all items
                5. Change password
                6. Log out
                """)
                ch = int(input("Enter your choice: "))

                if ch == 1:  # Add new item
                    loop = 'y'
                    while loop.lower() == 'y':
                        pcode = int(input("Enter product code: "))
                        pname = input("Enter product name: ")
                        quantity = int(input("Enter product quantity: "))
                        price = int(input("Enter product price: "))
                        mycursor.execute("""
                            INSERT INTO stock (pcode, pname, quantity, price)
                            VALUES (%s, %s, %s, %s)
                        """, (pcode, pname, quantity, price))
                        con.commit()
                        print("Record successfully inserted.")
                        loop = input("Do you want to enter more items (y/n): ")
                    loop2 = input("Do you want to continue editing stock (y/n): ")

                elif ch == 2:  # Update price
                    loop = 'y'
                    while loop.lower() == 'y':
                        pcode = int(input("Enter the product code: "))
                        new_price = int(input("Enter the new price: "))
                        mycursor.execute("""
                            UPDATE stock SET price = %s WHERE pcode = %s
                        """, (new_price, pcode))
                        con.commit()
                        loop = input("Do you want to change price of any other item (y/n): ")
                    loop2 = input("Do you want to continue editing stock (y/n): ")

                elif ch == 3:  # Delete item
                    loop = 'y'
                    while loop.lower() == 'y':
                        pcode = int(input("Enter the product code: "))
                        mycursor.execute("DELETE FROM stock WHERE pcode = %s", (pcode,))
                        con.commit()
                        loop = input("Do you want to delete any other data (y/n): ")
                    loop2 = input("Do you want to continue editing stock (y/n): "

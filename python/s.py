import pymysql as sql


def start(): # starting text - optional 
    print("_"*100)
    print("_"*25, "  H O T E L   M A N A G E M E N T  S Y S T E M  ", "_"*25)
    print("_"*100)
    connection() # calling the connection() function to stablish the connection

def connection(): # Stablish the connection between mysql and python - needed
    print("C O N N E C T I N G . . . \n \n ")

    # Error handling in case of failed connection...
    try:
        con = sql.connect(host='localhost', user='root', passwd='1928374655', database='hotel')

    except sql.Error as e:

        print('WARNING: Their is an error occured while connecting to sql! \n ', e)
        exit()

    # Recheck if the connection is properly build 
    if con:
        print("C O N N E C T E D !")
        
        control_pannel(con) # called if the connection is build succesfully 
    else:
        print("WARNING: Unexpected error occured!")
        exit() # Exit the program if connection cannot build 


def control_pannel(con): # Operation handling - needed   

    print("_"*100)
    print("_"*25, "  C O N T R O L   P A N N E L   ", "_"*25)
    print("_"*100, '\n \n')
    
    print('''
    '1' to add guest
    '2' to remove guest
    '3' to see all the guest
    '4' to see all the rooms
    '5' to remove room
    '7' to assign room to guest
    '8' to unassign the room to guest
    '9' to add room
''')
    

    # handling the operations
    while True:
        user_inp = input("Enter your command: ")

        if user_inp == '1':
            add_guest(con)
        elif user_inp == '2':
            remove_guest(con)
        elif user_inp =='3':
            see_guest(con)
        elif user_inp =='4':
            see_rooms(con)
        elif user_inp == '5':
            remove_rooms(con)
        elif user_inp == '7':
            assign_room(con)
        elif user_inp == '8':
            unassign_room(con)
        elif user_inp == '9':
            add_rooms(con)

        else:
            print("no command found")

def add_guest(con): # ADD new guest
    
    print("_"*100)
    print("_"*25, "  A D D   G U E S T   ", "_"*25)
    print("_"*100, '\n \n')
    
    try:
        cur = con.cursor()
    except sql.Error as e:
        print("Error: ", e)
        control_pannel(con)

    # Basic fields ...
    name = input("Enter Guest Name: ")
    if len(name) > 50:
        print("WARNING: Name is to big!")
        control_pannel(con)
    gender = input("Enter The Guest Gender ('male' or 'female'): ")
    if gender not in ['male', 'female']:
        print("WARNING: Invaild Gender!")
        control_pannel(con)
    mobileNo = input("Enter The Guest Mobile Number (10 digit): ")
    if not mobileNo.isdigit():
        print("WARNING: Invaild Mobile Number:")
        control_pannel(con)

    # Creating guestId ...
    cur.execute("select count(*) from guest")
    data = cur.fetchall()
    id = data[0][0]
    if id == 0:
        id += 1

    try:
        cur.execute(f"insert into guest(guestId, guestName, guestGender, guestMobile) values({id}, '{name}', '{gender}', '{mobileNo}')")
        con.commit()
    except sql.Error as e:
        print("Error: ", e)
        control_pannel(con)
    
    print("NEW GUEST IS SUCCESFULLY ADDED!")

    # Getting new guest info ...
    cur.execute(f'select * from guest where guestId={id}')
    data = cur.fetchall()
    print(data[0])

def remove_guest(con):
    
    cur = con.cursor()

    print("_"*100)
    print("_"*25, "  R E M O V E    G U E S T   ", "_"*25)
    print("_"*100, '\n \n')

    id = int(input("Enter the gustId you want to remove: "))

    try: # Checking if the guest really exist
        cur.execute(f"select * from guest where guestId={id}")
        data = cur.fetchall()
        print(data[0])
    except sql.Error as e:
        print("error: ", e)
        control_pannel(con)

    conform = input("Do You Really Want To Remove This User? (Y/n): ")

    if conform in ['n', 'N']:
        print("Guest is not removed!")

    else:
        
        try:
            cur.execute(f'delete from guest where guestId={id}')
            con.commit()
        except sql.Error as e:
            print("ERROR: ", e) 
            control_pannel(con)
        print("Guest is succesfully removed!")

def see_guest(con):
    cur = con.cursor()

    cur.execute('select * from guest')

    data = cur.fetchall()
    if len(data) > 0:
        print("No Guest Found!")
    for i in data:
        print(i)
    
    print(data)

    control_pannel(con)

def see_rooms(con):

    cur = con.cursor()

    cur.execute('select * from rooms')

    data = cur.fetchall()
    for i in data:
        print(i)

    control_pannel(con)

def remove_rooms(con):
    
    cur = con.cursor()

    print("_"*100)
    print("_"*25, "  R E M O V E    R O O M S   ", "_"*25)
    print("_"*100, '\n \n')

    id = int(input("Enter the roomNo you want to remove: "))

    try: # Checking if the room really exist
        cur.execute(f"select * from rooms where roomNo={id}")
        data = cur.fetchall()
        print(data[0])
    except sql.Error as e:
        print("error: ", e)
        control_pannel(con)

    conform = input("Do You Really Want To Remove This User? (Y/n): ")

    if conform in ['n', 'N']:
        print("Guest is not removed!")

    else:
        
        try:
            cur.execute(f'delete from rooms where roomNo={id}')
            con.commit()
        except sql.Error as e:
            print("ERROR: ", e) 
            control_pannel(con)
        print("Room is succesfully removed!")


def assign_room(con):
    cur = con.cursor()

    print("_"*100)
    print("_"*25, "  A S S I G N   R O O M   ", "_"*25)
    print("_"*100, '\n \n')

    room_no = int(input("Enter the roomNo you want to assign: "))
    guest_id = int(input("Enter the guestId you want to assign to this room: "))

    # Check if the room exists
    cur.execute(f"select * from rooms where roomNo={room_no}")
    room = cur.fetchall()
    if len(room) == 0:
        print(f"ERROR: Room {room_no} does not exist!")
        control_pannel(con)

    # Check if the guest exists
    cur.execute(f"select * from guest where guestId={guest_id}")
    guest = cur.fetchall()
    if len(guest) == 0:
        print(f"ERROR: Guest {guest_id} does not exist!")
        control_pannel(con)

    # Assign the room to the guest
    try:
        cur.execute(f"update rooms set isAssignedTo={guest_id} where roomNo={room_no}")
        con.commit()
        print(f"Room {room_no} successfully assigned to Guest {guest_id}.")
    except sql.Error as e:
        print(f"ERROR: {e}")
        control_pannel(con)

    control_pannel(con)

def unassign_room(con):
    cur = con.cursor()

    print("_"*100)
    print("_"*25, "  U N A S S I G N   R O O M   ", "_"*25)
    print("_"*100, '\n \n')

    room_no = int(input("Enter the roomNo you want to unassign: "))

    # Check if the room exists
    cur.execute(f"select * from rooms where roomNo={room_no}")
    room = cur.fetchall()
    if len(room) == 0:
        print(f"ERROR: Room {room_no} does not exist!")
        control_pannel(con)

    # Check if the room is already unassigned
    if room[0][2] is None:
        print(f"Room {room_no} is already unassigned.")
        control_pannel(con)

    # Unassign the room from the guest
    try:
        cur.execute(f"update rooms set isAssignedTo=NULL where roomNo={room_no}")
        con.commit()
        print(f"Room {room_no} successfully unassigned from the guest.")
    except sql.Error as e:
        print(f"ERROR: {e}")
        control_pannel(con)

    control_pannel(con)

def add_rooms(con):
    cur = con.cursor()

    print("_"*100)
    print("_"*25, "  A D D   R O O M   ", "_"*25)
    print("_"*100, '\n \n')

    # Room number and cost
    room_no = int(input("Enter the room number: "))
    per_day_cost = input("Enter the per-day cost for this room (e.g., '1000'): ")

    # Validate the per_day_cost input
    if not per_day_cost.isdigit():
        print("WARNING: Invalid per-day cost. Please enter a numeric value.")
        control_pannel(con)

    # Assigning a room to a guest (optional)
    assign_guest = input("Do you want to assign this room to a guest? (Y/n): ")

    if assign_guest.lower() == 'y':
        guest_id = int(input("Enter the guestId you want to assign to this room: "))
        
        # Check if the guest exists
        cur.execute(f"select * from guest where guestId={guest_id}")
        guest = cur.fetchall()
        if len(guest) == 0:
            print(f"ERROR: Guest {guest_id} does not exist!")
            control_pannel(con)
        
        # Inserting new room data into the rooms table with guest assignment
        try:
            cur.execute(f"insert into rooms (roomNo, perDayCost, isAssignedTo) values ({room_no}, '{per_day_cost}', {guest_id})")
            con.commit()
            print(f"Room {room_no} successfully added and assigned to guest {guest_id}.")
        except sql.Error as e:
            print(f"ERROR: {e}")
            control_pannel(con)

    else:
        # Inserting new room data without assignment
        try:
            cur.execute(f"insert into rooms (roomNo, perDayCost, isAssignedTo) values ({room_no}, '{per_day_cost}', NULL)")
            con.commit()
            print(f"Room {room_no} successfully added (not assigned to any guest).")
        except sql.Error as e:
            print(f"ERROR: {e}")
            control_pannel(con)

    control_pannel(con)



start()
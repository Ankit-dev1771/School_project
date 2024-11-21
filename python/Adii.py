import pymysql as myq
print(""
_____________________________________
welcome to medical management system
_____________________________________"")
con=myq.connect(host="localhost",user="root",passwd="",database="")
if con is connected:
	print("connected successfully")
else:
	print("error")
mycursor=con.cursor()
mycursor.execute("create database if not exists sales_vdo")
mycursor.execute("use sales_vdo")
mycursor.execute("create table if not exists login(username varchar(25) not null,password varchar(25) not null")
mycursor.execute("create table if not exists purchase(odate date not null, name varchar(25) not null,pcode int not null,amount int not null)")
mycursor.execute("create table if not exists stock(pcode int not null,pname varchar(25) not null, quantity int not null, price int not null) ")
con.commit()
z=0
mycursor.execute("select * from login")
for i in mycursor:
	z+=1
if(z==0):
	mycursor.execute("insert into login values('username','aditya')")
	con.commit()
while True:
	print(""""1.Admin2.Customer3.Exit""")
	ch=int(input("enter your choice:"))
	if(ch==1):
		passs=input("enter password:")
		mycursor.execute("select * from login")
		for i in mycursor:
			username,password=i
		if(passs==password):
			print("welcome")
			loop2='y'
			while(loop2=='y' or loop2=='Y'):
				print("1.Add new item 2.updating price 3.deleting item 4.display all items 5. To change the password 6.Log out")
				ch=int(input("enter your choice:"))
				if(ch==1):
					loop='y'
					while(loop=='y' or loop=='Y'):
						pcode=int(input("enter product code:")
						pname=input("enter product name:")
						quantity=int(input("enter product quantity:"))
						price=int(input("enter product price:"))
						mycursor.execute("insert into stock values('"+str(pcode)+"','"+pname+"','"+str(quantity)+"','"+str(price)+"')")
						con.commit()
						print("record successfully inserted..")
						loop=input("do you want to enter more items(y/n)")
					loop2=input("do you want to continue editing stock(y/n):")
				elif(ch==2):
					loop='y'
					while(loop=='y' or loop=='Y'):
						pcode=int(input("enter the product code:"))
						new_price=int(input("enter the new price:"))
						mycursor.execute("update stock set price='"+str(new_price)+"' where pcode='"+str(pcode)+"'")
						con.commit()
						loop=input("do you want to change price of any other item(y/n):")
					loop2=input("do you want to continue editing stock(y/n):")
				elif(ch==3):
						loop='y'
						while(loop=='y' or loop=='Y'):
							pcode=int(input("enter the product code:"))
							mycursor.execute("delete from stock where pcode='"+str(pcode)"'")
							con.commit()
							loop=input("do you want to delete any other data(y/n):")
						loop2=input("do you want to continue editing stock(y/n):")
				elif(ch==4):
						mycursor.execute("select * from stock")
						print("pcode || pname || quantity || price")
						for i in mycursor:
							t_code,t_name,t_quan,t_price=i
							print(f"{t_code}|| {t_name} || {t_quan}|| {t_price}")
						loop2=input("do you want to continue editing stock(y/n):")
				 elif(ch==5):
				 	old_passs=input("enter the old password :")
				 	mycursor.execute("select * from login")
				 	for i in mycursor:
				 		username,password=i
				 	if(old_passs==password):
				 		new_passs=input("enter the new password:")
				 		mycursor execute("update login set password='"+new_passs+"'")
				 		con.commit()
				 		print("password changes successfully..")
				 	loop2=input("do you want to continue editing stock(y/n):")
				 elif(ch==6):
				 	break
	else:
		print("wrong password")
	elif(ch==2):
				 	print("""1.item bucket 2.payment 3.view available items 4.go back""")
				 	ch2=int(input("enter your choice: "))
				 	if(ch2==1):
				 		name=input("enter your name:")
				 		pcode=int(input("enter product code:"))
				 		quantity=int(input("enter product quantity:"))
				 		mycursor.execute("select * from stock where pcode='"+str(pcode)+"'")
				 		for i in mycursor:
				 			t_code,t_name,t_quan,t_price=i
				 		amount=t_price*quantity
				 		net_quan=t_quan-quantity
				 		mycursor.execute("update stock set quantity='"+str(net_quan)+"' where pcode='"+str(pcode)+"'")
				 		mycursor.execute("insert into purchase values(now(),'"+name+"','"+str(pcode)"','"+str(amount)+"'")
				 		con.commit()
				 	elif(ch2==2):
				 			print(f"amount to be paid {amount}")
				 	elif(ch2==3):
				 			print("code || name || price")
				 			mycursor.execute("select * from stock")
				 			for i in mycursor:
				 				t_code,t_name,t_quan,t_price=i
				 				print(f"{t_code} || {t_name} || {t_price}")
				 	elif(ch2==4):
				 		break
	elif(ch==3):
				 		break

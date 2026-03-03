import mysql.connector


# Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="yor_db"
)

cursor = conn.cursor()

while True:
    print("\n---- ONLINE FOOD DELIVERY SYSTEM ----")
    print("1. Insert Customer")
    print("2. View Customers")
    print("3. Update Customer")
    print("4. Delete Customer")
    print("5. Exit")

    choice = input("Enter your choice: ")

    # INSERT
    if choice == "1":
        cid = int(input("Enter Customer ID: "))
        name = input("Enter Name: ")

        sql = "INSERT INTO Customer (customer_id, name) VALUES (%s, %s)"
        values = (cid, name)

        cursor.execute(sql, values)
        conn.commit()

        print("Customer Inserted Successfully!")

    # READ
    elif choice == "2":
        cursor.execute("SELECT * FROM Customer")
        result = cursor.fetchall()

        for row in result:
            print(row)

    # UPDATE
    elif choice == "3":
        cid = int(input("Enter Customer ID to update: "))
        new_name = input("Enter New Name: ")

        sql = "UPDATE Customer SET name = %s WHERE customer_id = %s"
        values = (new_name, cid)

        cursor.execute(sql, values)
        conn.commit()

        print("Customer Updated Successfully!")

    # DELETE
    elif choice == "4":
        cid = int(input("Enter Customer ID to delete: "))

        sql = "DELETE FROM Customer WHERE customer_id = %s"
        values = (cid,)

        cursor.execute(sql, values)
        conn.commit()

        print("Customer Deleted Successfully!")

    # EXIT
    elif choice == "5":
        print("Exiting Program...")
        break

    else:
        print("Invalid Choice!")

# Close connection
cursor.close()
conn.close()
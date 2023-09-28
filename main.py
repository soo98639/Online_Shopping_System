import pyodbc
import pandas as pd

conn_string = (
    r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Users\acer\PycharmProjects\groupProject\database.accdb;'
)
conn = pyodbc.connect(conn_string)
cursor = conn.cursor()


def user_register():
    print("=================== User Registration ===================")
    print("")
    userRegID = input("User ID: ")
    userRegPassword = input("Password: ")
    cursor.execute("INSERT INTO user_login (user_id, password) VALUES (?,?)", (userRegID, userRegPassword))
    conn.commit()
    print("Congratulations, your account has been successfully created.")
    print("")


def admin_register():
    print("================= Admin Registration =====================")
    print("")
    adminRegID = input("Admin ID: ")
    adminRegPassword = input("Password: ")
    cursor.execute("INSERT INTO admin_login (admin_id, password) VALUES (?,?)", (adminRegID, adminRegPassword))
    conn.commit()
    print("Congratulations, your account has been successfully created.")
    print("")


def item_list_page():
    sqlQuery = pd.read_sql_query("SELECT * FROM item_list", conn)
    df_itemList = pd.DataFrame(sqlQuery, columns=["item_name", "price"])
    print("\n")
    print("----------------------------------------------------------")
    print("====================== Item List =========================")
    print("----------------------------------------------------------")
    print(df_itemList.to_string())
    print("----------------------------------------------------------")
    print("")
    print("1. Back")
    print("2. Add Item")
    print("3. Remove Item")
    print("")
    print("----------------------------------------------------------")
    admin_choice1 = int(input("Enter your choice: "))
    print("----------------------------------------------------------")

    if admin_choice1 == 1:
        print("")

    elif admin_choice1 == 2:
        print("")
        print("Insert the product name and price that you want to add.")
        newItemName = input("Item Name: ")
        newItemPrice = input("Price: ")
        cursor.execute("INSERT INTO item_list (item_name, price) VALUES (?,?)", (newItemName, newItemPrice))
        conn.commit()
        print("Added successfully.")

    elif admin_choice1 == 3:
        print("")
        print("Insert the product name that you want to delete.")
        dltItemName = input("Item Name: ")
        cursor.execute("DELETE FROM item_list WHERE item_name = ?", dltItemName)
        conn.commit()
        print("Removed successfully.")


def place_order_page():
    cart = {"item_name": [], "price": []}
    cartItemList = []
    sqlQuery = pd.read_sql_query("SELECT * FROM item_list", conn)
    df_itemList = pd.DataFrame(sqlQuery, columns=["item_name", "price"])
    user_choice1 = 2
    while user_choice1 == 1 or user_choice1 == 2:
        print("\n")
        print("------------------- USER MAIN PAGE -----------------------")
        print("==================== All Products ========================")
        print("----------------------------------------------------------")
        print(df_itemList.to_string())
        print("----------------------------------------------------------")
        print("")
        print("1. Add Item to Cart")
        print("2. Check Out")
        print("3. Quit")
        print("")
        print("----------------------------------------------------------")
        user_choice1 = int(input("Enter your choice: "))
        print("----------------------------------------------------------")

        if user_choice1 == 1:
            itemNo = int(input("Please enter the No. of item you want to add into cart: "))
            itemName = df_itemList.loc[itemNo]["item_name"]
            itemPrice = df_itemList.loc[itemNo]["price"]
            cart["item_name"].append(itemName)
            cart["price"].append(itemPrice)
            cartItemList.append(itemName)
            print("Item added to cart.")
            user_choice2 = "yes"

            while user_choice2 == "yes":
                print("")
                user_choice2 = input("Do you want to add another item into cart? (yes/no): ")
                print("")
                if user_choice2 == "yes":
                    addItemNo = int(input("Please enter the No. of item you want to add into cart: "))
                    addItemName = df_itemList.loc[addItemNo]["item_name"]
                    addItemPrice = df_itemList.loc[addItemNo]["price"]
                    cart["item_name"].append(addItemName)
                    cart["price"].append(addItemPrice)
                    print("Item added to cart.")

        elif user_choice1 == 3:
            exit()

        while user_choice1 == 2:
            df_cart = pd.DataFrame(cart)
            print("\n")
            print("----------------------------------------------------------")
            print("======================== Cart ============================")
            print("----------------------------------------------------------")
            print(df_cart.to_string())
            print("----------------------------------------------------------")
            print("")
            print("1. Remove item.")
            print("2. Confirm check out")
            print("3. Back")
            print("")
            print("----------------------------------------------------------")
            user_choice3 = int(input("Enter your choice: "))
            print("----------------------------------------------------------")
            if user_choice3 == 1:
                dltItemNo = int(input("Enter the No. of item you want to remove from cart: "))
                del cart["item_name"][dltItemNo]
                del cart["price"][dltItemNo]
                print("Removed successfully.")

            elif user_choice3 == 2:
                print("Please enter your information below.")
                name = input("Name: ")
                address = input("Address: ")
                hpNo = input("Phone number: ")
                totPayment = (df_cart["price"].sum()).round(2)
                maxIndex = len(df_cart)
                index = 0
                products = ""
                while index < maxIndex:
                    initial = products + df_cart.loc[index]["item_name"] + " ; "
                    index += 1
                    products = initial

                cursor.execute(
                    "INSERT INTO order_history "
                    "(cust_name, cust_address, cust_phone_number, total_product, total_payment)"
                    "VALUES (?,?,?,?,?)",
                    (name, address, hpNo, products, totPayment)
                )
                conn.commit()
                print("")
                print("Your order has been placed successfully.")
                print("Total payment is RM", totPayment)
                cart.clear()
                break

            else:
                break


def sales_report():
    sqlQuery = pd.read_sql_query("SELECT * FROM order_history", conn)
    df_orderHistory = pd.DataFrame(
        sqlQuery, columns=["cust_name", "cust_address", "cust_phone_number", "total_product", "total_payment"]
    )
    totSales = float(df_orderHistory["total_payment"].sum())
    avgSpending = float(df_orderHistory["total_payment"].mean())
    totOrder = int(df_orderHistory["total_payment"].count())
    print("\n")
    print("-----------------------------------------------------------")
    print("====================== Order History ======================")
    print("-----------------------------------------------------------")
    print("")
    print(df_orderHistory.to_string())
    print("-----------------------------------------------------------")
    print("")
    print("Total order: ", totOrder)
    print("")
    print("Total sales is RM", totSales)
    print("")
    print("Average spending of a customer is RM", avgSpending)
    print("")
    print("-------------------------------------------------------------")
    admin_choice2 = int(input("Enter your choice. (1 - Back to Main Page, 2 - End Program):"))
    if admin_choice2 == 1:
        print("-------------------------------------------------------------")
    elif admin_choice2 == 2:
        print("-------------------------------------------------------------")
        exit()


option1 = 1
while 1 <= option1 <= 4:
    print("----------------------------------------------------------")
    print("============ Machines Official Apple Retailer ============")
    print("----------------------------------------------------------")
    print("")
    print("1. Admin Login")
    print("2. Admin Register")
    print("3. User Login")
    print("4. User Register")
    print("5. Quit")
    print("")
    print("----------------------------------------------------------")
    option1 = int(input("Enter your choice: "))
    print("----------------------------------------------------------")
    print("\n")
    if option1 == 1:
        adminSqlQuery = pd.read_sql_query("SELECT * FROM admin_login", conn)
        df_adminLogin = pd.DataFrame(adminSqlQuery, columns=["admin_id", "password"])
        adminLoginID = input("Admin ID: ")
        adminLoginPassword = input("Password: ")
        adminMaxIndex = len(df_adminLogin)
        i = 0
        while i < adminMaxIndex:
            checkID = df_adminLogin.loc[i]["admin_id"]
            checkPassword = df_adminLogin.loc[i]["password"]
            if checkID == adminLoginID and checkPassword == adminLoginPassword:
                print("")
                print("Login Successful. Welcome", adminLoginID)
                option2 = 1
                while option2 == 1 or option2 == 2:
                    print("\n")
                    print("------------------------------------------------------------")
                    print("===================== ADMIN MAIN PAGE ======================")
                    print("------------------------------------------------------------")
                    print("")
                    print("1. Item Management")
                    print("2. Sales Report")
                    print("3. Quit")
                    print("")
                    print("----------------------------------------------------------")
                    option2 = int(input("Enter your choice: "))
                    print("----------------------------------------------------------")

                    if option2 == 1:
                        item_list_page()

                    elif option2 == 2:
                        sales_report()

                    elif option2 == 3:
                        exit()
            else:
                i += 1

    elif option1 == 2:
        admin_register()

    elif option1 == 3:
        userSqlQuery = pd.read_sql_query("SELECT * FROM user_login", conn)
        df_userLogin = pd.DataFrame(userSqlQuery, columns=["user_id", "password"])
        userLoginID = input("User ID: ")
        userLoginPassword = input("Password: ")
        userMaxIndex = len(df_userLogin)
        i = 0
        while i < userMaxIndex:
            checkID = df_userLogin.loc[i]["user_id"]
            checkPassword = df_userLogin.loc[i]["password"]
            if checkID == userLoginID and checkPassword == userLoginPassword:
                print("")
                print("Login Successful. Welcome", userLoginID)
                place_order_page()

            else:
                i += 1

    elif option1 == 4:
        user_register()

    else:
        exit()

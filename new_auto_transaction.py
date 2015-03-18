# error handling for owner table
def OwnerCheck(seller_id, vehicle_id, connection, curs):
    command = "SELECT owner_id FROM owner WHERE vehicle_id = %s AND owner_id = %s" % (vehicle_id, seller_id)
    curs.execute(command)
    row = curs.fetchone()
    count = 0
    while row:
        count = count + 1
        row = curs.fetchone()
    if count != 1:
        print("Invalid input: seller does not own vehicle.")
        return True
    else:
        return False

# error handling for price
def PriceErrCheck(price):
    format_err = True
    while (format_err):
        format_err = CheckIfFloat(price)
        if format_err == True:
            price = input("Enter the sale price: ")
            continue;
    return float(price)

# error handling for price
def CheckIfFloat(price):
    try:
        float(price)
    except:
        print("Invalid input: must be a float")
    else:
        return False
    return True


# formatting date
def FormatDate(year, month, day):
    return day + "-" + month + "-" + year

# error handling for month
def MonthErrCheck(s_month):
    len_err = True
    format_err = True
    while (format_err or len_err):
        len_err = CheckLen(s_month, 3)
        if len_err == True:
            s_month = input("Enter the month of the sale: ")
            continue;
        format_err = CheckIfAlpha(s_month)
        if format_err == True:
            s_month = input("Enter the month of the sale: ")
            continue;
    return s_month

# error handling for month
def CheckIfAlpha(a_str):
    if a_str.isalpha():
        return False
    else:
        return True

# error handling for day
def DayErrCheck(s_day):
    len_err = True
    format_err = True
    while (format_err or len_err):
        len_err = CheckLen(s_day, 2)
        if len_err == True:
            s_day = input("Enter the day of the sale: ")
            continue;
        format_err = CheckIfInt(s_day)
        if format_err == True:
            s_day = input("Enter the day of the sale: ")
            continue;
    return s_day

# error handling for year
def YearErrCheck(s_year):
    len_err = True
    format_err = True
    while (format_err or len_err):
        len_err = CheckLen(s_year, 4)
        if len_err == True:
            s_year = input("Enter the year of the sale: ")
            continue;
        format_err = CheckIfInt(s_year)
        if format_err == True:
            s_year = input("Enter the year of the sale: ")
            continue;
    return s_year

# error handling for vehicle_id
def VehErrCheck(vehicle_id, connection, curs):
    format_err = True
    db_err = True
    len_err = True
    while (format_err or db_err or len_err):
        len_err = CheckLen(vehicle_id, 15)
        if len_err == True:
            vehicle_id = input("Enter vehicle_id: ")
            continue;
        format_err = CheckIfInt(vehicle_id)
        if format_err == True:
            vehicle_id = input("Enter vehicle_id: ")
            continue;
        db_err = CheckIfVehExists(vehicle_id, connection, curs)
        if db_err == True:
            vehicle_id = input("Enter vehicle_id: ")
            continue;
    return int(vehicle_id)

# error handling for vehicle_id
def CheckIfVehExists(vehicle_id, connection, curs):
    vehicle_id = int(vehicle_id)
    command = "SELECT serial_no FROM vehicle WHERE serial_no =: vehicle_id"
    curs.execute(command, {"vehicle_id":vehicle_id})
    row = curs.fetchone()
    count = 0
    while row:
        count = count + 1
        row = curs.fetchone()
    if count != 1:
        print("Invalid input: serial_no does not exist.")
        return True
    else:
        return False

# error handling for seller_id
def SellerErrCheck(seller_id, connection, curs):
    format_err = True
    db_err = True
    len_err = True
    while (format_err or db_err or len_err):
        len_err = CheckLen(seller_id, 15)
        if len_err == True:
            seller_id = input("Enter seller_id: ")
            continue;
        format_err = CheckIfInt(seller_id)
        if format_err == True:
            seller_id = input("Enter seller_id: ")
            continue;
        db_err = CheckIfIdExists(seller_id, connection, curs)
        if db_err == True:
            seller_id = input("Enter seller_id: ")
            continue;
    return int(seller_id)

# error handling for buyer_id
def BuyerErrCheck(buyer_id, connection, curs):
    format_err = True
    db_err = True
    len_err = True
    while (format_err or db_err or len_err):
        len_err = CheckLen(buyer_id, 15)
        if len_err == True:
            buyer_id = input("Enter buyer_id: ")
            continue;
        format_err = CheckIfInt(buyer_id)
        if format_err == True:
            buyer_id = input("Enter buyer_id: ")
            continue;
        db_err = CheckIfIdExists(buyer_id, connection, curs)
        if db_err == True:
            buyer_id = input("Enter buyer_id: ")
            continue;
    return int(buyer_id)

# error handling for buyer_id
# error handling for seller_id
# error handling for vehicle_id
# error handling for s_year
# error handling for s_day
def CheckLen(a_str, expected_len):
    if len(a_str) <= expected_len:
        return False
    else:
        print("Invalid input: Must be <=", expected_len, "digits long")
        return True

# error handling for buyer_id
# error handling for seller_id
def CheckIfIdExists(some_id, connection, curs):
    some_id = int(some_id)
    command = "SELECT sin FROM people WHERE sin =: some_id"
    curs.execute(command,{"some_id":some_id})
    row = curs.fetchone()
    count = 0
    while row:
        count = count + 1
        row = curs.fetchone()
    if count != 1:
        print("Invalid input: SIN does not exist.")
        return True
    else:
        return False

# error handling for transaction_id
def TransErrCheck(transaction_id, connection, curs):
    format_err = True
    db_err = True
    while (format_err or db_err):
        format_err = CheckIfInt(transaction_id)
        if format_err == True:
            transaction_id = input("Enter transaction_id: ")
            continue;
        db_err = CheckIfTransExists(transaction_id, connection, curs)
        if db_err == True:
    	    transaction_id = input("Enter transaction_id: ")
    	    continue;
    return int(transaction_id)

# error handling for transaction_id
def CheckIfTransExists(transaction_id, connection, curs):
    transaction_id = int(transaction_id)
    command = "SELECT transaction_id FROM auto_sale WHERE transaction_id =: Transaction_id"
    curs.execute(command, {'Transaction_id': transaction_id} )
    row = curs.fetchone()
    count = 0
    while row:
        count = count + 1
        row = curs.fetchone()
    if count != 0:
        print("Invalid input: transaction id already exists")
        return True
    else:
        return False

# error handling for transaction_id
# error handling for buyer_id
# error handling for seller_id
# error handling for vehicle_id
# error handling for s_date
# error handling for s_day
def CheckIfInt(some_id):
    if some_id.isdigit():
        return False
    else:
        print("Invalid input: must be integer")
        return True

def AutoTransaction(connection, curs):
    # Ask user for relevant information

    transaction_id = input("Enter transaction_id: ")
    # check validity of input
    transaction_id = TransErrCheck(transaction_id, connection,  curs)
    
    buyer_id = input("Enter buyer_id: ")
    # check validity of input
    buyer_id = BuyerErrCheck(buyer_id, connection, curs)

    invalid_owner = True
    while (invalid_owner):
        seller_id = input("Enter seller_id: ")
	# check validity of input
        seller_id = SellerErrCheck(seller_id, connection, curs)
        # need to check if seller actually owns vehicle? no
        # need to check if buyer != seller id? no
        vehicle_id = input("Enter vehicle_id: ")
        # check validity of input
        vehicle_id = VehErrCheck(vehicle_id, connection, curs)
        # need to check that seller owns vehicle!!!!
        invalid_owner = OwnerCheck(seller_id, vehicle_id, connection, curs)	

    s_year = input ("Enter year of sale (eg. 1991): ")
    # check validity of input
    s_year = YearErrCheck(s_year)
    # need to check if year in some range? no

    s_month = input ("Enter month of sale (eg. FEB): ")
    # check validity of input
    s_month = MonthErrCheck(s_month)
    # need to check if month in set of 12? no

    s_day = input("Enter day of sale (eg. 25, 01): ")
    # check validity of input
    s_day = DayErrCheck(s_day)
    # need to check if day in {1,31} or it matches month? no

    s_date = FormatDate (s_year, s_month, s_day)

    price = input("Enter sale price")
    # check validity of input
    price = PriceErrCheck(price)

    # Delete owners from owners with vehicle_id
    command = "DELETE from owner WHERE vehicle_id =: Vehicle_id"
    curs.execute (command, {"Vehicle_id": vehicle_id})
    print(command, {"Vehicle_id": vehicle_id})

    # Insert new owner_id(buyer_id), vehicle_id into owner table
    # not sure if we need to ask if primary owner? yes assume primary owner
    data = [(buyer_id, vehicle_id, "y")]
    curs.bindarraysize = 1
    curs.setinputsizes(15,15,1)
    curs.executemany("INSERT into owner(owner_id,vehicle_id, is_primary_owner)"
                        "VALUES (:1, :2, :3)", data)

    print("entered new owner table row")

    # Insert new transaction_id, seller_id, buyer_id, vehicle_id, s_date, price into auto_sale table
    data = [(transaction_id, seller_id, buyer_id, vehicle_id, s_date, price)]
    curs.bindarraysize = 1
    curs.setinputsizes(int, 15, 15, 15, 11, float) 
    curs.executemany( "INSERT into auto_sale VALUES (:1, :2, :3, :4, :5, :6)", data)


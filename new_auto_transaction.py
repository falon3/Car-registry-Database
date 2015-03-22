from new_person import NewPerson
import datetime 

# error handling for owner table
def OwnerCheck(seller_id, vehicle_id, connection, curs):
    command = "SELECT owner_id FROM owner WHERE vehicle_id = %s AND owner_id = %s" % (vehicle_id, seller_id)
    curs.execute(command)
    if ( None == curs.fetchone()):
        print("Invalid input: seller does not own vehicle.")
        return True
    else:
        return False

# error handling for price
def PriceErrCheck():
    format_err = True
    while (format_err):
        price = input("Enter sale price: ")
        try:
            float(price)
        except:
            print("Invalid input: must be a float")
        else:
            format_err = False        
    return float(price)

def DateErrCheck(connection, curs):
    date_err = True
    while (date_err):
        date = input("Enter date, YY-MM-DD: ")
        try:
            # strptime throws an exception if userIn doesn't match the pattern
            vdate = datetime.datetime.strptime(date, "%y-%m-%d")
        except:
            print("Invalid date, try again!\n")
        else:
            date_err = False
    return vdate

# error handling for vehicle_id
def VehErrCheck( connection, curs):
    format_err = True
    db_err = True
    len_err = True
    while (format_err or db_err or len_err):
        vehicle_id = input("Enter vehicle_id: ")
        len_err = CheckLen(vehicle_id, 15)
        if len_err == True:
            continue;
        format_err = CheckIfInt(vehicle_id)
        if format_err == True:
            continue;
        db_err = CheckIfVehExists(vehicle_id, connection, curs)
        if db_err == True:
            continue;
    return int(vehicle_id)

# error handling for vehicle_id
def CheckIfVehExists(vehicle_id, connection, curs):
    vehicle_id = int(vehicle_id)
    command = "SELECT serial_no FROM vehicle WHERE serial_no =: vehicle_id"
    curs.execute(command, {"vehicle_id":vehicle_id})
    if ( None == curs.fetchone()):
        print("Invalid input: serial_no does not exist.")
        return True
    else:
        return False

# error handling for buyer_id, seller_id
def IdErrCheck( id_type, connection, curs):
    format_err = True
    db_err = True
    len_err = True
    while (format_err or db_err or len_err):
        some_id = input("Enter " + id_type + ": ")
        len_err = CheckLen(some_id, 15)
        if len_err == True:
            continue;
        format_err = CheckIfInt(some_id)
        if format_err == True:
            continue;
        db_err = CheckIfIdExists(some_id, connection, curs)
        if db_err == True:
            continue;
    return int(some_id)

# error handling for buyer_id, seller_id, vehicle_id
def CheckLen(a_str, expected_len):
    if len(a_str) <= expected_len:
        return False
    else:
        print("Invalid input: Must be <=", expected_len, "digits long")
        return True

# error handling for buyer_id, seller_id
def CheckIfIdExists(some_id, connection, curs):
    some_id = int(some_id)
    command = "SELECT sin FROM people WHERE sin =: some_id"
    curs.execute(command,{"some_id":some_id})
    if ( None == curs.fetchone()):
        print("Invalid input: SIN does not exist.")
        # ask user if they would like to enter a new person
        check = input("Would you like to add this person into the database? (y/n): ")
        if (check == "y"):
            NewPerson(some_id, connection, curs)
            return False
        else: # if check == "n"
            return True
    else:
        return False

# get transaction_id and call helper function
def GenerateTransaction( connection, curs):
    command = "SELECT COUNT(*) FROM auto_sale"
    curs.execute(command)
    no_trans = curs.fetchone()[0]
    transaction_id = no_trans + 1
    return int(transaction_id)

# error handling for buyer_id, seller_id, vehicle_id
def CheckIfInt(some_id):
    if some_id.isdigit():
        return False
    else:
        print("Invalid input: must be integer")
        return True

'''
Call functions to obtain user information.
parameters: 
return values:
assumptions: 
'''
def AutoTransaction(connection, curs):

    print("\nAuto Sale Transaction:\n") 
    # generate transaction_id
    transaction_id = GenerateTransaction( connection, curs )

    # ask user to input relevant information
    buyer_id = IdErrCheck( "buyer_id", connection, curs )

    # need to confirm that seller actually owns vehicle
    owner_err = True
    while (owner_err):

        seller_id = IdErrCheck( "seller_id", connection, curs)
        vehicle_id = VehErrCheck( connection, curs)
        owner_err = OwnerCheck(seller_id, vehicle_id, connection, curs)	
    
    # obtain and check s_date information
    s_date = DateErrCheck(connection, curs).date()

    price = PriceErrCheck()

    # Display auto sale transaction information to user
    print("\nSummary of Auto Sale Transaction:")
    print("\ntransaction_id: ", transaction_id, "\nbuyer_id: ", buyer_id, \
                "\nseller_id: ", seller_id, "\nvehicle_id: ", vehicle_id, \
                "\ns_date: ", s_date, "\nprice: ", price)

    # ask user to confirm auto sale transaction information
    check = input ("\nIs this information correct? (y/n): ")
    if (check == "n"):
        print("\nAuto Sale Transaction was not added to database. Please try again.")
        AutoTransaction( connection, curs)

    # Delete owners from owners with vehicle_id
    command = "DELETE from owner WHERE vehicle_id =: Vehicle_id"
    curs.execute (command, {"Vehicle_id": vehicle_id})

    # Insert new owner_id(buyer_id), vehicle_id into owner table
    data = [(buyer_id, vehicle_id, "y")]
    curs.bindarraysize = 1
    curs.setinputsizes(15,15,1)
    curs.executemany("INSERT into owner(owner_id,vehicle_id, is_primary_owner)"
                        "VALUES (:1, :2, :3)", data)

    # Insert new transaction_id, seller_id, buyer_id, vehicle_id, s_date, price into auto_sale table
    data = [(transaction_id, seller_id, buyer_id, vehicle_id, s_date, price)]
    curs.bindarraysize = 1
    curs.setinputsizes(int, 15, 15, 15, 11, float) 
    curs.executemany( "INSERT into auto_sale VALUES (:1, :2, :3, :4, :5, :6)", data)

    print("\nAuto Sale Transaction was succesfully added to database.")

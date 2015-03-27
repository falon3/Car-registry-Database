from new_person import NewPerson
from decimal import Decimal
import datetime 

# This function takes in a valid seller_id and valid vehicle_id 
# and determines if the seller owns the vehicle they intend to sell
# That is, the database is checked to see if the seller is in the 
# owner table and owns the particular vehicle. 
def OwnerCheck(seller_id, vehicle_id, connection, curs):
    command = "SELECT owner_id FROM owner WHERE vehicle_id = %s AND owner_id = %s" % (vehicle_id, seller_id)
    curs.execute(command)
    if ( None == curs.fetchone()):
        print("Invalid input: seller does not own vehicle. Please try that again.")
        return True
    else:
        return False

# error handling for price
def PriceErrCheck():
    format_err = True
    while (format_err):
        price = input("Enter sale price (between 0.00 and 9999999.99): ")
        try:
            price = Decimal(price)
            price = round(price,2)
        except:
            print("Invalid price!")
            exit = input("Would you like to try that again? (y/n): ")
            if (exit == "n" or exit == "N"):
                return "EXIT"
            else:
                continue;
        else:
            format_err = False 

    return price

# error handling for s_date
def DateErrCheck(connection, curs):
    date_err = True
    while (date_err):
        date = input("Enter sale date, YY-MM-DD: ")
        try:
            vdate = datetime.datetime.strptime(date, "%y-%m-%d")
        except:
            print("Invalid date")
            exit = input("Would you like to try that again? (y/n): ")
            if (exit == "n" or exit == "N"):
                return "EXIT"
            else:
                continue;
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
            exit = input("Would you like to try that again? (y/n): ")
            if (exit == "n" or exit == "N"):
                return "EXIT"
            else:
                continue;
        format_err = CheckIfInt(vehicle_id)
        if format_err == True:
            exit = input("Would you like to try that again? (y/n): ")
            if (exit == "n" or exit == "N"):
                return "EXIT"
            else:
                continue;
        db_err = CheckIfVehExists(vehicle_id, connection, curs)
        if db_err == True:
            exit = input("Would you like to try that again? (y/n): ")
            if (exit == "n" or exit == "N"):
                return "EXIT"
            else:
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
            exit = input("Would you like to try that again? (y/n): ")
            if (exit == "n" or exit == "N"):
                return "EXIT"
            else:
                continue;
        format_err = CheckIfInt(some_id)
        if format_err == True:
            exit = input("Would you like to try that again? (y/n): ")
            if (exit == "n" or exit == "N"):
                return "EXIT"
            else:
                continue;
        db_err = CheckIfIdExists(some_id, connection, curs)
        if db_err == True:
            exit = input("Would you like to try that again? (y/n): ")
            if (exit == "n" or exit == "N"):
                return "EXIT"
            else:
                continue;
        if db_err == "EXIT":
            return "EXIT"
    return int(some_id)

# error handling for buyer_id, seller_id, vehicle_id
def CheckLen(a_str, expected_len):
    if len(a_str) <= expected_len:
        return False
    else:
        print("Invalid input: Must be <=", expected_len, "digits long")
        return True

# error handling for buyer_id, seller_id
# If Id doesnt exist user has option of creating a new person
def CheckIfIdExists(some_id, connection, curs):
    some_id = int(some_id)
    command = "SELECT sin FROM people WHERE sin =: some_id"
    curs.execute(command,{"some_id":some_id})
    if ( None == curs.fetchone()):
        print("Invalid input: SIN does not exist.")
        check = input("Would you like to add this person into the database? (y/n): ")
        if (check == "y"):
            # add a new person into the database
            result = NewPerson(some_id, connection, curs)
            if (result == True):
                return False
            # if person was not successfully added
            else:
                return "EXIT"
        else: # if check == "n"
            return True
    else:
        return False

# Generates transaction id number 
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
This component is used by a registering officer to create 
an auto sale transaction record.

Information needed from the user:
    - buyer's SIN (int CHAR(15))
    - seller's SIN (int CHAR(15))
    - vehicle serial number (int CHAR(15))
    - date of sale (DATE)
    - vehicle price (numeric(9,2))

Information generated by database:
    - transaction id (int)

This function obtains user information and checks the 
validity of the information sometimes by querying the 
database. If the user input is valid, it removes all 
previous vehicle owner information from owner table.
Then it adds the new owner information into owner table.
Finally, it adds a new auto sale transaction into 
the auto sale table.

parameters: connection, curs
return values: none
assumptions:
    - user is entering valid price 
'''
def AutoTransaction(connection, curs):

    print("\nAuto Sale Transaction:\n") 
    
    exit = False

    while (exit == False):

        # generate transaction_id
        transaction_id = GenerateTransaction( connection, curs )
        if (transaction_id == "EXIT"):
            break;

        # ask user to input relevant information
        buyer_id = IdErrCheck( "buyer_id", connection, curs )
        if (buyer_id == "EXIT"):
            break;    

        # need to confirm that seller actually owns vehicle
        owner_err = True
        while (owner_err):

            seller_id = IdErrCheck( "seller_id", connection, curs)
            if (seller_id == "EXIT"):
                break;
    
            vehicle_id = VehErrCheck( connection, curs)
            if (vehicle_id == "EXIT"):
                break;

            owner_err = OwnerCheck(seller_id, vehicle_id, connection, curs)	
            if (owner_err == "EXIT"):
                break;
    
        # if owner does not actually own vehicle
        if (seller_id == "EXIT" or vehicle_id == "EXIT" or owner_err == "EXIT"):
            break;

        s_date = DateErrCheck(connection, curs).date()
        if (s_date == "EXIT"):
            break;        

        price = PriceErrCheck()
        if (price == "EXIT"):
            break;

        # Display auto sale transaction information to user
        print("\nSummary of Auto Sale Transaction:")
        print("\ntransaction_id: ", transaction_id, "\nbuyer_id: ", buyer_id, \
                "\nseller_id: ", seller_id, "\nvehicle_id: ", vehicle_id, \
                "\ns_date: ", s_date, "\nprice: $", price)

        # Ask user to confirm auto sale transaction information
        check = input ("\nIs this information correct? (y/n): ")
        if (check == "n"):
            break;

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
        curs.setinputsizes(int, 15, 15, 15, 11, 9) 
        curs.executemany( "INSERT into auto_sale VALUES (:1, :2, :3, :4, :5, :6)", data)

        print("\nAuto Sale Transaction was succesfully added to database.")
        
        # exit loop succesfully
        exit = True         

    if (exit == False):
        print("\nAuto Sale Transaction was not added to database. Please try again.")

    print("\nReturning to main menu\n")

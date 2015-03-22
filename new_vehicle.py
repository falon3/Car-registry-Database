from new_person import NewPerson

# error handling for primary_owner, secondary_owner
def OwnerErrCheck( owner_type, connection, curs):
    format_err = True
    db_err = True
    len_err = True
    while (format_err or db_err or len_err):
        SIN = input("Enter SIN of " + owner_type + "_owner: ")
        len_err = CheckLen(SIN, 9)
        if len_err == True:
            continue;
        format_err = CheckIfInt(SIN)
        if format_err == True:
            continue;
        db_err = CheckIfIdExists(SIN, connection, curs)
        if db_err == True:
            continue;
    return SIN

# error handling for primary_owner, secondary_owner
# If Id doesnt exist, user has option to create a new person
def CheckIfIdExists(some_id, connection, curs):
    some_id = int(some_id)
    command = "SELECT sin FROM people WHERE sin =: some_id"
    curs.execute(command,{"some_id":some_id})
    if ( None == curs.fetchone()):
        print("Invalid input: SIN does not exist.")
        check = input("Would you like to add this person into the database? (y/n): ")
        if (check == "y"):
            # Add a new person into the database
            NewPerson(some_id, connection, curs)
            return False
        else: # if check == "n"
            return True
    else:
        return False

# error handling for type_id
def TypeErrCheck( connection, curs):
    format_err = True
    db_err = True
    while (format_err or db_err):
        type_id = input("Enter type_id: ")
        format_err = CheckIfInt(type_id)
        if format_err == True:
            continue;
        db_err = CheckIfTypeExists(type_id, connection, curs)
        if db_err == True:
            continue;
    return type_id

# error handling for type_id
def CheckIfTypeExists(type_id, connection, curs):
    type_id = int(type_id)
    command = "SELECT type_id FROM vehicle_type WHERE type_id =: Type_id"
    curs.execute(command,{"Type_id":type_id})
    if ( None == curs.fetchone()):
        print("Invalid input: type_id does not exist.")
        return True
    else:
        return False

# error handling for year
def YearErrCheck():
    len_err = True
    format_err = True
    while (format_err or len_err):
        year = input("Enter vehicle year (Eg. 1991): ")
        len_err = CheckLen(year,4)
        if len_err == True:
            continue;
        format_err = CheckIfInt(year)
        if format_err == True:
            continue;
    return int(year)

# error handling for maker, model, color
def StrErrCheck( a_str, max_len):
    len_err = True
    format_err = True
    while (format_err or len_err):
        descriptor = input ("Enter vehicle " + a_str + ": ")
        len_err = CheckLen(descriptor, max_len )
        if len_err == True:
            continue;
        format_err = CheckIfAlpha(descriptor)
        if format_err == True:
            continue;
    return descriptor

# error handling StrErrCheck
def CheckIfAlpha(a_str):
    if a_str.isalpha():
        return False
    else:
        print("Invalid input: must enter string")
        return True

# error handling for serial_no
def SerialErrCheck( connection, curs):
    format_err = True
    db_err = True
    len_err = True
    while (format_err or db_err or len_err):
        serial_no = input("Enter serial_no: ")
        len_err = CheckLen(serial_no, 15)
        if len_err == True:
            continue;
        format_err = CheckIfInt(serial_no)
        if format_err == True:
            continue;
        db_err = CheckIfVehicleExists(serial_no, connection, curs)
        if db_err == True:
            continue;
    return serial_no

# error handling for serial_no, maker, model, year, color
def CheckLen(a_str, expected_len):
    if len(a_str) <= expected_len:
        return False
    else:
        print("Invalid input: Must be <=", expected_len, "digits long")
        return True

# error handling for serial_no
def CheckIfVehicleExists(some_id, connection, curs):
    some_id = int(some_id)
    command = "SELECT serial_no FROM vehicle WHERE serial_no =: some_id"
    curs.execute(command,{"some_id":some_id})
    if ( None != curs.fetchone()):
        print("Invalid input: vehicle already exists in database.")
        return True
    else:
        return False

# error handling for serial_no, year, primary_owner, secondary_owner
def CheckIfInt(some_id):
    if some_id.isdigit():
        return False
    else:
        print("Invalid input: must be integer")
        return True

'''
This component is used by a registering officer to create
an new vehicle record and new ownership record.

Information needed from the user:
    - serial number of vehicle (int CHAR(15))
    - maker (VARCHAR(20))
    - model (VARCHAR(20))
    - year (Number(4,0))
    - color (VARCHAR(10))
    - type_id (integer)
    - primary owner sin (CHAR(15))
    - secondary owner sin (CHAR(15)) 

This function obtains user information and checks the
validity of the information sometimes by querying the
database. If the user input is valid, adds the new vehicle
information into the vehicle table.
Then it adds the new primary owner information into owner table.
If a secondary owner is given it then adds the new secondary
owner into the owner table.

parameters: connection, curs
return values: none
assumptions:
    - it is only possible to have one secondary owner
    - all vehicles must have one primary owner
    - user enters sins that are 9 digits long
    - there are some valid type_ids already entered in the 
      vehicle_type table
'''

def NewVehicle(connection, curs):
    
    print("\nNew Vehicle Registration:\n")
    serial_no = SerialErrCheck(connection, curs)
    maker = StrErrCheck( "maker", 20 )
    model = StrErrCheck( "model", 20 )
    year = YearErrCheck()
    color = StrErrCheck( "color", 10 )
    type_id = TypeErrCheck( connection, curs )

    primary_owner = OwnerErrCheck("primary", connection, curs)
    sec_owner_check = input ("Would you like to enter a secondary owner? (y/n): ")
    if (sec_owner_check == "y"):
        # must make sure that secondary_owner != primary owner
        secondary_owner = OwnerErrCheck("secondary", connection, curs)

    # Display vehicle registration information to user
    print("\nSummary of Vehicle Registration Information:")
    print("\nserial_no: ", serial_no, "\nmaker: ", maker, \
                "\nmodel: ", model, "\nyear: ", year, \
                "\ncolor: ", color, "\ntype_id: ", type_id, \
                "\nprimary owner: ",  primary_owner)
    if (sec_owner_check == "y"):
        print("secondar owner: ", secondary_owner)

    # ask user to confirm registration information
    check = input ("\nIs this information correct? (y/n): ")
    if (check == "n"):
        print("\nNew Vehicle was not added to database. Please try again.")
        NewVehicle( connection, curs)

    # Insert serial_no into vehicle table
    data = [(serial_no, maker, model, year, color, type_id)]
    curs.bindarraysize = 1
    curs.setinputsizes(15, 20, 20, int, 10, int)
    curs.executemany( "INSERT into vehicle VALUES (:1, :2, :3, :4, :5, :6)", data)

    # Insert primary_owner into owner table
    data = [(primary_owner, serial_no, "y")]
    curs.bindarraysize = 1
    curs.setinputsizes(15,15,1)
    curs.executemany("INSERT into owner VALUES (:1, :2, :3)", data)   

    # insert secondary_owner into owner table
    if (sec_owner_check == "y"):
        data = [(secondary_owner, serial_no, "n")]
        curs.bindarraysize = 1
        curs.setinputsizes(15,15,1)
        curs.executemany("INSERT into owner VALUES (:1, :2, :3)", data)
 
    print("\nVehicle was succesfully registered into the database.")


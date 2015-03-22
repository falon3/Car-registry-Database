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
        db_err = CheckIfExists(serial_no, connection, curs)
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
def CheckIfExists(some_id, connection, curs):
    some_id = int(some_id)
    command = "SELECT sin FROM people WHERE sin =: some_id"
    curs.execute(command,{"some_id":some_id})
    if ( None != curs.fetchone()):
        print("Invalid input: vehicle already exists.")
        return True
    else:
        return False

# error handling for serial_no, year
def CheckIfInt(some_id):
    if some_id.isdigit():
        return False
    else:
        print("Invalid input: must be integer")
        return True

def NewVehicle(connection, curs):

    serial_no = SerialErrCheck(connection, curs)
    maker = StrErrCheck( "maker", 20 )
    model = StrErrCheck( "model", 20 )
    year = YearErrCheck()
    color = StrErrCheck( "color", 10 )
    type_id = TypeErrCheck( connection, curs )

    # Display new vehicle information to user
    print("\nSummary of Vehicle")
    print("\nserial_no: ", serial_no, "\nmaker: ", maker, \
                "\nmodel: ", model, "\nyear: ", year, \
                "\ncolor: ", color, "\ntype_id: ", type_id)

    # ask user to confirm auto sale transaction information
    check = input ("Is this information correct? (y/n): ")
    if (check == "n"):
        print("\nNew Vehicle was not added to database. Please try again.")
        NewVehicle( connection, curs)

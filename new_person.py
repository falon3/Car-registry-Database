import datetime

''' 
assumptions: SIN is not in database and format of SIN is valid
'''

def DateErrCheck(connection, curs):
    date_err = True
    while (date_err):
        date = input("Enter birthdate, YY-MM-DD: ")
        try:
            # strptime throws an exception if userIn doesn't match the pattern
            vdate = datetime.datetime.strptime(date, "%y-%m-%d")
        except:
            print("Invalid birthdate, try again!\n")
        else:
            date_err = False
    return vdate

def CheckIfInt(some_id):
    if some_id.isdigit():
        return False
    else:
        print("Invalid input: must be integer")
        return True

def GenderErrCheck():
    format_err = True
    while (format_err):
        gender = input( "Enter gender (m/f): ")
        if (gender == "f" or gender == "m"):
            format_err = False  
        else:
            print("Invalid input: must be (m/f)") 
    return gender

def FloatErrCheck( a_str ):
    format_err = True
    while (format_err):
        measurement = input("Enter " + a_str + " of form ___.__: ")
        try:
            float(measurement)
        except:
            print("Invalid input: must be float of form ___.__: ")
        else:
            format_err = False
    return float(measurement)

def StrErrCheck( a_str, max_len):
    len_err = True
    format_err = True
    while (format_err or len_err):
        descriptor = input ("Enter person's " + a_str + ": ")
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
        return True

def CheckLen(a_str, expected_len):
    if len(a_str) <= expected_len:
        return False
    else:
        print("Invalid input: Must be <=", expected_len, "digits long")
        return True

def NewPerson( SIN, connection, curs):
    name = StrErrCheck( "name ", 40)
    height = FloatErrCheck("height")
    weight = FloatErrCheck("weight")
    eyecolor = StrErrCheck("eyecolor", 10) 
    haircolor = StrErrCheck("haircolor", 10)
    addr = StrErrCheck( "address", 50)
    gender = GenderErrCheck()
    birthday = DateErrCheck( connection, curs)

    # Display new person information to user
    print("\nSummary of New Person")
    print("\nsin: ", SIN, "\nname: ", name, "\nheight: ", height, \
                "\nweight: ", weight, "\neyecolor: ", eyecolor, \
                "\nhaircolor: ", haircolor, "\naddress: ", addr, \
                "\ngender: ", gender, "\nbirthday: ", birthday)

    # ask user to confirm auto sale transaction information
    check = input ("Is this information correct? (y/n): ")
    if (check == "n"):
        print("\nNew Person was not added to database. Please try again.")
        NewPerson( SIN, connection, curs)
    
    # Insert new person into people table
    data = [(SIN, name, height, weight, eyecolor, haircolor, addr, gender, birthday)]
    curs.bindarraysize = 1
    curs.setinputsizes(15, 40, float, float, 10, 10, 50, 1)
    curs.executemany("INSERT into people (sin, name, height, weight, eyecolor, haircolor, addr, gender, birthday)"
                        "VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)", data)

    print("\nPerson was succesfully added to database.")
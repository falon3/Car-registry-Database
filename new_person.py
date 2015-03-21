''' 
assumptions: SIN is not in database and format of SIN is valid
'''

# formatting date
def FormatDate(year, month, day):
    return day + "-" + month + "-" + year

# error handling for day
def DayErrCheck():
    len_err = True
    format_err = True
    while (format_err or len_err):
        day = input("Enter day of birth (eg. 25, 01): ")
        len_err = CheckLen(day, 2)
        if len_err == True:
            continue;
        format_err = CheckIfInt(day)
        if format_err == True:
            continue;
    return day

# error handling for year
def YearErrCheck():
    len_err = True
    format_err = True
    while (format_err or len_err):
        year = input ("Enter year of birth (eg. 1991): ")
        len_err = CheckLen(year, 4)
        if len_err == True:
            continue;
        format_err = CheckIfInt(year)
        if format_err == True:
            continue;
    return year

# error handling for month
def MonthErrCheck():
    len_err = True
    format_err = True
    while (format_err or len_err):
        month = input ("Enter month of birth (eg. FEB): ")
        len_err = CheckLen(month, 3)
        if len_err == True:
            continue;
        format_err = CheckIfAlpha(month)
        if format_err == True:
            continue;
    return month.upper()

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

    year = YearErrCheck()
    month = MonthErrCheck()
    day = DarErrCheck()

    birthday = FormatDate(year, month, day)

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


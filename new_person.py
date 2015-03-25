import datetime

#error handling for birthday
def DateErrCheck(connection, curs):
    date_err = True
    while (date_err):
        date = input("Enter birthdate, YY-MM-DD: ")
        try:
            vdate = datetime.datetime.strptime(date, "%y-%m-%d")
        except:
            print("Invalid birthdate")
            exit = input("Would you like to try that again? (y/n): ")
            if (exit == "n" or exit == "N"):
                return "EXIT"
        else:
            date_err = False
    return vdate

# error handling for gender
def GenderErrCheck():
    format_err = True
    while (format_err):
        gender = input( "Enter gender (m/f): ")
        if (gender == "f" or gender == "m"):
            format_err = False  
        else:
            print("Invalid input: must be (m/f)")
            exit = input("Would you like to try that again? (y/n): ")
            if (exit == "n" or exit == "N"):
                return "EXIT" 
    return gender

# error handling for height, weight
def FloatErrCheck( a_str ):
    format_err = True
    while (format_err):
        measurement = input("Enter " + a_str + " (between 0.00 and 999.99): ")
        try:
            float(measurement)
        except:
            print("Invalid input: must be number between 0.00 and 999.99: ")
            exit = input("Would you like to try that again? (y/n): ")
            if (exit == "n" or exit == "N"):
                return "EXIT"
        else:
            format_err = False
    return measurement

# error handling for name, eyecolor, haircolor, addr, gender
def StrErrCheck( a_str, max_len):
    len_err = True
    while (len_err):
        descriptor = input ("Enter person's " + a_str + ": ")
        if (len(a_str) <= max_len):
            len_err = False
        else:
            print("Invalid input: Must be <=", + max_len, + "digits long")
            exit = input("Would you like to try that again? (y/n): ")
            if (exit == "n" or exit == "N"):
                return "EXIT"
    return descriptor

'''
This component is used to create a new person in the database.

Information needed from the user:
    - person's name (CHAR(40))
    - person's height (number(5,2))
    - person's weight (number(5,2))
    - person's eyecolor (VARCHAR(10))
    - person's haircolor (VARCHAR(10))
    - person's addresss (VARCHAR(50))
    - person's gender (CHAR(1))
    - person's birthday (DATE)

This function obtains user information and checks the
validity of the information.
If the user input is valid, it adds the new person into
the people table in the database

parameters: sin, connection, curs
return values: none
assumptions:
    - user will enter valid alpha strings (spaces permitted)
    - sin is valid (9 digits long) and does not already
      exist in the database
'''

def NewPerson( SIN, connection, curs):

    print("\nNew Person:\n")    

    exit = False

    while (exit == False):
        
        name = StrErrCheck( "name", 40)
        if (name == "EXIT"):
            break;

        height = FloatErrCheck("height")
        if (height == "EXIT"):
            break;

        weight = FloatErrCheck("weight")
        if (weight == "EXIT"):
            break;

        eyecolor = StrErrCheck("eyecolor", 10) 
        if (eyecolor == "EXIT"):
            break;

        haircolor = StrErrCheck("haircolor", 10)
        if (haircolor == "EXIT"):
            break;

        addr = StrErrCheck( "address", 50)
        if (addr == "EXIT"):
            break;        

        gender = GenderErrCheck()
        if (gender == "EXIT"):
            break;    

        birthday = DateErrCheck( connection, curs)
        if (birthday == "EXIT"):
            break;
        
        birthday = birthday.date()
        
        # Display new person information to user
        print("\nSummary of New Person: ")
        print("\nsin: ", SIN, "\nname: ", name, "\nheight: ", height, \
                "\nweight: ", weight, "\neyecolor: ", eyecolor, \
                "\nhaircolor: ", haircolor, "\naddress: ", addr, \
                "\ngender: ", gender, "\nbirthday: ", birthday)

        # ask user to confirm auto sale transaction information
        check = input ("\nIs this information correct? (y/n): ")
        if (check == "n"):
            print("\nNew Person was not added to database. Please try again.")
            break;
    
        # Insert new person into people table
        data = [(SIN, name, height, weight, eyecolor, haircolor, addr, gender, birthday)]
        curs.bindarraysize = 1
        curs.setinputsizes(15, 40, float, float, 10, 10, 50, 1)
        curs.executemany("INSERT into people (sin, name, height, weight, eyecolor, haircolor, addr, gender, birthday)"
                        "VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)", data)

        print("\nPerson was succesfully added to database.")
        
        # exit loop sucessfully
        exit = True

    return exit

import datetime


def GetValidSin(connection, curs, ID_type):
    """
    GetValidSin repeatedly asks the user for the SIN they want to enter
    until the input meets the requirements of being a 9-digit integer. Then it
    is queiried whether or not the SIN exists in the system yet for a person
    since this is a requirment for issuing a violation record.
    Returns valid SIN

    args:
        ID_type: a string specifying if ID type is 'SIN' or 'officer id"
                 for user's convenience only since our verification is same for
                 either number in the system.
    """

    # prompt for ID_type from user input and check digits and type
    Sin = input("enter " + ID_type + ":  ")
    while ((Sin.isdigit() == False) or (len(Sin) != 9)):
        print("You didn't enter a 9-digit integer " + ID_type + "!\n")
        Sin = input("enter " + ID_type + ":  ")

    # check if SIN in system. Recurse function call if not.
    do = "select * from people where SIN =: sin"
    curs.execute(do, {'sin':Sin})
    person = curs.fetchall()
    
    if person == None:
        print("That " + ID_type + " doesn't exist!")
        GetValidSin(connection, curs, ID_type)

    return Sin

def GetValidVin(connection, curs):
    """
    GetValidVin repeatedly asks the user for the VIN(vehicle identifiaction number)
    they want to enter until the input meets the requirements of being an integer. 
    Then it is queried whether or not the VIN exists in the system yet 
    for a vehicle since this is a requirment for issuing a violation record.
    Returns valid VIN(more commonly referred to as serial number)
    """
    
    # get VIN as user input and check digits and type
    Vin = input("enter vehicle's serial number:  ")
    while (Vin.isdigit() == False):
        print("You didn't enter an integer serial number!\n")
        Vin = input("enter vehicle's serial number:  ")

    # convert type to int from str
    Vin = int(Vin)

    # check if VIN in system. Recurse function call if not.
    do = "select * from vehicle where serial_no =: vin"
    curs.execute(do, {'vin':Vin})
    vehicle = curs.fetchone()

    if vehicle == None:
        print("That serial number doesn't exist!")
        GetValidVin(connection, curs)

    return Vin

def GetValidDate(connection, curs):
    
    ValidDate = False
    while not ValidDate:
        userIn = input("enter date, YY-MM-DD: ")

        try:
            # strptime throws an exception if userIn doesn't match the pattern
            ValidDate = datetime.datetime.strptime(userIn, "%y-%m-%d")
        except:
            print("Invalid date, try again!\n")

    return ValidDate


def ViolationRecord(connection, curs):
    '''
    This component is used by a police officer to issue a traffic ticket
    and record the violation.

    information needed from the user(police officer):
        -violator's SIN (9 digit integer CHAR)
        -violator's VIN (integer CHAR)
        -officer's ID   (integer CHAR)
        -violation type (char)
        -date           (YYYY-MM-DD date)
        -location of violation  (varchar)
        -any notes about the incident  (varchar)

    information that can be obtained from in the database already:
        -ticket number

    Obtain the informaton needed from user and database to create a 
    ticket record in the database table 'ticket'. Need to check user input
    for validity. The information entered needs to match the formats listed
    above and the SIN, VIN, officer no., and violation type has to exist in the system already
    to be be valid.
    '''
    print("New Violation Record Form")
    # get number of tickets to make new integer ticket number
    curs.execute("select COUNT(*) from ticket") 
    num_tickets = curs.fetchone()[0]
    
    new_ticket_num = str(num_tickets + 1)

    # get valid SIN from user
    Violator_SIN = GetValidSin(connection, curs, 'SIN')
    # get valid VIN from user
    Vehicle_ID = GetValidVin(connection, curs)
    # get valid officer id from user
    officer_id = GetValidSin(connection, curs, 'officer ID')

 
    exists = None
    # get type of violation from user and check if a valid violation
    while exists == None:

        v_type = input("enter type of violation: ")
        query = "select * from ticket_type where vtype =: vio"
        curs.execute(query, {'vio':v_type})
        exists = curs.fetchall()

        if exists == None:
            print("invalid violation type!\n")

    vdate = GetValidDate(connection,curs)
            
    # get location
    location = '0'
    while location.isalpha() == False: # CHANGE THIS BECAUSE DOESN'T ALLOW FOR SPACES
        """
        Check if string entered is all letters and keep prompting 
        user to re-enter until it is all letters. Trust that 
        they entered a valid city name if all letters
        """
        location = input("city of violation: ")
    
        if location.isalpha() == False:
            print("that wasn't an alphabetic location!\n")

    # ask for violation description
    notes = input("description of violation made: ")
    # notes section cannot be empty or get errors
    if not notes:
        notes = " "

    # CREATE TICKET RECORD
    # insert new ticket_no, violator_no, vehicle_id, office_id, vtype, vdate, 
    # place, descriptions into ticket table
    Values = [(new_ticket_num, Violator_SIN, Vehicle_ID, officer_id, v_type, \
                  vdate, location, notes)]
    curs.bindarraysize = 1
    
    curs.setinputsizes(int, 15, 15, 15, 10, 11, 20, 1024)
    curs.executemany("INSERT into ticket VALUES (:1, :2, :3, :4, :5, :6, :7, :8)", Values)
    
    print("\n Violation Record successfully created\n")
                  
    


    

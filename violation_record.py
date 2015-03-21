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
        

    Sin = int(Sin)
    # check if SIN in system. Recurse function call if not.
    do = "select * from people where SIN =: sin"
    curs.execute(do, {'sin':Sin})
    person = curs.fetchone()
    
    if person == None:
        print("That " + ID_type + " doesn't exist in the system!")
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
        print("That serial number doesn't exist in the system!")
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
    above and the SIN, VIN, officer no., and violation type has to exist in 
    the system already to be be valid.
    '''
    print("New Violation Record Form")
    # get number of tickets to make new integer ticket number
    curs.execute("select COUNT(*) from ticket") 
    num_tickets = curs.fetchone()[0]
    
    new_ticket_num = str(num_tickets + 1)

    # get valid VIN from user
    Vehicle_ID = GetValidVin(connection, curs)
    # get valid SIN from user if not 
    Violator_SIN = GetValidSin(connection, curs, 'SIN')   
    # get valid officer id from user
    officer_id = GetValidSin(connection, curs, 'officer ID')

    # get type of violation from user and check if a valid violation
    exists = None
    while exists == None:

        v_type = input("enter type of violation: ")
        v_type = v_type.upper()
        #v_type = v_type.strip()
        print("|"+ v_type +"|")
        
        query = "select * from ticket_type where UPPER(vtype) = '" +v_type + "'"
        curs.execute(query)
        exists = curs.fetchone()
        print(exists)

        if exists == None  :
            print("invalid violation type!\n")


    # get date of violation from user
    vdate = GetValidDate(connection,curs)
         
    # get place violation happened from user
    location = input("location of violation: ")

    # ask for any violation descriptions
    notes = input("description of violation made: ")
    if not notes: # notes section cannot be empty or get errors
        notes = "NULL"

    # Print all details back to user to verify correct before inserting data
    print("\n Summary of Violation \n")
    print("Ticket_no: ", new_ticket_num, "\n Violator's SIN: ", Violator_SIN, \
              "\n Serial_no: ", Vehicle_ID, "\n Officer_id: ",officer_id, \
              "\n violation type: ", v_type, "\n Date: ", vdate, \
              "\n location: ", location, "\n notes: ", notes)

    # if user claims the information is not correct then start over and re-do it
    confirmation = input("\n Is this information correct (y/n)?")
    if (confirmation == 'n' or confirmation == 'N'):
        print("Okay let's try that again \n")
        ViolationRecord(connection, curs)


    # Now ready to CREATE TICKET RECORD
    # insert new ticket_no, violator_no, vehicle_id, office_id, vtype, vdate, 
    # place, descriptions into ticket table
    Values = [(new_ticket_num, Violator_SIN, Vehicle_ID, officer_id, v_type, \
                  vdate, location, notes)]
    curs.bindarraysize = 1
    
    curs.setinputsizes(int, 15, 15, 15, 10, 11, 20, 1024)
    curs.executemany("INSERT into ticket VALUES \
                    (:1, :2, :3, :4, :5, :6, :7, :8)", Values)
    
    print("\n Violation Record successfully created\n")
                  
    


    

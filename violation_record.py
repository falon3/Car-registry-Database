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
    ValidSin = False
    while not ValidSin:
        # prompt for ID_type from user input and check type is int
        Sin = input("enter " + ID_type + ":  ")
        if len(Sin) <= 15:    
            try: 
                Sin = int(Sin)
                ValidSin = True              
            except ValueError:
                print("\n You didn't enter an integer!")
                again = input("Do you want to try again?\n (y/n): ")
                if again == 'n' or again == 'N':
                    return False
        else:
            again = input("Input too large! Do you want to try again?\n (y/n): ")
            if again == 'n' or again == 'N':
                return False
      
    # check if SIN in system. Recurse function call if not.
    do = "select * from people where SIN =: sin"
    curs.execute(do, {'sin':Sin})
    person = curs.fetchone()
    
    # prompt user again until valid SIN recieved
    if person == None:
        print("\n That " + ID_type + " doesn't exist in the system!")
        again = input("Do you want to try again?\n (y/n): ")
        if again == 'n' or again == 'N':
            return False

        Sin = GetValidSin(connection, curs, ID_type)

    return Sin

def GetValidVin(connection, curs):
    """
    GetValidVin repeatedly asks the user for the VIN(vehicle identifiaction number)
    they want to enter until the input meets the requirements of being an integer. 
    Then it is queried whether or not the VIN exists in the system yet 
    for a vehicle since this is a requirment for issuing a violation record.
    Returns valid VIN(more commonly referred to as serial number)
    """
    ValidVin = False
    # get VIN as user input and check type is numeric
    while not ValidVin:
        Vin = input("enter vehicle's serial number:  ")
        if len(Vin) <= 15:
            try: 
                Vin = int(Vin)
                ValidVin = True
            except ValueError:
                print("\n You didn't enter an integer!")
                again = input("Do you want to try again?\n (y/n): ")
                if again == 'n' or again == 'N':
                    return False
        else:
            again = input("Input too large! Do you want to try again?\n (y/n): ")
            if again == 'n' or again == 'N':
                return False
    
    # check if VIN in system. Recurse function call if not.
    do = "select * from vehicle where serial_no =: vin"
    curs.execute(do, {'vin':Vin})
    vehicle = curs.fetchone()

    if vehicle == None:
        print("\n That serial number doesn't exist in the system!")
        again = input("Do you want to try again?\n (y/n): ")
        if again == 'n' or again == 'N':
            return False

        Vin = GetValidVin(connection, curs)

    return Vin

def GetValidDate(connection, curs):
    
    ValidDate = False
    while not ValidDate:
        userIn = input("enter date, YY-MM-DD: ")

        try:
            # strptime throws an exception if userIn doesn't match the pattern
            ValidDate = datetime.datetime.strptime(userIn, "%y-%m-%d")
        except:
            again = input("Invalid date! Do you want to try again?\n (y/n): ")
            if again == 'n' or again == 'N':
                return False

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
    do_query = False
    # main loop for entire function
    while do_query == False: 
        print("\n  New Violation Record Form")
        # get number of tickets to make new integer ticket number
        curs.execute("select COUNT(*) from ticket") 
        num_tickets = curs.fetchone()[0]
    
        new_ticket_num = str(num_tickets + 1)
        
        # get valid VIN from user
        Vehicle_ID = GetValidVin(connection, curs)
        # user quit
        if not Vehicle_ID:
            return

        # get valid SIN from user if primary owner is not violator 
        # (and violator is known) 
        isRadar = ""
        while ((isRadar != "Y") and (isRadar != "N")):
            isRadar = input("Is this ticket being issued to the primary owner of the vehicle? \n (y/n):  ")
            isRadar = isRadar.upper()
    
            if isRadar == "N": 
                # prompt user for violator's SIN
                Violator_SIN = GetValidSin(connection, curs, 'SIN')
        
            elif isRadar == "Y":  
                # violator is primary owner of vehicle and get their SIN from database
                getSIN = "select owner_id from owner where vehicle_id = :vid and UPPER(is_primary_owner) = 'Y' "
                curs.execute(getSIN, {'vid':Vehicle_ID})
                Violator_SIN = int(curs.fetchone()[0])
    
        # user quit
        if not Violator_SIN:
            return

        # get valid officer id from user
        officer_id = GetValidSin(connection, curs, 'officer ID')
        if not officer_id:
            return

        # get type of violation from user and check if a valid violation
        exists = None
        while exists == None:

            v_type = input("enter type of violation (max 10 characters): ")
            if len(v_type) <= 10:
                query = "select * from ticket_type where TRIM((vtype)) = :vio"
                curs.execute(query, {'vio':v_type})
                exists = curs.fetchone()

                if exists == None  :
                    print("\ninvalid violation type! ")
                    again = input("Do you want to try again?\n (y/n): ")
                    if again == 'n' or again == 'N':
                        return
            else:
                again = input("Input too large! Do you want to try again?\n (y/n): ")
                if again == 'n' or again == 'N':
                    return

    
        # get date of violation from user
        vdate = GetValidDate(connection,curs).date()
        # user quit
        if not vdate:
            return

        while True:
            # get place violation happened from user (max 20 characters)
            location = input("location of violation: ")
            if len(location) <= 20:
                break
            else:
                again = input("Input too large! Do you want to try again?\n (y/n): ")
                if again == 'n' or again == 'N':
                    return

        while True:
            # ask for any violation descriptions
            notes = input("description of violation made: ")
            if not notes: # notes section cannot be empty or get errors
                notes = "NULL"
                break
            if len(notes) <= 1024:
                break
            else:
                again = input("Input too large! Do you want to try again?\n (y/n): ")
                if again == 'n' or again == 'N':
                    return

        # Print all details back to user to verify correct before inserting data
        print("\n Summary of Violation \n")
        print(" Ticket_no: ", new_ticket_num, "\n Violator's SIN: ", Violator_SIN, \
              "\n Serial_no: ", Vehicle_ID, "\n Officer_id: ",officer_id, \
              "\n violation type: ", v_type, "\n Date: ", vdate, \
              "\n location: ", location, "\n notes: ", notes)

        # if user claims the information is not correct then start over and re-do it
        confirmation = input("\n Is this information correct? \n (y/n): ")
        if (confirmation == 'n' or confirmation == 'N'):
            again = input("Do you want to try again?\n (y/n): ")
            if again == 'n' or again == 'N':
                return
        elif confirmation == 'y' or confirmation == 'Y':
            do_query = True  # exit main loop


    # Now ready to CREATE TICKET RECORD
    # insert new ticket_no, violator_no, vehicle_id, office_id, vtype, vdate, 
    # place, descriptions into ticket table
    Values = [(new_ticket_num, Violator_SIN, Vehicle_ID, officer_id, v_type, \
                  vdate, location, notes)]
    curs.bindarraysize = 1
    
    curs.setinputsizes(int, 15, 15, 15, 10, 11, 20, 1024)
    curs.executemany("INSERT into ticket VALUES(:1, :2, :3, :4, :5, :6, :7, :8)", Values)
    
    print("\n Violation Record successfully created\n")
                  
    


    

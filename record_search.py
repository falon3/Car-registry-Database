import datetime

def DriverRecord(connection, curs):
    '''
    Driver Record gives the name, licence_no, addr, birthday, class,
    driving_condition, and expiring_date for a driver that is searched via 
    a query into the database using what the user entered as the name or 
    licence number.

    input: user requested for name(case insensitive), or licence number

    output: a list of all of the results or a message saying the record doesn't exist
    '''

    Name_DL = input("Enter driver name or licence number  ")
    # decide if user entered a name or license number
 
    if Name_DL[0].isalpha(): # user entered name
        Name = Name_DL.upper()
        query = "SELECT p.name as name, dl.licence_no as licence_no, p.addr as address, \
                 p.birthday as DOB, dl.class as driving_class, \
                 dl.expiring_date as expiring_date, dc.description as driving_condition \
                 FROM people p, drive_licence dl, driving_condition dc, restriction r \
                 WHERE TRIM(UPPER(p.name)) = :NA and \
                       p.sin = dl.sin and \
                       dc.c_id (+)= r.r_id and \
                       r.licence_no (+)= dl.licence_no"
        curs.execute(query, {'NA':Name})
        
    else: # user entered licence number
        DL_num = int(Name_DL)
        query = "SELECT p.name as name, dl.licence_no as licence_no, p.addr as address, \
                 p.birthday as DOB, dl.class as driving_class, \
                 dl.expiring_date as expiring_date, dc.description as driving_condition \
                 FROM people p, drive_licence dl, driving_condition dc, restriction r \
                 WHERE dl.licence_no = :DL and \
                       p.sin = dl.sin and \
                       dc.c_id (+)= r.r_id and \
                       r.licence_no (+)= dl.licence_no"
        curs.execute(query, {'DL':DL_num})

    # get and format the info retrieved if any
    Record = curs.fetchall()
    if Record == []:
        print("\n Record does not exist")
        RecordSearch(connection, curs)

    # print the results for all entires including duplicates
    for row in Record:
        print("\n Name: ", row[0])
        print(" Licence no.: ", row[1])
        print(" Address: ", row[2])
        print(" Date of Birth: ", row[3].date())
        print(" Driving Class: ", row[4])
        print(" Expiration date: ", row[5].date())
        print(" Driving condition: ", row[6])
        
        
def DriverAbstract(connection, curs):
    '''
    Driver Abstract lists all of the violations for a driver that 
    is searched via a query into the database using what the user 
    entered as the driver's SIN or licence number.

    input: user requested for SIN, or licence number

    output: a list of all of the violations or a message saying there 
            is no violation history
    '''

    ID_num = input("Enter driver SIN or licence number  ")
    # decide if user entered a name or license number
    ID_num = int(ID_num)

    # see if if was a SIN that exists
    test = "select * from people where sin = :SIN"
    curs.execute(test, {'SIN':ID_num})
    try_SIN = curs.fetchone()

    if try_SIN: # if SIN then get history from sin
        query = "select * from ticket where violator_no = :sin"
        curs.execute(query, {'sin':ID_num})
        history = curs.fetchall()
      
    else:  # it was a licence number entered get history this way
        do = " select * from ticket \
               where violator_no = (select sin from drive_licence \
                                    where licence_no = :licence )"
        curs.execute(do, {'licence':ID_num})
        history = curs.fetchall()
    
    if not history: 
        # if person does not exist in the system or if they had 
        # no violations this message is printed
        print("\nNo violation history\n")

    else: # print out each violation ever recieved by driver
        for row in history:
            print("\n Ticket Numer: ", row[0])
            print(" Violator SIN: ", row[1])
            print(" Vehicle Serial_no: ", row[2])
            print(" Officer ID: ", row[3])
            print(" Violation Type: ", row[4])
            print(" Date of Violation: ", row[5].date())
            print(" Violation Location: ", row[6], "\n")
 

def VehicleHistory(connection, curs):
    pass

def RecordSearch(connection, curs):
    """
    Search engine for car registry database.

    can search for:
    -the name, licence_no, addr, birthday, driving class, driving_condition,
    and the expiring_data of a driver by entering either a licence_no or a
    given name

    -all violation records received by a person if  the drive licence_no or 
    sin of a person  is entered.

    -the vehicle_history, including the number of times that a vehicle has 
    been changed hand, the average price, and the number of violations it 
    has been involved by entering the vehicle's serial number
    """

    print("\n\n Record Search Engine \n")

    print("1. Driver information\n")
    print("2. Driver's Abstract\n")
    print("3. Vehicle History\n")
    print("4. Return to Main Menu\n")
  
    select = input("Select an option ")

    if select == '1':
        DriverRecord(connection, curs)

    elif select == '2':
        DriverAbstract(connection, curs)

    elif select == '3':
        VehicleHistory(connection, curs)

    elif select == '4':
        Menu(connection, curs)

    else:
        print("\nthat wasn't a valid option!\n")
        RecordSearch(connection, curs)
    
    # display search results until user presses enter again
    userIn = input("\nPress enter to return to Record Search Engine  ")
    RecordSearch(connection, curs)

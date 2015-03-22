import datetime

def DriverRecord(connection, curs):

   # select name, licence_no(drive_licence), addr, birthday, class(drive_licence), driving_condition    
	# (driving_condition and restriction), expiring_date(drive_licence) 

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

    # get and format the info retrieved
    Record = curs.fetchall()
    if Record == []:
        print("\n Record does not exist")
        RecordSearch(connection, curs)

    # print the results for all entires including duplicates
    for row in Record:
        name = Record[0][0]
        licence_no = Record[0][1]
        address = Record[0][2]
        birthday = Record[0][3].date()
        driving_class = Record[0][4]
        expiring_date = Record[0][5].date()
        driving_condition = Record[0][6]
        print("\n Name: ", name)
        print(" Address: ", address)
        print(" Date of Birth: ", birthday)
        print(" Driving Class: ", driving_class)
        print(" Expiration date: ", expiring_date)
        print(" Driving condition: ",driving_condition)
        
        

def DriverAbstract(connection, curs):
    pass

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
    
    userIn = input("\nPress enter to return to Record Search Engine\n  ")
    RecordSearch(connection, curs)

def DriverRecord(connection, curs):

   # select name, licence_no(drive_licence), addr, birthday, class(drive_licence), driving_condition    
	# (driving_condition and restriction), expiring_date(drive_licence) 

    Name_DL = input("Enter driver name or licence number  ")

    # decide if user entered a name or license number 
    if Name_DL[0].isalpha(): # user entered name
        pass

    else: # user entered licence number
        pass
        

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

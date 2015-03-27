import datetime
from decimal import Decimal

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
    
    try: # if integer entered assume it was valid licence number
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

    except ValueError: # not a number entered so must be a name
        Name = Name_DL.upper() # make query case-insentive
        query = "SELECT p.name as name, dl.licence_no as licence_no, p.addr as address, \
                 p.birthday as DOB, dl.class as driving_class, \
                 dl.expiring_date as expiring_date, dc.description as driving_condition \
                 FROM people p, drive_licence dl, driving_condition dc, restriction r \
                 WHERE TRIM(UPPER(p.name)) = :NA and \
                       p.sin = dl.sin and \
                       dc.c_id (+)= r.r_id and \
                       r.licence_no (+)= dl.licence_no"
        curs.execute(query, {'NA':Name})
        
  
    # get and format the info retrieved if any
    Record = curs.fetchall()
    if Record == []:
        print("\n Record does not exist")

    else:
    # print the results for all entires including duplicates
        for row in Record:
            
            # could possibly be null
            if row[0]:
                print("\n Name: ", row[0])
            else:
                print("\n Name: ")
            
            # is a key so cant be NULL
            print(" Licence no.: ", row[1])
            
            # could possibly be null
            if row[2]:
                print(" Address: ", row[2])
            else:
                 print(" Address: ")
        
            # could possibly be null
            if row[3]:
                print(" Date of Birth: ", row[3].date())
            else:
                print(" Date of Birth: ")

            # could possibly be null
            if row[4]:
                print(" Driving Class: ", row[4])
            else: 
                print(" Driving Class: ")
    
            # could possibly be null
            if row[5]:
                print(" Expiration date: ", row[5].date())
            else:
                print(" Expiration date: ")

            # not sure if this could could possibly be NULL,
            # so just incase, here is some error handling
            if row[6]:
                print(" Driving condition: ", row[6])
            else:
                print(" Driving condition: \n")
        
def DriverAbstract(connection, curs):
    '''
    Driver Abstract lists all of the violations for a driver that 
    is searched via a query into the database using what the user 
    entered as the driver's SIN or licence number.

    input: user requested for SIN, or licence number

    output: a list of all of the violations or a message saying there 
            is no violation history
    '''

    ID_num = False
    while not ID_num:
    # needs to be an int
        try:
            ID_num = int(input("Enter driver SIN or licence number  "))
        
        except ValueError: # let the user retry
            again = input("That wasn't an integer! Do you want to try again?\n (y/n): ")
            if again == 'n' or again == 'N':
                return

    # see if it was a SIN that exists
    test = "select * from people where sin = :SIN"
    curs.execute(test, {'SIN':ID_num})
    try_SIN = curs.fetchone()

    if try_SIN: # if didn't return 'none' then it was valid sin entered
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

            # these are all keys (primary or foreign) so can't possibly be NULL
            print("\n Ticket Number: ", row[0])
            print(" Violator SIN: ", row[1])    
            print(" Vehicle Serial_no: ", row[2])
            print(" Officer ID: ", row[3])
            print(" Violation Type: ", row[4])
            
            # could possibly be null
            if row[5]:
                print(" Date of Violation: ", row[5].date())
            else:
                print(" Date of Violation: ")        
            # could possibly be null
            if row[6]:
                print(" Violation Location: ", row[6], "\n")
            else:
                print(" Violation Location: \n")
            
def VehicleHistory(connection, curs):
    '''
    Vehicle History lists the number of times that a vehicle has been changed
    hand, the average price, and the number of violations it has been involved
    in by entering the vehicle's serial number.

    history is searched via a query into the database using what the user 
    entered as the vehicle's serial number.

    input: user prompted for serial_no

    output: a list of all of the vehicle's history or a message saying there 
            is no history available for that vehicle
    '''
    valid = False
    while not valid:
        try: 
            VIN = int(input("Enter vehicle's serial number:  "))
            valid = True

        except ValueError: # let the user retry
            again = input("That wasn't an integer! Do you want to try again?\n (y/n): ")
            if again == 'n' or again == 'N':
                return

    # get vehicle history from database
    query = "SELECT  h.serial_no, count(DISTINCT transaction_id), \
            avg(price), count(DISTINCT t.ticket_no) \
            FROM    vehicle h, auto_sale a1, ticket t \
            WHERE   t.vehicle_id (+) = h.serial_no AND \
                    a1.vehicle_id (+) = h.serial_no AND \
                    h.serial_no = :vin \
            GROUP by h.serial_no"

    curs.execute(query, {'vin':VIN})
    v_history = curs.fetchone()
 
    if not v_history: 
        # if vehicle serial number does not exist in the system
        print("\nNo history for that vehicle available\n")

    else: # print out vehicle history
        print("\n Vehicle History \n")
        # these can't possibly be null
        print(" Serial Numer: ", v_history[0])
        print(" Number of Sale Transactions: ", v_history[1])
        
        # format average price for printing considering case if not been in any transactions yet
        if not v_history[2]:
            price = Decimal(0.00)
        else:
            price = Decimal(v_history[2])   
            price = round(price,2)

        print(" Average Price Sold For: $", price)
        print(" Number of Violations Involved in: ", v_history[3])
       

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
        # display search results until user presses enter again
        userIn = input("\nPress enter to return to Main Menu  ")

    elif select == '2':
        DriverAbstract(connection, curs)
        # display search results until user presses enter again
        userIn = input("\nPress enter to return to Main Menu  ")

    elif select == '3':
        VehicleHistory(connection, curs)
        # display search results until user presses enter again
        userIn = input("\nPress enter to return to Main Menu  ")

        # if user presses '4' function returns to menu
        # otherwise invalid input
    elif select > '4' or select == '0' or select.isdigit() == False:
        print("\nthat wasn't a valid option!")
        RecordSearch(connection, curs)
    
def exit():
    pass


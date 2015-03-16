def ViolationRecord(connection, curs):
    '''
    This component is used by a police officer to issue a traffic ticket
    and record the violation.
    '''
    print("New Violation Record Form")
    # get number of tickets to make ticket number
    curs.execute("select COUNT(*) from ticket") 
    num_tickets = curs.fetchone()[0]
    
    new_ticket_num = str(num_tickets + 1)

    print(new_ticket_num)

    # get necessary ticket details from user
    SIN = input("violator's SIN:  ")
    VIN = input("vehicle identification number: ")
    officer_id = input("issuing officer's ID: ")
    v_type = input("type of vehicle: ")
    date = input("date of violation: ")
    location = input("city of violation: ")
    notes = input("description of violation made: ")
    


    

import sys
import cx_Oracle
import getpass
from new_vehicle import NewVehicle
from violation_record import ViolationRecord
from new_driver import NewDriver
from record_search import RecordSearch
from new_auto_transaction import AutoTransaction
# 1. from filename (without .py) import functionname
# OR 2. import filename
# in the first case you call with functionname
# in the second case you call with filename.functionname
# from filename import functionname as thisfunction

def Exit():

    connection.close()   
    print("\nGoodBye!")
    exit()
         
def Menu(connection, curs):
    
    print("\n\n       MAIN MENU \n")
    print("1. New Vehicle Registration\n")
    print("2. Auto Transaction\n")
    print("3. Driver License Registration\n")
    print("4. Violation Record\n")
    print("5. Search Engine\n")
    print("6. Exit Auto Registration System\n")

    select = input("Select an option: ")
    
    if select == '1':
        NewVehicle(connection, curs)
    
    elif select == '2':
        AutoTransaction(connection, curs)
	
    elif select == '3':
        NewDriver(connection, curs)
   
    elif select == '4':
        ViolationRecord(connection, curs)

    elif select == '5':
        RecordSearch(connection, curs)
    
    elif select == '6':
        Exit()

    else: 
        print("Error, invalid input.")

    Menu(connection, curs)

if __name__ == "__main__":

    login_err = True
    while (login_err):
        try:
            ccid = input('\nEnter your CCID: ')
            password = getpass.getpass('Password: ')
            login = ccid + '/' + password + '@gwynne.cs.ualberta.ca:1521/CRS'
            connection = cx_Oracle.connect(login)
            # this makes everything auto commit so no worries of exiting before commiting new info
            connection.autocommit = 1
            curs = connection.cursor()
        
            '''
            # drop table
            dropTable = ("drop table TOFFEES")
            curs.execute(dropTable)

            # make table
            createStr = ("create table TOFFEES "
	        "(T_NAME VARCHAR(32), SUP_ID INTEGER, PRICE FLOAT, SALES INTEGER, TOTAL INTEGER)")
            curs.execute(createStr)
        
            data = [('Quadbury', 101, 7.99, 0, 0),
                ('Almond roca', 102, 8.99, 0, 0),
                ('Golden Key', 103, 3.99, 0, 0)]

            cursInsert = connection.cursor()
            cursInsert.bindarraysize = 3
            cursInsert.setinputsizes(32, int, float, int, int)
            cursInsert.executemany("INSERT INTO TOFFEES(T_NAME, SUP_ID, PRICE, SALES, TOTAL) " 
                               "VALUES (:1, :2, :3, :4, :5)", data)
            connection.commit()
              
            curs.execute("SELECT * from TOFFEES")
            rows = curs.fetchall()
            for row in rows:
            print(row)
                  
            '''
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            # I dont think we need a very detailed error message here? 
            #print( sys.stderr, "Oracle code:", error.code)
            #print( sys.stderr, "Oracle message:", error.message)
            print("Error:", error.message)
        
        else:
            login_err = False
    Menu(connection, curs)

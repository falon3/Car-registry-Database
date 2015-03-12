import sys
import cx_Oracle
from new_vehicle import NewVehicle       
# 1. from filename (without .py) import functionname
# OR 2. import filename
# in the first case you call with functionname
# in the second case you call with filename.functionname
# from filename import functionname as thisfunction

def Exit():

    connection.close()   
    print("GoodBye!")
    exit()
         
def Menu():

    print("1. New Vehicle Registration\n")
    print("2. Auto Transaction\n")
    print("3. Driver License Registration\n")
    print("4. Violation Record\n")
    print("5. Search Engine\n")
    print("6. Exit Auto Registration System\n")

    select = input("Select an option ")
    
    if select == '1':
        NewVehicle()
    
    elif select == '2':
        AutoTransaction()
	
    elif select == '3':
        DriverRegistration()
   
    elif select == '4':
        ViolationRecord()

    elif select == '5':
         RecordSearch()
    
    elif select == '6':
         Exit()

    else: 
        print("Error, invalid input.")

    Menu()

if __name__ == "__main__":

    ccid = input('Enter your CCID: ')
    password = input('Password: ')
   
    login = ccid + '/' + password + '@gwynne.cs.ualberta.ca:1521/CRS'

    try:
        connection = cx_Oracle.connect(login)
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
        print( sys.stderr, "Oracle code:", error.code)
        print( sys.stderr, "Oracle message:", error.message)

    # this makes everything auto commit so no worries of exiting before commiting new info
    connection.autocommit = 1

    Menu()

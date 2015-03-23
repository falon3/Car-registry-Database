import cx_Oracle
import datetime

"""
    Flow:
    (done) 1. Request sin. Check if sin exists in drive_licence
        If YES: Return failure "record already exists"
        If NO: Go to 2.
    (done) 2. Check if sin exists in people  
        If YES: Goto 3.
        If NO: Create new people record. 
               Information required: sin CHAR(15), name VARCHAR(40), 
                 height number(5,2), weight number(5,2), eyecolor VARCHAR(10),
                 haircolor VARCHAR(10), addr VARCHAR2(50), 
                 gender CHAR ('m' or 'f'), birthday DATE
        Note: We need to specify a format that they should obey for date.
    3. Create new driver record. 
       Information required: licence_no CHAR(15), class VARCHAR(10), 
         photo BLOB, issuing_date DATE, expiring_date DATE
       Also sin but we already have that.
       Note: photo to be entered as 'filename of photo'.
    4. Query for driving restrictions (r_id INTEGER).
        IF YES: Goto 5
        IF NO: Done, exit.
    5. Query for existence of r_id in restriction as c_id.
        IF EXISTS: Create new driving restriction entry, then goto 4.
        IF NO: Return error.
    6. Confirm input.
    
    Questions:
    1. If the restriction is wrong should we create the license at all?
         We can solve this by saving all the create record statements until
         the end and then queueing them all for entry. If failure is 
         encountered at any point then no records will be created.
         It's also debatable that we should always create new people records.
    2. Is it better to ask 'how many restrictions' and then loop?
       As opposed to constant prompting for restrictions?
       My rationale for the loop prompt is that I assume a single or maybe
       2 driving conditions in practice (only with corrective lenses, only
       under supervision). It also depends on how the conditions table is set
       up.
"""
def NewDriver(connection, curs):
    newRecUI()
    sin = requestSIN()
    if recordExists(sin,'drive_licence',connection,curs):
        print("Error: that driver already has a license!")
        print("Returning to main menu...")
    elif recordExists(sin, 'people', connection, curs):
        print("People record found; no driving license found")
    else:
        newPeopleUI(sin,connection,curs)
        
"""
newPeopleUI

Parameters: sin, connection, curs
Return value: none

Displays prompt and instructions for creating a new people record.
"""
def newPeopleUI(sin,connection,curs):
    print("New people record required.")
    fields = ('sin', 'name', 'height', 'weight', 'eyecolor', 'haircolor', 'addr', 'gender', 'birthday')
    descript = {}
    descript['sin'] = "SIN"
    descript['name'] = "Name"
    descript['height'] = "Height"
    descript['weight'] = "Weight"
    descript['eyecolor'] = "Eye color"
    descript['haircolor'] = "Hair color"
    descript['addr'] = "Address"
    descript['gender'] = "Gender"
    descript['birthday'] = "Birthday"
    
    indict = {}
    indict['sin'] = sin
    indict['name'] = requestName()
    indict['height'] = requestBodyStats('height')
    indict['weight'] = requestBodyStats('weight')
    indict['eyecolor'] = requestColor('eye')
    indict['haircolor'] = requestColor('hair')
    indict['addr'] = requestAddr()
    indict['gender'] = requestGender()
    indict['birthday'] = requestDate('birthday')

    print()
    print("You have entered the following information:")
    for x in fields:
        print(descript[x] + ':',indict[x])
    if verifyYN():
        stmt = "INSERT INTO PEOPLE " + str(fields).replace("'","") \
        + " VALUES " + str(fields).replace("'", "").replace("(","(:").replace(" "," :")
        curs.execute(stmt,indict)
        print("\nNew record has been created in people.")
    else:
        print("Returning to main menu...\n\n")
        # To do: maybe have a way for them to return to just creating a new person
        # but with option for editing the SIN.
        # newPeopleUI(sin,connection,curs)


"""
newRecUI

Parameters: none
Return value: none

Displays prompt and instructions for creating a new driving record.
"""
def newRecUI():
    # note that multistrings include the indent as part of the string.
    s = """
    -------------------------------
    New Driver License Registration
    -------------------------------
    You will be prompted for the following information: driver's SIN,
    licence number, class of license, filename of driver's photo,
    date of issue, date of expiry.
    If a record does not currently exist for the driver, you will be
    prompted to enter additional identifying information:
    name, height, weight, eye color, hair color, address, gender and
    birth date.
    All data entered will be truncated to the correct length.
    You will be asked for confirmation before the record is created.
    
    """
    print(s)

"""
verifyYN

Parameters: none
Return value: 1 if yes, 0 if no
"""

def verifyYN():

    ans = input("Is this correct? (y/n): ")
    while not (ans == 'y' or ans == 'n'):
        ans = input("Invalid input, please enter y or n: ")
    if ans == 'y':
        return 1
    if ans == 'n':
        return 0
    
"""
requestSIN

Parameters: none
Return value: String (not to exceed 15 chars) containing the SIN.
"""
def requestSIN():
    errinputs = """\
You entered an invalid SIN number. SIN numbers must be 9 digits long 
and devoid of external formatting, i.e. 123456789.
Please enter the new driver's SIN number again: """
    sin = input("Please enter the new driver's SIN number (9 digits): ")
    while not (sin.isdigit()):
        sin = input(errinputs)
    print("You have entered:", sin)
    if verifyYN():
        return sin[:15]
    else:
        return requestSIN()

"""
requestDate

Parameters: type (type of date requested)
Return value: date in format 
"""
def requestDate(type):
    query = "Please enter the driver's %s (DD-MMM-YY): " % type
    done = 0
    while not done:
        date = input(query)
        try:
            vdate = datetime.datetime.strptime(date, "%d-%b-%y")
        except:
            print("Incorrect date format.")
        else:
            done = 1
    return date.upper()
    
"""
requestGender

Parameters: none
Return value: 1-char string 'm' or 'f'
"""
def requestGender():
    errinputs = """\
You entered an invalid gender. Please enter only 'm' or 'f'.
Please enter the driver's gender again: """
    gender = input("Please enter the driver's gender (m or f) : ")
    while not (gender == 'm' or gender == 'f'):
        gender = input(errinputs)
    return gender[:1]
    
"""
requestAddr

Parameters: none
Return value: 
"""
   
def requestAddr():
    query = "Please enter the driver's address (max 50 char.): "
    addr = input(query)
    return addr[:50]
   
"""
requestBodyStats

Parameters: type (height or weight)
Return value: float that is formatted correctly for 5.2
"""
def requestBodyStats(type):
    query = "Please enter the driver's %s (to 2 d.p.): " % type
    inpt = input(query)
    return float('%5.2f'%float(inpt))
    
"""
requestColor

Parameters: type (eye or hair)
Return value: String containing color, max length 10 digits
"""    
def requestColor(type):
    query = "Please enter the driver's %s color (max 10 characters): " % type
    color = input(query)
    return color[:10]
    
"""
requestName

Parameters: none
Return value: String containing name, max length 40
"""
def requestName():
    query = "Please enter the driver's full name (max 40 characters): "
    name = input(query)
    return name[:40]    

    
"""
recordExists

Parameters: sin (string), table (string) connection, curs (for querying db)
Return value: 1 if sin exists, 0 if not.
Assumptions: sin is in valid format; is contained in first 9 characters of
             the string passed in.
             table is a valid table_name

Checks the given table to see if the SIN already exists.
"""
def recordExists(sin, table, connection, curs):
    # Notes: since sin is char 16, we need to pad out the remaining values
    sin = sin[:9] + '      '
    query = "SELECT SIN FROM %s WHERE SIN = :sinno" % table
    qdict = {'sinno':sin}
    curs.execute(query,qdict)
    row = curs.fetchone()
    if row == None:
        return 0
    return 1

    

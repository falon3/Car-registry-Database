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
    if not sin:
        print("No records were created. Returning to main menu... \n\n")
        return
    if recordExists(sin,'drive_licence',connection,curs):
        print("Error: that driver already has a license!")
        print("Returning to main menu...")
    elif recordExists(sin, 'people', connection, curs):
        print("People record found; no driving license found")
        newDriverUI(sin,connection,curs)
    else:
        rval = newPeopleUI(sin,connection,curs)
        if not rval:
            print("No records were created. Returning to main menu... \n\n")
            return
        rval = newDriverUI(sin,connection,curs)
        if not rval:
            print("No records were created. Returning to main menu... \n\n")
            return
            
"""
newPeopleUI

Parameters: sin, connection, curs
Return value: 1 if new record successfully created, 0 else.
Assummptions: SIN entered at this point is correct.

Displays prompt and instructions for creating a new people record.
"""
def newPeopleUI(sin,connection,curs):
    print("New people record required.")
    print("Please enter the required information (leave blank and enter to quit).")
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
    if not indict['name']:
        return 0
    indict['height'] = requestBodyStats('height')
    if not indict['height']:
        return 0
    indict['weight'] = requestBodyStats('weight')
    if not indict['weight']:
        return 0
    indict['eyecolor'] = requestCharT('eye color')
    if not indict['eyecolor']:
        return 0
    indict['haircolor'] = requestCharT('hair color')
    if not indict['haircolor']:
        return 0
    indict['addr'] = requestAddr()
    if not indict['addr']:
        return 0
    indict['gender'] = requestGender()
    if not indict['gender']:
        return 0
    indict['birthday'] = requestDate('birthday')
    if not indict['birthday']:
        return 0

    print()
    print("You have entered the following information:")
    for x in fields:
        print(descript[x] + ':',indict[x])
    flag = verifyYN()
    if flag == 1:
        stmt = "INSERT INTO PEOPLE " + str(fields).replace("'","") \
        + " VALUES " + str(fields).replace("'", "").replace("(","(:").replace(", ",", :")
        curs.execute(stmt,indict)
        print("\nNew record has been created in people.\n\n")
        return 1
    elif flag == -1:
        return newPeopleUI(sin,connection,curs)
    # we should never reach this point
    return 0

"""
newDriverUI

Parameters: sin, connection, curs
Return value: 1 if new record successfully created, 0 else.
Assummptions: SIN entered at this point is correct. People record exists. 
              Driving licence number is determined outside of program.

Displays prompt and instructions for creating a new driving licence record.
"""
def newDriverUI(sin,connection,curs):
    print("Now creating new driving licence record.")
    print("Please enter the required information (leave blank and enter to quit).")
    fields = ('licence_no','sin','class','photo','issuing_date','expiring_date')
    descript = {}
    descript['licence_no'] = "Licence number"
    descript['sin'] = "SIN"
    descript['class'] = "Class"
    descript['photo'] = "Filename of photo"
    descript['issuing_date'] = "Date of issue"
    descript['expiring_date'] = "Date of expiry"
    
    indict = {}
    indict['licence_no'] = requestLicence(connection, curs)
    if not indict['licence_no']:
        return 0
    indict['sin'] = sin
    indict['class'] = requestCharT('licence class')
    if not indict['class']:
        return 0
    p = requestPhoto()
    indict['photo'] = p[0]
    if not p[1]:
        return 0
    indict['issuing_date'] = requestDate('licence date of issue')
    if not indict['issuing_date']:
        return 0
    indict['expiring_date'] = requestDate('licence date of expiry')
    if not indict['expiring_date']:
        return 0

    print()
    print("You have entered the following information:")
    for x in fields:
        if not ( x == 'photo'):
            print(descript[x] + ':',indict[x])
        else:
            print(descript[x] + ':', p[1])
    flag = verifyYN()
    if flag == 1:
        curs.setinputsizes(photo=cx_Oracle.BLOB)
        stmt = "INSERT INTO DRIVE_LICENCE " + str(fields).replace("'","") \
        + " VALUES " + str(fields).replace("'", "").replace("(","(:").replace(", ",", :")
        curs.execute(stmt,indict)
        print("\nNew record has been created in drive_licence.\n\n")
        errval = createRestrictions(indict['licence_no'], connection, curs)
        return errval
    elif flag == -1:
        return newDriverUI(sin,connection,curs)
    # we should never reach this point
    return 0

"""
createRestrictions

Parameters: licence_no, connection, curs
Returns: 1 if successful, 0 if not.

Assumes: 'q' is not a restriction. No restrictions currently exists for the driver licence.
"""

def createRestrictions(licence_no, connection, curs):
    done = 0
    added = []
    fields = ('licence_no', 'r_id')
    indict = {}
    indict['licence_no'] = licence_no
    while not done:
        r_no = input("Please enter the driving condition ID number ('q' when done): ")
        if not r_no.isdigit():
            if r_no == 'q':
                print("Finished creating record.\n\n")
                done = 1
            else:
                print("Invalid ID number: must be a digit.")
        elif r_no in added:
            print("You have already added that restriction.")
        else:
            if verifyRestrictions(r_no, connection, curs):
                added += [r_no]
                indict['r_id'] = r_no
                stmt = "INSERT INTO restriction " + str(fields).replace("'","") \
            + " VALUES " + str(fields).replace("'", "").replace("(","(:").replace(", ",", :")
                curs.execute(stmt,indict)
                print("Driving condition added.")
            else:
                print("Invalid driving condition ID number.")
    return 1

"""
verifyRestrictions
Parameters: r_no, connection, curs
Returns: 1 if verified, 0 if not
"""
def verifyRestrictions(r_no, connection, curs):
    query = "SELECT c_id FROM driving_condition WHERE c_id = :restrict"
    qdict = {'restrict':r_no}
    curs.execute(query,qdict)
    row = curs.fetchone()
    if row == None:
        return 0
    return 1    
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
    To exit the process at any point, press enter without entering a 
    value.
    You will be asked for confirmation before the record is created.
    
    """
    print(s)

"""
verifyYN

Parameters: none
Return value: 1 if yes, 0 if no
"""

def verifyYN():

    ans = input("Is this correct? (y/n/q): ")
    while not (ans == 'y' or ans == 'n' or ans == 'q'):
        ans = input("Invalid input, please enter y or n or q: ")
    if ans == 'y':
        return 1
    if ans == 'n':
        return -1
    if ans == 'q':
        return 0
"""
requestPhoto

Parameters: none
Return value: the read photo file in [1], the filename in [2]
"""

def requestPhoto():
    errinputs="You entered an invalid file name. Please try again."
    done = 0
    while not done:
        photoname = input("Please enter the filename of the driver's photo: ")
        if photoname:
            try:
                photofile = open(photoname, 'rb')
            except:
                print(errinputs)
            else:
                done = 1
        else:
            return 0, 0
        photo = photofile.read()
    return photo,photoname

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
    while not (sin.isdigit() or sin == ''):
        sin = input(errinputs)
    if sin == '':
        return 0
    print("You have entered:", sin)
    flag = verifyYN()
    if flag == 1:
        return sin[:15]
    elif flag == -1:
        return requestSIN()
    return 0

"""
requestLicence

Parameters: connection, curs
Return value: String (not to exceed 15 chars) containing the licence number

Potential error cases:
1. licence number already exists (and is tied to another SIN number)
We don't have to cover the case of both sin and licence existing because we 
checked that earlier.
"""
        
def requestLicence(connection, curs):
    errinputs = """\
You entered an invalid licence number. Licence numbers must be 9 digits long 
and devoid of external formatting, i.e. 123456789.
Please enter the new driver's SIN number again: """
    existserr = """\
The licence number you have entered already exists. Licence numbers
must be 9 digits long and devoid of external formatting, i.e. 123456789."""
    licence = input("Please enter the new driver's licence number (9 digits): ")
    while not (licence.isdigit() or licence==''):
        licence = input(errinputs)
    if licence == '':
        return 0
    print("You have entered:", licence)
    # changed from == to =
    flag = verifyYN()
    if flag == 1:
        if licenceExists(licence, 'drive_licence', connection, curs):
            print(existserr)
            return requestLicence(connection,curs)
        return licence
    elif flag == -1:
        return requestLicence(connection,curs)    
    return 0

        
"""
requestDate

Parameters: type (type of date requested)
Return value: date in format 
"""
def requestDate(type):
    query = "Please enter the driver's %s (YY-MM-DD): " % type
    done = 0
    while not done:
        vdate = input(query)
        if vdate == '':
            return 0
        try:
            vdate = datetime.datetime.strptime(vdate, "%y-%m-%d")
        except:
            print("Incorrect date format.")
        else:
            done = 1
    return vdate.date()
    
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
    while not (gender == 'm' or gender == 'f' or gender == ''):
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
    done = 0
    while not done:
        done = 1
        query = "Please enter the driver's %s (to 2 d.p.): " % type
        inpt = input(query)
        if inpt == '':
            return 0
        try:
            float(inpt)
        except:
            print("Input should be a number. ")
            done = 0
    return float('%5.2f'%float(inpt))
    
"""
requestCharT

Parameters: type (eye color or hair color or class)
Return value: String containing color, max length 10 digits
"""    
def requestCharT(type):
    query = "Please enter the driver's %s (max 10 characters): " % type
    val = input(query)
    return val[:10]
    
"""
requestName

Parameters: none
Return value: String containing name, max length 40
"""
def requestName():
    query = "Please enter the driver's full name (max 40 characters): "
    name = input(query)
    return name[:40]    

# At some point of time, can maybe combine recordExists and licenceExists into the same function
    
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
    # Notes: since sin is char 15, we need to pad out the remaining values
    sin = sin + (15-len(sin)) * ' '
    query = "SELECT SIN FROM %s WHERE SIN = :sinno" % table
    qdict = {'sinno':sin}
    curs.execute(query,qdict)
    row = curs.fetchone()
    if row == None:
        return 0
    return 1

"""
licenceExists

Parameters: licence (string), table (string) connection, curs (for querying db)
Return value: 1 if licence exists, 0 if not.
Assumptions: licence is in valid format; is contained in first 9 characters of
             the string passed in.
             table is a valid table_name

Checks the given table to see if the licence number already exists.
"""
def licenceExists(licence, table, connection, curs):
    # Notes: since sin is char 16, we need to pad out the remaining values
    licence = licence[:9] + '      '
    query = "SELECT LICENCE_NO FROM %s WHERE LICENCE_NO = :lno" % table
    qdict = {'lno':licence}
    curs.execute(query,qdict)
    row = curs.fetchone()
    if row == None:
        return 0
    return 1
    

def NewDriver(connection, curs):
    """
    stuff here. maybe not tonight.
    okay maybe tonight. 
    we may perhaps also want to create a people record if it does not exist.
    Contents of this comment should be moved to the documentation.
    
    Flow:
    1. Request sin. Check if sin exists in drive_licence
        If YES: Return failure "record already exists"
        If NO: Go to 2.
    2. Check if sin exists in people  
        If YES: Goto 3.
        If NO: Create new people record. 
               Information required: sin CHAR(15), name VARCHAR(40), 
                 height number(5,2), weight number(5,2), eyecolor VARCHAR(10),
                 haircolor VARCHAR(10), addr VARCHAR2(50), 
                 gender CHAR ('m' or 'f'), birthday DATE
        Note: We need to specify a format that they should obey for date.
        Check later: autoconversion to 5,2 format for height/weight.
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
    newRecUI()
    sin = requestSIN()
    if recordExists(sin):
        pass
        
"""
newRecUI

Parameters: none
Return value: none

Displays prompt and instructions for creating a new driving record.
"""
def newRecUI():
    pass

"""
requestSIN

Parameters: none
Return value: String (not to exceed 15 chars) containing the SIN.

Request user input SIN number, checks for compliance with format.
Prompts for re-entry else; prompts for confirmation.
"""
def requestSIN():
    return ""

"""
recordExists

Parameters: sin (string), connection, curs (for querying db)
Return value: TRUE if sin exists, FALSE if not.
Assumptions: sin is valid format

Checks the people table to see if the SIN already exists.
"""
def recordExists(sin, connection, curs):
    return FALSE
    

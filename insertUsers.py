###################################################################
#                                                                 #
#   This will insert user names and slack IDs into a database     #
#                                                                 #
###################################################################

def addToDB(someFile, someCursor, connection):
    fileOBJ = open(someFile,"r")
    i = 0
    for line in fileOBJ.readlines():
        UserName, SlackID = line.split("|")
        UserName = UserName.title()
        SlackID = SlackID.upper()

        SlackID = SlackID.rstrip()
        UserName = UserName.rstrip()

        someCursor.execute(("""
            INSERT INTO
                User ('SlackID', 'UserName')
            VALUES
                ('{0}', '{1}');
        """).format(SlackID, UserName))
        i += 1
        print("inserting record {}!".format(i))

    print("Insert complete")
    connection.commit()
    return
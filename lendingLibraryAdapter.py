import databaseProvider as sql
import sqlite3

DATABASE = "lendingLibrary.db"
sql.MAIN_CONNECTION = sqlite3.connect(DATABASE) # set DB connection

####################################
"""
Tony Strickland and I both need to be admins
List all items - show available, or not
list what's there
list what's not - who's got it
allow a checkout/checkin
add/remove items from the library
categories, types, genres, owner

ID, Name, Genre, Owner, SlackName, LastCheckIn, Checkedout, ByWhom, WhenCheckedOut, NumberOfTimesCheckedOut

"""

ADMINS = {

    "UC1LT08SX" : "Tony Strickland",
    "UC176R92M" : "Andre Gueret",
    "UC1Q3DVL2" : "Daniel Hodge"

}

def isAdmin(someID):
    if someID in ADMINS:
        return True
    return False

#######################
###   Users Table   ###
#######################

# CREATE TABLE `Users` (
# `ID`INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
# `slackID`TEXT NOT NULL DEFAULT 'Slack ID Not Set' UNIQUE,
# `realName`TEXT NOT NULL DEFAULT 'Slack Name Not Set'
# );


########################
###   Animal Table   ###
########################

# CREATE TABLE `Animal` (
# 	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
# 	`Name`	TEXT,
# 	`Type`	INTEGER
# );

def selectAllAnimals():
    return sql.SELECT_ALL("Animal")

def insertManyAnimals(aList):
    columns = "Name", "Type"
    fullList = columns + aList
    return sql.VARIABLE_INSERT("Animal", 2, fullList)

def updateSimpleAnimals(updateColumn, updateValue, whereColumn, whereCondition):
    return sql.SIMPLE_UPDATE("Animal", updateColumn, updateValue, whereColumn, whereCondition)
    
def deleteSimpleAnimals(whereColumn, whereCondition):
    return sql.SIMPLE_DELETE("Animal", whereColumn, whereCondition)
    
def testAnimal():
    cmd = """
        INSERT INTO 
            Animal (Name, Type)
        VALUES
            ('Cat', 3);
    """
    return sql.EXEC(cmd)
import databaseProvider as sql
import sqlite3

DATABASE = "data/lendingLibrary.db"
# DATABASE = "lenderBot/data/lendingLibrary.db" # Prod path
sql.MAIN_CONNECTION = sqlite3.connect(DATABASE) # set DB connection

####################################

# Tony Strickland and I both need to be admins
# List all items - show available, or not
# list what's there
# list what's not - who's got it
# allow a checkout/checkin
# add/remove items from the library
# categories, types, genres, owner
# Video games, card games, etc

####################################

#######################
###   Users Table   ###
#######################

# CREATE TABLE `Users` (
# `ID`INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
# `slackID`TEXT NOT NULL DEFAULT 'Slack ID Not Set' UNIQUE,
# `realName`TEXT NOT NULL DEFAULT 'Slack Name Not Set'
# , IsAdmin BIT
# );

def isAdmin(slackID):
    result = """
    SELECT
        IsAdmin
    FROM
        Users
    WHERE
        SlackId = '{0}'
    """.format(slackID)
    return sql.GET(result)

###########################
###   MediaType Table   ###
###########################

# CREATE TABLE MediaType (
# ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
# Description TEXT NOT NULL
# );

# Video games, board games, cards, etc

def insert_MediaType(newType):
    return sql.SIMPLE_INSERT("MediaType", "Description", newType)

###############################
###   MediaCategory Table   ###
###############################

# CREATE TABLE MediaCategory (
# ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
# Name TEXT NOT NULL
# );

# family, Comedy, Horror, etc.

def insert_MediaCategory(newCategory):
    return sql.SIMPLE_INSERT("MediaCategory", "Name", newCategory)

#######################
###   Media Table   ###
#######################

# CREATE TABLE Media (
# ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
# MediaType INTEGER NOT NULL DEFAULT 1, 
# MediaCategory INTEGER NOT NULL DEFAULT 1, 
# OwnerID TEXT NOT NULL, FullName TEXT NOT NULL, 
# LongGame BIT NOT NULL DEFAULT 1, 

# FOREIGN KEY (MediaType) REFERENCES MediaType(ID), 
# FOREIGN KEY (MediaCategory) REFERENCES MediaCategory(ID), 
# FOREIGN KEY (OwnerID) REFERENCES Users(SlackID)
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
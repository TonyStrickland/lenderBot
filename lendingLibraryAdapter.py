import databaseProvider as sql
import sqlite3
import datetime

DATABASE = "data/lendingLibrary.db"
# DATABASE = "lenderBot/data/lendingLibrary.db" # prod location
sql.MAIN_CONNECTION = sqlite3.connect(DATABASE) # set DB connection

##################################################

# Tony Strickland and I both need to be admins
# List all items - show available, or not
# list what's there - DONE
# list what's not - who's got it
# allow a checkout/checkin
# add/remove items from the library - DONE
# categories, types, genres, owner - DONE
# Video games, card games, etc - DONE

##################################################

#######################
###   Users Table   ###
#######################

# CREATE TABLE `Users` (
# 	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
# 	`userName`	TEXT NOT NULL,
# 	`slackID`	TEXT NOT NULL UNIQUE,
# 	`directID`	TEXT NOT NULL,
# 	`IsAdmin`	BIT NOT NULL DEFAULT 0
# );

def isAdmin(slackID):
    result = """
    SELECT
        IsAdmin
    FROM
        Users
    WHERE
        slackID = '{0}';
    """.format(slackID)
    
    try:
        fin = sql.GET(result)[0][0]
    except:
        fin = 0

    return fin

def isDirect(channelID):
    result = """
    SELECT
        *
    FROM
        Users
    WHERE
        directID = '{0}';
    """.format(channelID)

    try:
        fin = sql.GET(result)[0][0]
    except:
        fin = 0

    return fin

def getSlackID(name):
    cmd = """
        SELECT 
            slackID
        FROM 
            Users 
        WHERE 
            userName LIKE '{0}'
    """.format(name)

    try:
        fin = sql.GET(cmd)[0][0]
    except:
        fin = 'No ID'

    return fin

#######################
###   Facts Table   ###
#######################

# CREATE TABLE `Facts` (
# `ID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
# `Line` TEXT NOT NULL UNIQUE 
# );

def insert_Fact(newType):
    return sql.SIMPLE_INSERT("Facts", "Line", "'{}'".format(newType))

def selectAll_Facts():
    return sql.SELECT_ALL("Facts")

def remove_Facts(ID):
    return sql.SIMPLE_DELETE("Facts", "ID", ID)

def getFactByID(ID):
    result = """
    SELECT
        Line
    FROM
        Facts
    WHERE
        ID = {0};
    """.format(ID)

    try:
        fin = sql.GET(result)[0][0]
    except:
        fin = 0

    return fin

#########################
###   Insults Table   ###
#########################

# CREATE TABLE `Insults` (
# `ID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
# `Line` TEXT NOT NULL UNIQUE 
# );

def insert_Insult(newType):
    return sql.SIMPLE_INSERT("Insults", "Line", "'{}'".format(newType))

def selectAll_Insults():
    return sql.SELECT_ALL("Insults")

def remove_Insults(ID):
    return sql.SIMPLE_DELETE("Insults", "ID", ID)

def getInsultByID(ID):
    result = """
    SELECT
        Line
    FROM
        Insults
    WHERE
        ID = {0};
    """.format(ID)

    try:
        fin = sql.GET(result)[0][0]
    except:
        fin = 0

    return fin

###########################
###   MediaType Table   ###
###########################

# CREATE TABLE MediaType (
# ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
# Description TEXT NOT NULL UNIQUE
# );

# Video games, board games, cards, etc

def insert_MediaType(newType):
    return sql.SIMPLE_INSERT("MediaType", "Description", "'{}'".format(newType))

def remove_MediaType(ID):
    return sql.SIMPLE_DELETE("MediaType", "ID", ID)

def update_MediaType(ID, desc):
    return sql.SIMPLE_UPDATE("MediaType", "Description", "'{}'".format(desc), "ID", ID)

def selectAll_MediaType():
    return sql.SELECT_ALL("MediaType")

def get_MediaTypeID(mediaType):
    cmd = """
    SELECT
        ID
    FROM
        MediaType
    WHERE
        Description LIKE '{}';
    """.format(mediaType)
    
    try:
        result = sql.GET(cmd)[0][0]
    except:
        result = 1 # defaults to 1, undefined

    return result

###############################
###   MediaCategory Table   ###
###############################

# CREATE TABLE MediaCategory (
# ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
# Name TEXT NOT NULL UNIQUE
# );

# family, Comedy, Horror, etc.

def insert_MediaCategory(newCategory):
    return sql.SIMPLE_INSERT("MediaCategory", "Name", "'{}'".format(newCategory))

def remove_MediaCategory(ID):
    return sql.SIMPLE_DELETE("MediaCategory", "ID", ID)
    
def update_MediaCategory(ID, desc):
    return sql.SIMPLE_UPDATE("MediaCategory", "Name", "'{}'".format(desc), "ID", ID)

def selectAll_MediaCategory():
    return sql.SELECT_ALL("MediaCategory")

def get_MediaCategoryID(mediaType):
    cmd = """
    SELECT
        ID
    FROM
        MediaCategory
    WHERE
        Name LIKE '{}';
    """.format(mediaType)

    try:
        result = sql.GET(cmd)[0][0]
    except:
        result = 1 # defaults to 1, undefined

    return result

#######################
###   Media Table   ###
#######################

# CREATE TABLE Media (
# ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
# MediaType INTEGER NOT NULL DEFAULT 1, 
# MediaCategory INTEGER NOT NULL DEFAULT 1, 
# OwnerID TEXT NOT NULL, 
# FullName TEXT NOT NULL, 
# LongGame BIT NOT NULL DEFAULT 1, 

# FOREIGN KEY (MediaType) REFERENCES MediaType(ID), 
# FOREIGN KEY (MediaCategory) REFERENCES MediaCategory(ID), 
# FOREIGN KEY (OwnerID) REFERENCES Users(SlackID)
# );

def insert_Media(mediaInfo):
    return sql.SIMPLE_INSERT("Media", "MediaType, MediaCategory, OwnerID, FullName, LongGame", mediaInfo)

def remove_Media(ID):
    return sql.SIMPLE_DELETE("Media", "ID", ID)

def select_MediaID(ID):
    return sql.SIMPLE_SELECT("Media", "ID", ID)

def selectAll_Media():
    return sql.SELECT_ALL("Media")

def getMediaNameByID(ID):
    result = """
    SELECT
        FullName
    FROM
        Media
    WHERE
        ID = {0};
    """.format(ID)

    try:
        fin = sql.GET(result)[0][0]
    except:
        fin = 0

    return fin

def format_Media(): # TODO add isCheckedOut to this
    cmd = """
    SELECT 
    m.ID
    , m.FullName
    , mc.Name
    , mt.Description
    , CASE m.LongGame 
        WHEN 1
            THEN 'Long'
            ELSE 'Short'
        END as Length
    FROM Media as m
    JOIN 
    MediaCategory as mc 
        ON m.MediaCategory = mc.ID
    , MediaType as mt 
	    ON m.MediaType = mt.ID;
    """

    return sql.GET(cmd)

##############################
###   Transactions Table   ###
##############################

# CREATE TABLE Transactions (
# 'ID' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
# 'MediaID' INTEGER NOT NULL, 
# 'SlackID' TEXT NOT NULL, 
# 'CheckIN' DATE, 
# 'CheckOUT' DATE, 

# FOREIGN KEY (MediaID) REFERENCES Media(ID), 
# FOREIGN KEY (SlackID) REFERENCES Users(SlackID) 
# );

def tooManyOut(slackID):
    cmd = """
    SELECT COUNT(0) as numberOut
    FROM Transactions as t
    WHERE 
        t.SlackID = '{0}'
        AND t.CheckIN is null;
    """.format(slackID)

    numOut = sql.GET(cmd)[0][0]
    
    if numOut >= 2: # if they have 2 or more items out, they'll need to talk to an admin
        return True
        
    return False

def isItemCheckedOut(mediaID):
    cmd = """
    SELECT COUNT(0) as numberOut
    FROM Transactions as t
    WHERE 
        t.MediaID = '{0}'
        AND t.CheckIN is null;
    """.format(mediaID)

    numOut = sql.GET(cmd)[0][0]
    
    if numOut >= 1: # can't check ou an item twice... I hope
        return True
        
    return False

def CheckIN(mediaID):
    if isItemCheckedOut(mediaID): # if this doesn't work, you'll need an admin
        return 7

    cmd = """
    UPDATE 
    Transactions
    SET
    CheckIN = datetime('now','localtime')
    WHERE
    MediaID = {0}
    AND CheckIN is null;
    """.format(mediaID)

    return sql.EXEC(cmd)

def CheckOUT(mediaID, slackID):
    if isItemCheckedOut(mediaID): # can't check out something twice
        return 5

    if tooManyOut(slackID): # can only check out a cuople of items
        return 4

    cmd = """
    INSERT INTO 
    Transactions
    (MediaID, SlackID, CheckOUT)
    VALUES
    ({0},'{1}', datetime('now','localtime'));
    """.format(mediaID, slackID)

    return sql.EXEC(cmd)

def adminCheckIN(mediaID):
    cmd = """
    UPDATE 
    Transactions
    SET
    CheckIN = datetime('now','localtime')
    WHERE
    MediaID = {0}
    AND CheckIN is null;
    """.format(mediaID)

    return sql.EXEC(cmd)

def adminCheckOUT(mediaID, slackID):
    if isItemCheckedOut(mediaID): # can't check out something twice
        return 5

    cmd = """
    INSERT INTO 
    Transactions
    (MediaID, SlackID, CheckIN)
    VALUES
    ({0},'{1}', datetime('now','localtime'));
    """.format(mediaID, slackID)

    return sql.EXEC(cmd)
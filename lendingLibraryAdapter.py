import databaseProvider as sql
import sqlite3

DATABASE = "data/lendingLibrary.db"
# DATABASE = "lenderBot/data/lendingLibrary.db" # prod location
sql.MAIN_CONNECTION = sqlite3.connect(DATABASE) # set DB connection

##################################################

# Tony Strickland and I both need to be admins
# List all items - show available, or not
# list what's there
# list what's not - who's got it
# allow a checkout/checkin
# add/remove items from the library
# categories, types, genres, owner
# Video games, card games, etc

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

def format_Media():
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
        END as  Length
    FROM Media as m
    JOIN 
    MediaCategory as mc 
        ON m.MediaCategory = mc.ID
    , MediaType as mt 
	ON m.MediaType = mt.ID;"""

    return sql.GET(cmd)
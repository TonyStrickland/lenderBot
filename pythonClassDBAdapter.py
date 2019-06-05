import databaseProvider as sql
import sqlite3

DATABASE = "pythonClass.db"
sql.MAIN_CONNECTION = sqlite3.connect(DATABASE) # set DB connection

########################
###   Table Schema   ###
########################

# CREATE TABLE MyTable (
#   ID INTEGER PRIMARY KEY AUTOINCREMENT, 
#   testC1 TEXT, 
#   testx3 BLOB
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

###########################
###   Vegetable Table   ###
###########################

# CREATE TABLE `Vegetable` (
# 	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
# 	`Name`	TEXT,
# 	`Type`	INTEGER
# );

def selectAllVegetables():
    return sql.SELECT_ALL("Vegetable")

def insertManyVegetables(aList):
    columns = "Name", "Type"
    fullList = columns + aList
    return sql.VARIABLE_INSERT("Vegetable", 2, fullList)
    

def updateSimpleVegetables(updateColumn, updateValue, whereColumn, whereCondition):
    return sql.SIMPLE_UPDATE("Vegetable", updateColumn, updateValue, whereColumn, whereCondition)
    

def deleteSimpleVegetables(whereColumn, whereCondition):
    return sql.SIMPLE_DELETE("Vegetable", whereColumn, whereCondition)

def createAnimaltable(tableName):
    cmd = ""
    sql.EXEC(cmd)
#########################
###   Mineral Table   ###
#########################

# CREATE TABLE `Mineral` (
# 	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
# 	`Name`	TEXT,
# 	`Type`	INTEGER,
# 	`Composition`	TEXT
# );

def selectAllMinerals():
    return sql.SELECT_ALL("Mineral")

def insertManyMinerals(aList):
    columns = "Name", "Type", "Composition"
    fullList = columns + aList
    return sql.VARIABLE_INSERT("Mineral", 3, fullList)
    
def updateSimpleMinerals(updateColumn, updateValue, whereColumn, whereCondition):
    return sql.SIMPLE_UPDATE("Mineral", updateColumn, updateValue, whereColumn, whereCondition)

def deleteSimpleMinerals(whereColumn, whereCondition):
    return sql.SIMPLE_DELETE("Mineral", whereColumn, whereCondition)
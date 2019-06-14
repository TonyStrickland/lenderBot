import lendingLibraryAdapter as adapter
import sys

def longGame(word):
	if word.lower() == "long":
		return 1
	return 0

def addToDB(someFile):
    try:
        fileOBJ = open(someFile,"r")
    except:
        print("no")
        sys.exit()

    i = 0
    err = 0
    errList = []
    for line in fileOBJ.readlines():
        try:
            MediaType, MediaCategory, Owner, LongGame, FullName = line.split(",", 4)

            theMediaType = adapter.get_MediaTypeID(MediaType)
            theMediaCategory = adapter.get_MediaCategoryID(MediaCategory)
            slackID = adapter.getSlackID(Owner).upper()
            isLong = longGame(LongGame)
            theFullName = FullName.strip('\n')

            insertString = "{}, {}, '{}', '{}', {}".format(theMediaType, theMediaCategory, slackID, theFullName, isLong)

            result = adapter.insert_Media(insertString)
            if result:
                print("Error inserting: {}".format(insertString))
                sys.exit()
            print("Inserting: {}".format(insertString))

        except:
            err += 1
            errList.append(insertString)
        
    print("Insert complete. With errors: {}".format(err))
    print(errList)
    return

addToDB("library.csv")
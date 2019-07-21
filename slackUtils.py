
def parseSlackInput(aText):
	if aText and len(aText) > 0:
		item = aText[0] # gets first (only) item
		if 'text' in item:
			msg = item['text'].strip(' ') # text of the message
			chn = item['channel'] # ID of the channel
			usr = item['user'] # ID of the user
			stp = item['ts'] # Timestamp at which message was posted
			return [str(msg),str(chn),str(usr),str(stp)]
		else:
			return [None,None,None,None]

def inChannelResponse(client, channel, response):
	client.chat_postMessage(
		channel=channel,
		text=response,
		as_user=True
    )
	
def threadedResponse(client, channel, response, stamp):
	client.chat_postMessage(
		channel=channel,
		text=response,
		thread_ts=stamp,
		as_user=True
	)

def directResponse(client, channel, someUser, text):
	client.chat_postMessage(
		channel=someUser,
		text=text,
		as_user=True
    )

############################
###   Parsing commands   ###
############################

def longGame(word):
	if word.lower() == "long":
		return 1
	return 0

def checkReturn(someInt):
	try:
		if someInt < 0:
			return 1
	except:
		return 1
	return someInt

def parseInsult_select(mediaInfo):
	try:
		result = "This is how I speak to those who are unworthy.\n\n"
		for i in mediaInfo:
			for x, y in enumerate(i):
				if x == 0:
					result += "{}\t".format(y)
				if x == 1:
					result += "{}\n".format(y)

	except: # if there aren't enough parts
		return False # returns false
	return result

def parseFact_select(mediaInfo):
	try:
		result = "Let me tell you of my many feats!\n\n"
		for i in mediaInfo:
			for x, y in enumerate(i):
				if x == 0:
					result += "{}\t".format(y)
				if x == 1:
					result += "{}\n".format(y)

	except: # if there aren't enough parts
		return False # returns false
	return result

def sanitizeID(slackID):
	return slackID.replace('<','').replace('>','').replace('@','').upper()

def reconstitueID(slackID):
	return "<@{}>".format(slackID)

def parseMedia_insert(mediaInfo):
	try:
		stripper = [x.strip() for x in mediaInfo.split(',', 4)]

		theMediaType = adapter.get_MediaTypeID(stripper[0])
		theMediaCategory = adapter.get_MediaCategoryID(stripper[1])
		theUser = sanitizeID(stripper[2])
		isLong = longGame(stripper[3])
		theFullName = stripper[4]

		insertString = "{}, {}, '{}', '{}', {}".format(theMediaType, theMediaCategory, theUser, theFullName, isLong)

	except: # if there aren't enough parts
		return False # returns false
	return insertString, theFullName

def parseMedia_select(mediaInfo):
	try:
		result = "Allow me to show you the hoard!\n\n"
		for item in mediaInfo:
			theID = item[0]
			theTitle = item[1]
			theCategory = item [2]
			theType = item [3]
			theLength = item[4]
			isThere = item[5]

			formatted = """{}: Title: "{}"\tCategory: {}\tMedium: {}\tLength: {} - {}""".format(theID, theTitle, theCategory, theType, theLength, isThere)
			result += formatted + "\n"
	except: # if there aren't enough parts
		return False # returns false
	return result

def parseMedia_WhosGotIt(mediaInfo):
	try:
		result = "I'll tell you who took it!\n\n"
		for item in mediaInfo:
			theID = item[0]
			theTitle = item[1]
			theUser = reconstitueID(item[2])
			theTime = item[3]

			formatted = """ID {}: Title: "{}"\tUser: {}\tTime: {}""".format(theID, theTitle, theUser, theTime)
			result += formatted + "\n"
	except: # if there aren't enough parts
		return False # returns false
	return result

def parseMediaType_select(mediaInfo):
	try:
		result = "I will show you my many types of media.\n\n"
		for i in mediaInfo:
			for x, y in enumerate(i):
				if x == 0:
					result += "{}\t".format(y)
				if x == 1:
					result += "{}\n".format(y)

	except: # if there aren't enough parts
		return False # returns false
	return result

def parseMediaType_update(mediaInfo):
	try:
		stripper = [x.strip() for x in mediaInfo.split(',', 1)]
		mediaID = stripper[0]
		newCategoryName = stripper[1].title()
		newCategoryID = adapter.get_MediaTypeID(newCategoryName)

	except: # if there aren't enough parts
		return False # returns false
	return mediaID, newCategoryID

def parseMediaCategory_select(mediaInfo):
	try:
		result = "I will show you my many categories of media!\n\n"
		for i in mediaInfo:
			for x, y in enumerate(i):
				if x == 0:
					result += "{}\t".format(y)
				if x == 1:
					result += "{}\n".format(y)

	except: # if there aren't enough parts
		return False # returns false
	return result

def parseMediaCategory_update(mediaInfo):
	try:
		stripper = [x.strip() for x in mediaInfo.split(',', 1)]
		mediaID = stripper[0]
		newCategoryName = stripper[1].title()
		newCategoryID = adapter.get_MediaCategoryID(newCategoryName)

	except: # if there aren't enough parts
		return False # returns false
	return mediaID, newCategoryID

def parseAdminCheckout(mediaInfo):
	try:
		stripper = [x.strip() for x in mediaInfo.split(',', 1)]
		mediaID = stripper[0]
		slackID = stripper[1]

	except: # if there aren't enough parts
		return False # returns false
	return mediaID, slackID

def parseViewMediaByCategory(mediaInfo):
	try:
		result = ""
		for i in mediaInfo:
			for x, y in enumerate(i):
				if x == 0:
					result += "ID {}:\t".format(y)
				if x == 1:
					result += """Title: "{}"\t""".format(y)
				if x == 2:
					result += """Category: "{}"\t""".format(y)
				if x == 3:
					result += """Medium: "{}" - """.format(y)
				if x == 4:
					result += "{}\n".format(y)
					
	except: # if there aren't enough parts
		return False # returns false
	return result

def parseViewMediaByType(mediaInfo):
	try:
		result = ""
		for i in mediaInfo:
			for x, y in enumerate(i):
				if x == 0:
					result += "ID {}:\t".format(y)
				if x == 1:
					result += """Title: "{}"\t""".format(y)
				if x == 2:
					result += """Category: "{}"\t""".format(y)
				if x == 3:
					result += """Medium: "{}" - """.format(y)
				if x == 4:
					result += "{}\n".format(y)
					
	except: # if there aren't enough parts
		return False # returns false
	return result

def parseMyStuff(mediaInfo):
	try:
		result = "Here is my treasure that you're holding!\n\n"
		for i in mediaInfo:
			for x, y in enumerate(i):
				if x == 0:
					result += "ID {}:\t".format(y)
				if x == 1:
					result += """Title: "{}"\t""".format(y)
				if x == 2:
					result += "Time: {}\n".format(y)

	except: # if there aren't enough parts
		return False # returns false
	return result

def parseOtherStuff(mediaInfo):
	try:
		result = ""
		for i in mediaInfo:
			for x, y in enumerate(i):
				if x == 0:
					result += "ID {}:\t".format(y)
				if x == 1:
					result += """Title: "{}"\t""".format(y)
				if x == 2:
					result += "Time: {}\n".format(y)

	except: # if there aren't enough parts
		return False # returns false
	return result

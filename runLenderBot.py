import decode as de
import lendingLibraryAdapter as adapter

import sqlite3
from sqlite3 import Error
import time
import datetime
import random
import os

from datetime import datetime
from slackclient import SlackClient

#####################
###   TODO List   ###
#####################

# update to the 2.X version and python3.7
# https://github.com/slackapi/python-slackclient/wiki/Migrating-to-2.x#basic-usage-of-the-rtm-client


#################################
###   Parameterized Queries   ###
#################################

# # example 1 -- simple placeholders
# db.execute('update players set name=?, score=?, active=? where jerseyNum=?', ('Smith, Steve', 42, True, 99))
 
# # example 2 -- named placeholders
# db.execute('update players set name=:name, score=:score, active=:active where jerseyNum=:num',
#     {'num': 100,
#      'name': 'John Doe',
#      'active': False,
#      'score': -1}
# )

###############################
###   Get the slack token   ###
###############################

de.MAIN_KEY = "lenderBot/data/lenderBot" # prod location
slack_client = SlackClient(de.getToken())

###############################
###   End the slack token   ###
###############################

############################################################################
############################################################################

# lenderBot's user ID in Slack: value is assigned after the bot starts up
templateID = None

# CONSTANTS
RTM_READ_DELAY = 0.5 # 0.5 second delay in reading events

CURATOR = "<@UC1LT08SX>" # Tony Strickland's ID

###########################
###   Snarky Comments   ###
###########################

adding = """I'll add "{}" to the hoard!"""

updateMediaType = """MediaType ID {} will now be set to "{}" """
updateMediaCategory = """MediaCategory ID {} will now be set to "{}" """
removeItem = """I'll make sure to throw "{}" to the wolves!"""

notAdmin = "Only the powerful can use this command!"
notDirect = "That is a DM only command, weakling!"

what = "I don't understand."
what2 = "I have no idea what you mean."
what3 = "That makes no sense!"
what4 = "I have half a mind to send you to the Avatar of Mitra!"

notEnough = "I can't add that, imbecile!"

doesntExist = "HA HA HA! That doesn't exist!"

notFound = "I couldn't find that! Perhaps it fell off a cliff."
notFound2 = "Despite my best efforts, that has been lost to time."
notFound3 = "That could not be found!"

conanTells = "Listen well and I shall tell you of who I am!"
aboutConan = "<https://www.youtube.com/watch?v=mZHoHaAYHq8|Conan the Librarian>"

publicHelp = "<https://drive.google.com/open?id=1kwWW0AzoOgjV9OGjfkJV4ah8ejZY81DMImyTRwMmxmI|Help Scroll>"
adminHelp = "<https://drive.google.com/open?id=1H_CUyR7JDUvfGD6lkhtbuM1gWW9dghePxlphyFVOhDs|Admin Help Scroll>"

cromHelp = "Crom helps those who help themselves. I send you help scrolls!"
returnItem = "Crom helps those who help reshelve."

checkedOUT = """It seems "{}" has been taken already! Are you sure that was correct?"""
tooManyOut = "You have taken too much of the hoard! You'll need to speak to Curator {} to take more.".format(CURATOR)
takeIt = """I'll let you borrow "{}" for a time."""
bringIt = """I'm glad you brought "{}" back! I was beginning to think I would need to hunt you down!"""

notTaken = """No one has borrowed "{}". Perhaps you should strike first, and take it!"""
adminCheckOut = """Alright! I'll let {} borrow "{}" ... for a time."""
adminCheckIN = """I'll put "{}" back in the hoard!"""

notYou = """You didn't check out "{}"!"""
noGreed = "Stop being greedy! You have borrowed enough of my hoard!"

correctCheckOUT = "HA HA HA! That's wrong! Try !checkOUT[SPACE]##"
correctCheckIN = "HA HA HA! That's wrong! Try !checkIN[SPACE]##"

############################################################################
############################################################################

###################################
###   Slack Response commands   ###
###################################

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

def inChannelResponse(channel,response):
	slack_client.api_call(
		"chat.postMessage",
		channel=channel,
		text=response,
		as_user=True
		)
	return

def threadedResponse(channel,response,stamp):
	slack_client.api_call(
		"chat.postMessage",
		channel=channel,
		text=response,
		thread_ts=stamp,
		as_user=True
		)
	return

def directResponse(someUser,text):
	slack_client.api_call(
		"chat.postMessage",
		channel=someUser,
		text=text,
		as_user=True
		)
	return

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
			theUser = item [2]
			theTime = item [3]

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
		typeID = stripper[0]
		newType = stripper[1]

	except: # if there aren't enough parts
		return False # returns false
	return typeID, newType

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
		newCategory = stripper[1].title()

	except: # if there aren't enough parts
		return False # returns false
	return mediaID, newCategory

def parseAdminCheckout(mediaInfo):
	try:
		stripper = [x.strip() for x in mediaInfo.split(',', 1)]
		mediaID = stripper[0]
		slackID = stripper[1]

	except: # if there aren't enough parts
		return False # returns false
	return mediaID, slackID

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

##################################################################################################################################

################################
###   BEGIN handle_command   ###
################################

def handle_command(command, channel, aUser, tStamp):
	
	command = command.lower()
	response = None

	###########################
	###   PUBLIC commands   ###
	###########################

	#################
	###   !fact   ###
	#################
	    
	if command == "!fact":
		# TODO generate a random Conan fact
		return

	###################
	###   !insult   ###
	###################

	if command == "!insult":
		# TODO generate a random Conan insult
		return

	#################
	###   !help   ###
	#################

	if command == "!help".lower():
		inChannelResponse(channel, cromHelp)
		if adapter.isAdmin(aUser):
			directResponse(aUser, adminHelp)
			return
		directResponse(aUser, publicHelp)
		return

	################
	###   !who   ###
	################

	if command == "!who":
		inChannelResponse(channel, conanTells)
		directResponse(aUser, aboutConan)
		return

	###############################
	###   !allMediaCategories   ###
	###############################

	if command == "!allMediaCategories".lower():
		if adapter.isDirect(channel):
			allCategory = adapter.selectAll_MediaCategory()
			parsed = parseMediaCategory_select(allCategory)
			inChannelResponse(channel, parsed)
			return
		inChannelResponse(channel, notDirect)
		return

	##########################
	###   !allMediaTypes   ###
	##########################

	if command == "!allMediaTypes".lower():
		if adapter.isDirect(channel):
			allCategory = adapter.selectAll_MediaType()
			parsed = parseMediaType_select(allCategory)
			inChannelResponse(channel, parsed)
			return
		inChannelResponse(channel, notDirect)
		return

	#######################
	###   !everything   ###
	#######################

	if command == "!everything".lower():
		if adapter.isDirect(channel):
			allMedia = adapter.format_Media()
			parsed = parseMedia_select(allMedia)
			inChannelResponse(channel, parsed)
			return
		inChannelResponse(channel, notDirect)
		return

	######################
	###   !available   ###
	######################

	if command == "!available".lower():
		if adapter.isDirect(channel):
			allMedia = adapter.format_Media_Available()
			parsed = parseMedia_select(allMedia)
			inChannelResponse(channel, parsed)
			return
		inChannelResponse(channel, notDirect)
		return

	#######################
	###   !myStuff   ###
	#######################

	if command == "!myStuff".lower():
		if adapter.isDirect(channel):
			allMedia = adapter.getMyStuff(aUser)
			parsed = parseMyStuff(allMedia)
			inChannelResponse(channel, parsed)
			return
		inChannelResponse(channel, notDirect)
		return

	#####################
	###   !checkOut   ###
	#####################

	if command.startswith("!checkOut".lower()):
		if adapter.isDirect(channel):
			someID = command[len("!checkOut")+1:].strip()
			if someID:
				exists = adapter.getMediaNameByID(someID)
				if exists != -1 and exists:
					sqlResult = adapter.Media_CheckOUT(someID, aUser)
					if sqlResult == 5:
						inChannelResponse(channel, checkedOUT.format(exists))
						return
					if sqlResult == 4:
						inChannelResponse(channel, noGreed)
						return
					if not sqlResult:
						inChannelResponse(channel, takeIt.format(exists))
						return
					inChannelResponse(channel, checkedOUT.format(exists))
					return
				inChannelResponse(channel, doesntExist)
				return
			inChannelResponse(channel, correctCheckOUT)
			return
		inChannelResponse(channel, notDirect)
		return

	####################
	###   !checkIn   ###
	####################

	if command.startswith("!checkIn".lower()):
		if adapter.isDirect(channel):
			someID = command[len("!checkIn")+1:].strip()
			if someID:
				exists = adapter.getMediaNameByID(someID)
				if exists != -1 and exists:
					sanatary = sanitizeID(aUser)
					sqlResult = adapter.Media_CheckIN(someID, sanatary)
					if sqlResult == 3:
						inChannelResponse(channel, notYou.format(exists))
						return
					if sqlResult == 5:
						inChannelResponse(channel, checkedOUT.format(exists))
						return
					if not sqlResult:
						inChannelResponse(channel, bringIt.format(exists))
						return
					inChannelResponse(channel, notTaken.format(exists))
					return
				inChannelResponse(channel, doesntExist)
				return
			inChannelResponse(channel, correctCheckIN)
			return
		inChannelResponse(channel, notDirect)
		return

	###############################
	###   END PUBLIC commands   ###
	###############################

	##########################
	###   ADMIN commands   ###
	##########################

	#####################
	###   !allFacts   ###
	#####################

	if command == "!allFacts".lower():
		if adapter.isAdmin(aUser):
			if adapter.isDirect(channel):
				allMedia = adapter.selectAll_Facts()
				parsed = parseFact_select(allMedia)
				inChannelResponse(channel, parsed)
				return
			inChannelResponse(channel, notDirect)
			return
		inChannelResponse(channel, notAdmin)
		return

	####################
	###   !addFact   ###
	####################

	if command.startswith("!addFact".lower()):
		if adapter.isAdmin(aUser):
			if adapter.isDirect(channel):
				mediaInfo = command[len("!addFact")+1:].strip().capitalize()
				if len(mediaInfo) > 10:
					sqlResult = adapter.insert_Fact(mediaInfo)
					if not sqlResult:
						inChannelResponse(channel,"""I had forgotten about that! I'll begin telling this tale when asked for more:\n{}""".format(mediaInfo))
						return
					inChannelResponse(channel, notEnough)
					return
				inChannelResponse(channel, what)
				return
			inChannelResponse(channel, notDirect)
			return
		inChannelResponse(channel, notAdmin)
		return

	#######################
	###   !removeFact   ###
	#######################

	if command.startswith("!removeFact".lower()):
		if adapter.isAdmin(aUser):
			if adapter.isDirect(channel):
				someID = command[len("!removeFact")+1:].strip()
				if someID:
					exists = adapter.getFactByID(someID)
					if exists != -1 and exists:
						sqlResult = adapter.remove_Facts(someID)
						if not sqlResult:
							inChannelResponse(channel, removeItem.format(exists)) ## TODO format this properly to remove Fact
							return
						inChannelResponse(channel, notFound3)
						return
					inChannelResponse(channel, doesntExist)
					return
				inChannelResponse(channel, what)
				return
			inChannelResponse(channel, notDirect)
			return
		inChannelResponse(channel, notAdmin)
		return

	#######################
	###   !allInsults   ###
	#######################

	if command == "!allInsults".lower():
		if adapter.isAdmin(aUser):
			if adapter.isDirect(channel):
				allMedia = adapter.selectAll_Insults()
				parsed = parseInsult_select(allMedia)
				inChannelResponse(channel, parsed)
				return
			inChannelResponse(channel, notDirect)
			return
		inChannelResponse(channel, notAdmin)
		return

	######################
	###   !addInsult   ###
	######################

	if command.startswith("!addInsult".lower()):
		if adapter.isAdmin(aUser):
			if adapter.isDirect(channel):
				mediaInfo = command[len("!addInsult")+1:].strip().capitalize()
				if len(mediaInfo) > 10:
					sqlResult = adapter.insert_Insult(mediaInfo)
					if not sqlResult:
						inChannelResponse(channel,"""That's a good one! I'll make sure to remember to hurl this at those who displease me:\n{}""".format(mediaInfo)) # TODO set up add an insult
						return
					inChannelResponse(channel, notEnough)
					return
				inChannelResponse(channel, what)
				return
			inChannelResponse(channel, notDirect)
			return
		inChannelResponse(channel, notAdmin)
		return

	#########################
	###   !removeInsult   ###
	#########################

	if command.startswith("!removeInsult".lower()):
		if adapter.isAdmin(aUser):
			if adapter.isDirect(channel):
				someID = command[len("!removeInsult")+1:].strip()
				if someID:
					exists = adapter.getInsultByID(someID)
					if exists != -1 and exists:
						sqlResult = adapter.remove_Insults(someID)
						if not sqlResult:
							inChannelResponse(channel, removeItem.format(exists)) ## TODO format this properly to reomve Insult
							return
						inChannelResponse(channel, notFound3)
						return
					inChannelResponse(channel, doesntExist)
					return
				inChannelResponse(channel, what)
				return
			inChannelResponse(channel, notDirect)
			return
		inChannelResponse(channel, notAdmin)
		return

	#########################
	###   !addMediaType   ###
	#########################
	# Video Games, Card Games, Books, etc.

	if command.startswith("!addMediaType".lower()):
		if adapter.isAdmin(aUser):
			if adapter.isDirect(channel):
				mediaInfo = command[len("!addMediaType")+1:].strip().title()
				if len(mediaInfo) > 4 and len(mediaInfo) < 20:
					sqlResult = adapter.insert_MediaType(mediaInfo)
					if not sqlResult:
						inChannelResponse(channel,"""I'll add "{}" to the types of media carried by the backs of our enemies!""".format(mediaInfo))
						return
					inChannelResponse(channel, notEnough)
					return
				inChannelResponse(channel, what)
				return
			inChannelResponse(channel, notDirect)
			return
		inChannelResponse(channel, notAdmin)
		return

	#############################
	###   !addMediaCategory   ###
	#############################
	# Horror, Anime, Family, etc.

	if command.startswith("!addMediaCategory".lower()):
		if adapter.isAdmin(aUser):
			if adapter.isDirect(channel):
				mediaInfo = command[len("!addMediaCategory")+1:].strip().title()
				if len(mediaInfo) > 4 and len(mediaInfo) < 20:
					sqlResult = adapter.insert_MediaCategory(mediaInfo)
					if not sqlResult:
						inChannelResponse(channel,"""I'll add "{}" to the categories of media!""".format(mediaInfo))
						return
					inChannelResponse(channel, notEnough)
					return
				inChannelResponse(channel, what)
				return
			inChannelResponse(channel, notDirect)
			return
		inChannelResponse(channel, notAdmin)
		return

	#####################
	###   !addMedia   ###
	#####################

	if command.startswith("!addMedia".lower()):
		if adapter.isAdmin(aUser):
			if adapter.isDirect(channel):
				mediaInfo = command[len("!addMedia")+1:].strip().title()
				if mediaInfo:
					parsed, mediaName = parseMedia_insert(mediaInfo)
					sqlResult = adapter.insert_Media(parsed)
					if not sqlResult:
						inChannelResponse(channel, adding.format(mediaName))
						return
					inChannelResponse(channel, notEnough)
					return
				inChannelResponse(channel, what)
				return
			inChannelResponse(channel, notDirect)
			return
		inChannelResponse(channel, notAdmin)
		return

	########################
	###   !removeMedia   ###
	########################

	if command.startswith("!removeMedia".lower()):
		if adapter.isAdmin(aUser):
			if adapter.isDirect(channel):
				someID = command[len("!removeMedia")+1:].strip()
				if someID:
					exists = adapter.select_MediaID(someID)
					if exists != -1 and exists:
						sqlResult = adapter.remove_Media(someID)
						if not sqlResult:
							inChannelResponse(channel, removeItem.format(exists[0][4]))
							return
						inChannelResponse(channel, notFound3)
						return
					inChannelResponse(channel, doesntExist)
					return
				inChannelResponse(channel, what)
				return
			inChannelResponse(channel, notDirect)
			return
		inChannelResponse(channel, notAdmin)
		return

	# TODO improve the below 2 functions to allow updates to the 
	# type/category of a specific media item

	################################
	###   !updateMediacategory   ###
	################################

	# if command.startswith("!updateMediaCategory".lower()):
	# 	if adapter.isAdmin(aUser):
	# 		if adapter.isDirect(channel):
	# 			mediaInfo = command[len("!updateMediacategory")+1:].strip()
	# 			if mediaInfo:
	# 				typeID, newType = parseMediaCategory_update(mediaInfo)
	# 				newType = newType.title()
	# 				sqlResult = adapter.update_MediaCategory(typeID, newType)
	# 				if not sqlResult:
	# 					inChannelResponse(channel, updateMediaCategory.format(typeID, newType))
	# 					return
	# 				inChannelResponse(channel, notFound3)
	# 				return
	# 			inChannelResponse(channel, what)
	# 			return
	# 		inChannelResponse(channel, notDirect)
	# 		return
	# 	inChannelResponse(channel, notAdmin)
	# 	return

	############################
	###   !updateMediaType   ###
	############################

	# if command.startswith("!updateMediaType".lower()):
	# 	if adapter.isAdmin(aUser):
	# 		if adapter.isDirect(channel):
	# 			mediaInfo = command[len("!updateMediaType")+1:].strip().title()
	# 			if mediaInfo:
	# 				typeID, newType = parseMediaType_update(mediaInfo)
	# 				newType = newType.title()
	# 				sqlResult = adapter.update_MediaType(typeID, newType)
	# 				if not sqlResult:
	# 					inChannelResponse(channel, updateMediaType.format(typeID, newType))
	# 					return
	# 				inChannelResponse(channel, notFound3)
	# 				return
	# 			inChannelResponse(channel, what)
	# 			return
	# 		inChannelResponse(channel, notDirect)
	# 		return
	# 	inChannelResponse(channel, notAdmin)
	# 	return

	##########################
	###   !adminCheckOut   ###
	##########################

	if command.startswith("!adminCheckOut".lower()):
		if adapter.isAdmin(aUser):
			if adapter.isDirect(channel):
				mediaInfo = command[len("!adminCheckOut")+1:].strip()
				if mediaInfo:
					mID, sID = parseAdminCheckout(mediaInfo)
					exists = adapter.getMediaNameByID(mID)
					if exists:
						sanatary = sanitizeID(sID)
						sqlResult = adapter.Media_adminCheckOUT(mID, sanatary)
						if sqlResult == 5:
							inChannelResponse(channel, checkedOUT.format(exists))
							return
						if not sqlResult:
							inChannelResponse(channel, adminCheckOut.format(sID.upper(), exists))
							return
						inChannelResponse(channel, doesntExist)
						return
					inChannelResponse(channel, notEnough)
					return
				inChannelResponse(channel, what)
				return
			inChannelResponse(channel, notDirect)
			return
		inChannelResponse(channel, notAdmin)
		return

	#########################
	###   !adminCheckIn   ###
	#########################

	if command.startswith("!adminCheckIn".lower()):
		if adapter.isAdmin(aUser):
			if adapter.isDirect(channel):
				someID = command[len("!adminCheckIn")+1:].strip()
				if someID:
					exists = adapter.getFactByID(someID)
					if exists != -1 and exists:
						sqlResult = adapter.Media_adminCheckIN(someID)
						if not sqlResult:
							inChannelResponse(channel, adminCheckIN.format(exists))
							return
						inChannelResponse(channel, notFound3)
						return
					inChannelResponse(channel, doesntExist)
					return
				inChannelResponse(channel, what)
				return
			inChannelResponse(channel, notDirect)
			return
		inChannelResponse(channel, notAdmin)
		return

	######################
	###   !whoTookIt   ###
	######################

	if command == "!whoTookIt".lower():
		if adapter.isAdmin(aUser):
			if adapter.isDirect(channel):
				allMedia = adapter.format_Media_WhosGotIt()
				parsed = parseMedia_WhosGotIt(allMedia)
				inChannelResponse(channel, parsed)
				return
			inChannelResponse(channel, notDirect)
			return
		inChannelResponse(channel, notAdmin)
		return

	##############################
	###   END ADMIN commands   ###
	##############################

	#######################################
	return   ###   END handle_command   ###
	#######################################

##################################################################################################################################

################
###   Main   ###
################

if __name__ == "__main__":
	if slack_client.rtm_connect(with_team_state=False):
		print("Lenderbot is running!")
		# Read bot's user ID by calling Web API method `auth.test`
		templateID = slack_client.api_call("auth.test")["user_id"]
		while True:
			try:
				command, channel,usr,stp = parseSlackInput(slack_client.rtm_read())
				if command:
					handle_command(command, channel,usr,stp)
			except:
				pass
                
		time.sleep(RTM_READ_DELAY)
	else:
		pass
		print("Connection failed. Exception traceback printed above.")

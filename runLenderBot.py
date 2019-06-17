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

# update to the 2.x version and python3
# https://github.com/slackapi/python-slackclient/wiki/Migrating-to-2.x#basic-usage-of-the-rtm-client

###############################
###   Get the slack token   ###
###############################

de.MAIN_KEY = "data/lenderBot"
# de.MAIN_KEY = "lenderBot/data/lenderBot" # prod location
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

cromHelp = "Crom helps those who help themselves."
returnItem = "Crom helps those who help reshelve."

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

def parseMedia_insert(mediaInfo):
	try:
		stripper = [x.strip() for x in mediaInfo.split(',', 4)]

		theMediaType = adapter.get_MediaTypeID(stripper[0])
		theMediaCategory = adapter.get_MediaCategoryID(stripper[1])
		theUser = stripper[2].replace('<','').replace('>','').replace('@','').upper()
		isLong = longGame(stripper[3])
		theFullName = stripper[4]

		insertString = "{}, {}, '{}', '{}', {}".format(theMediaType, theMediaCategory, theUser, theFullName, isLong)

	except: # if there aren't enough parts
		return False # returns false
	return insertString, theFullName

def parseMedia_select(mediaInfo): # TODO improve this to add 'checked out' 
	try:
		result = "Allow me to show you the hoard!\n\n"
		for item in mediaInfo:
			theID = item[0]
			theTitle = item[1]
			theCategory = item [2]
			theType = item [3]
			theLength = item[4]

			formatted = """{}: Title: "{}"\tCategory: {}\tMedium: {}\tLength: {}""".format(theID, theTitle, theCategory, theType, theLength)
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
		typeID = stripper[0]
		newType = stripper[1]

	except: # if there aren't enough parts
		return False # returns false
	return typeID, newType

##################################################################################################################################

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
			parsed = parseMedia_select(allMedia) # TODO add "checked out"
			inChannelResponse(channel, parsed)
			return
		inChannelResponse(channel, notDirect)
		return

	######################
	###   !available   ###
	######################

	if command == "!available".lower():
		if adapter.isDirect(channel):
			allMedia = adapter.format_Media()
			parsed = parseMedia_select(allMedia) # TODO calculate "checked out"
			inChannelResponse(channel, parsed)
			return
		inChannelResponse(channel, notDirect)
		return

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
					sqlResult = adapter.insert_MediaType(mediaInfo)
					if not sqlResult:
						inChannelResponse(channel,"""I'll add "{}" to the types of media carried by the backs of our enemies!""".format(mediaInfo))  # TODO set up add a fact
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
				someID = command[len("!removeFact")+1:].strip().title()
				if someID:
					exists = adapter.select_MediaID(someID)
					if exists != -1 and exists:
						sqlResult = adapter.remove_Media(someID)
						if not sqlResult:
							inChannelResponse(channel, removeItem.format(exists[0][4])) ## TODO format this properly to remove Fact
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
					sqlResult = adapter.insert_MediaType(mediaInfo)
					if not sqlResult:
						inChannelResponse(channel,"""I'll add "{}" to the types of media carried by the backs of our enemies!""".format(mediaInfo)) # TODO set up add an insult
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
				someID = command[len("!removeInsult")+1:].strip().title()
				if someID:
					exists = adapter.select_MediaID(someID)
					if exists != -1 and exists:
						sqlResult = adapter.remove_Media(someID)
						if not sqlResult:
							inChannelResponse(channel, removeItem.format(exists[0][4])) ## TODO format this properly to reomve Insult
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

	if command.startswith("!addMediaCategory".lower()):
		if adapter.isAdmin(aUser):
			if adapter.isDirect(channel):
				mediaInfo = command[len("!addMediaCategory")+1:].strip().title()
				if len(mediaInfo) > 4 and len(mediaInfo) < 20:
					sqlResult = adapter.insert_MediaCategory(mediaInfo)
					if not sqlResult:
						inChannelResponse(channel,"""I'll add "{}" to the categories of media! This pleases Ymir!""".format(mediaInfo))
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
				someID = command[len("!removeMedia")+1:].strip().title()
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

	######
	return 

	##############################
	###   End handle_command   ###
	##############################

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
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

# lenderbot's user ID in Slack: value is assigned after the bot starts up
templateID = None

# constants
RTM_READ_DELAY = 0.5 # 0.5 second delay in reading events

###########################
###   Snarky comments   ###
###########################

notAdmin = "Only the powerful can use this command!"
notDirect = "That is a DM only command, weakling!"
what = "I don't understand."
notEnough = "I can't add that, imbecile!"

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

def parseMedia(mediaInfo):
	try:
		result = [x.strip() for x in mediaInfo.split(',', 4)]
	except: # if there aren't enough parts
		return False # returns all false
	return result

##################################################################################################################################

def handle_command(command, channel, aUser, tStamp):
	
	command = command.lower()
	response = None
    
	if command == "!test":
		response = (("""Text:{0}
				Channel:{1}
				TS:{2}
				User:{3}
				""").format(command,channel,tStamp,aUser))
		inChannelResponse(channel,response)
		return
	    
	if command == "!fact":
		# need to generate a random Conan fact
		return

	##########################
	###   ADMIN commands   ###
	##########################

	### https://www.youtube.com/watch?v=mZHoHaAYHq8 - Conan the librarian
	### DK9JT0TMJ - DM channel with Conan

	adminDMIDs = {
		'DK9JT0TMJ' : "Andre Gueret",
		'DK1G58Q0K' : "Daniel Hodge",
		'DKCVBJPNC' : "Tony Strickland"
	}

	if command == "!admin":
		if adapter.isAdmin(aUser):
			inChannelResponse(channel,"I'm an admin!")
			return
		inChannelResponse(channel,"Not an admin.")
		return

	if command.startswith("!addMediaType".lower()):
		if adapter.isAdmin(aUser):
			if channel in adminDMIDs:
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

	if command.startswith("!addMediaCategory".lower()):
		if adapter.isAdmin(aUser):
			if channel in adminDMIDs:
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

	if command.startswith("!addMedia".lower()):
		if adapter.isAdmin(aUser):
			if channel in adminDMIDs:
				mediaInfo = command[len("!addMedia")+1:].strip().title()
				if len(mediaInfo) > 4 and len(mediaInfo) < 20:
					sqlResult = adapter.insert_MediaCategory(mediaInfo)
					if not sqlResult:
						inChannelResponse(channel,"""I'll add "{}" to the collection. Set will consume""".format(mediaInfo))
						return
					inChannelResponse(channel, notEnough)
					return
				inChannelResponse(channel, what)
				return
			inChannelResponse(channel, notDirect)
			return
		inChannelResponse(channel, notAdmin)
		return

	return ### End handle_command(command, channel,aUser,tStamp)

##################################################################################################################################

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
		print("Connection failed. Exception traceback printed above.")
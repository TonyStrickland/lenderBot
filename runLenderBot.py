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

# SQLite3 syntax to connect to database
# 
# conn = sqlite3.connect('SOME DATABASE')
# serverCursor = conn.cursor() 

de.MAIN_KEY = "lenderBot"
slack_client = SlackClient(de.getToken())

# lenderbot's user ID in Slack: value is assigned after the bot starts up
templateID = None

# constants
RTM_READ_DELAY = 0.5 # 0.5 second delay in reading events

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

def handle_command(command, channel,aUser,tStamp):
	
	command = command.lower()
	response = None

	# This is where you implement commands

	if command == "!history":
		directResponse(aUser,response)
		return
    
	if command.startswith("!test"):
		response = (("""Text:{0}
				Channel:{1}
				TS:{2}
				User:{3}
				""").format(command,channel,tStamp,aUser))
		inChannelResponse(channel,response)
		return

	# ADMIN command
	if command == "!farewell":
		if aUser == "SPECIFY ID":
			inChannelResponse(channel,"I'm an admin!")
		return
	return

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
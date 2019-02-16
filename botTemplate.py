import sqlite3
from sqlite3 import Error
import time
import datetime
import random
# import schedule
# import mysql.connector
import base64
import os
import cryptography
import slackclient

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from datetime import datetime
# from slackclient import SlackClient

# SQLite3 syntax to connect to database
# 
# conn = sqlite3.connect('SOME DATABASE')
# serverCursor = conn.cursor() 

##########################################################
#                                                        #
#  You will need to have access to the slack token and   #
#  create a key file and token pair with encoder.py      #
# .key files have been added to gitignore and            #
# should never be published                              #
#                                                        #
##########################################################

# keyFile = open('path/to/.key', 'rb')
# key = keyFile.read()
# keyFile.close()

# f = Fernet(key)

# encryptedTokenFile = open('path/to/encrypted/.token', 'rb')
# encryptedToken = encryptedTokenFile.read()

# decryptedToken = f.decrypt(encryptedToken)

SLACK_BOT_TOKEN = "xoxb-323434273830-530815171060-CWuVt1jCJ842s5hbTZsP41o5"

# instantiate Slack client
slack_client = slackclient(SLACK_BOT_TOKEN)
# starterbot's user ID in Slack: value is assigned after the bot starts up
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
		print("Slackbot is running!")
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
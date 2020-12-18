#!/usr/bin/python3

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import Conan.commandUtils as commandUtils
import Conan.decode as de
from slack import RTMClient, WebClient

##############################
###   Client 2.0 Updated   ###
##############################

__self_user_id = '' # Bot's user ID here

###############################
###   Get the slack token   ###
###############################

#de.MAIN_KEY = "/home/pi/Slackbot/Conan/data/lenderBot" #prod location
de.MAIN_KEY = "H:/Projects/lenderBot/Conan/data/lenderBot" #test path
__slack_token = de.getToken() 


###############################
###   End the slack token   ###
###############################

############################################################################
############################################################################

# lenderBot's user ID in Slack: value is assigned after the bot starts up
templateID = None

def __should_handle(user=__self_user_id, text=''):
    return (user != __self_user_id
        and len(text) != 0)

if __name__ == '__main__':
    

    def main():
        @RTMClient.run_on(event='message')
        def handle(**kwargs):
            data = kwargs['data']   
            text = data['text'] 
            if data['user'] != __self_user_id and len(text) != 0 and text.startswith('!'):
                commandUtils.runCommand(kwargs)

        rtm_client = RTMClient(token=__slack_token)
        rtm_client.start()
        
    main()


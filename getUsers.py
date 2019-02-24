###################################################################
#                                                                 #
#   This will create a file of all the user names and their IDs   #
#                                                                 #
###################################################################

def createUserFile(slack_client):

    members = slack_client.api_call('users.list')
    members = members['members']
    members = [m for m in members if not m['is_bot'] and not m['is_app_user']]

    slack_users = []

    print("Beginning Slack user retrieval")

    i = 0
    for member in members:
        SlackID = member['id']
        name = member['name']

        slack_users.append([SlackID,name])
       
        i += 1

        print("{} Slack records processed...".format(i))

    print("creating a file")

    userFile = open("allUsers.user","w")

    for userID, userName in slack_users:
        userName.replace("."," ")
        userName = userName.title()
        userID = userID.upper()


        userFile.write("{}|{}\n".format(userName,userID))

    userFile.close()

    print('User file created!')
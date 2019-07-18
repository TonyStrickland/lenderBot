import publicCommands

commandList = []

######################
# Load public commands
###################### 

commandList.append(publicCommands.SayHello())

def runCommand(payload):
    if 'text' in payload['data']:
        data = payload['data']
        text = data['text'].strip(' ')   
        text = text[1:]
        for option in commandList:
            if text.lower().startswith(str(option.name).lower()):
                option_method = getattr(option.source, option.method.__name__)
                if option_method:
                    option.method(payload)



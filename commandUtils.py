from commands import publicCommands as publicCommands
from commands import adminCommands as adminCommands

commandList = []
commandList = publicCommands.published + adminCommands.published

def checkCommand(text, option):
    check = text.split(' ')[0]
    for name in option.name:
        if check == name.lower():
            return True
    return False

def runCommand(payload):
    if 'text' in payload['data']:
        data = payload['data']
        text = data['text'].strip(' ')   
        text = text[1:]
        for option in commandList:
            if checkCommand(text, option):
                option_method = getattr(option.source, option.method.__name__)
                if option_method:
                    option.method(payload)
                break
                



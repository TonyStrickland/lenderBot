import lendingLibraryAdapter as adapter

class Command():
    def __init__(self, source, method, name, **kwargs):
        self.method = method
        self.source = source
        self.name = name
        self.kwargs = kwargs

def parseSlackInput(aText):
    if aText and len(aText) > 0:
        item = aText[0]  # gets first (only) item
        if 'text' in item:
            msg = item['text'].strip(' ')  # text of the message
            chn = item['channel']  # ID of the channel
            usr = item['user']  # ID of the user
            stp = item['ts']  # Timestamp at which message was posted
            return [str(msg), str(chn), str(usr), str(stp)]
        else:
            return [None, None, None, None]


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


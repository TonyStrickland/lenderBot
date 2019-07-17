class Command():
    def __init__(self, source, method, name, **kwargs):
        self.method = method
        self.source = source
        self.name = name
        self.kwargs = kwargs

    def ParsePayload(self, payLoad)
        web_client = payLoad['web_client']
        data = payLoad['data']
        channel = data['channel']
        text = data['text']
        return web_client, data, channel, text

class SayHello(Command):
    def __init__(self):
        super().__init__(source = SayHello, method = self.say_hello, name = "Hello")

    def say_hello(self, payLoad):
        thread_ts = None
        web_client, data, channel, text = ParsePayload(payLoad)
        if 'thread_ts' in payLoad:
            thread_ts = payLoad['thread_ts']
        if web_client is not None and len(text) > 0:
            message_args = {
                'channel' : channel,
                'text' : 'Hello!',
                'as_user' : True
            }       
            if thread_ts is not None:
                message_args['thread_ts'] = thread_ts   
        web_client.chat_postMessage(**message_args)

#untested code
class Help(Command):
    def __init__(self):
        super().__init__(source = SayHello, method = self.help, name = "Help")

    def help(self, payLoad):
        inChannelResponse(channel, cromHelp)
		if adapter.isAdmin(aUser):
			directResponse(aUser, adminHelp)
			return
		directResponse(aUser, publicHelp)
		return


from slack import RTMClient, WebClient

__self_user_id = '' # Bot's user ID here
__slack_token = None # Bot's Slack token goes here...duh

def send_simple_message(web_client, channel, text, thread_ts=None): ## not sure if this is in the right place...
    if web_client is not None and len(text) > 0:
        message_args = {
            'channel' : channel,
            'text' : text
        }
        
        if thread_ts is not None:
            message_args['thread_ts'] = thread_ts
    
    web_client.chat_postMessage(**message_args)

def __should_handle(user=__self_user_id, text=''):
    return (user != __self_user_id and len(text) is not 0)

def handle_message(web_client, data):
    channel = data['channel']
    #text = data['text']
    time = data['ts']
    send_simple_message(web_client, channel, "Message trigger", time)

def main():
    __rtm_client = RTMClient(token=__slack_token)
    
    @RTMClient.run_on(event='message')
    def message_handle(**payload):
        web_client = payload['web_client']
        data = payload['data']
        user = data['user']
        if user != __self_user_id and len(data['text']) is not 0:
            handle_message(web_client, data)

    __rtm_client.start()

if __name__ == '__main__':
    __web_client = WebClient(token=__slack_token)
    __self_user_id = __web_client.auth_test()['user_id']
    main()  

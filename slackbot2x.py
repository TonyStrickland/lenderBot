from slack import RTMClient, WebClient
import command

__self_user_id = '' # Bot's user ID here
__slack_token = None # Bot's Slack token goes here...duh

def __should_handle(user=__self_user_id, text=''):
    return (user != __self_user_id
        and len(text) is not 0)

if __name__ == '__main__':
    __slack_token = None # Bot's Slack token goes here...duh

    def main():
 
        @RTMClient.run_on(event='message')
        def handle(**kwargs):
            data = kwargs['data']   
            text = data['text'] 
            if data['user'] != __self_user_id and len(text) is not 0 and text.startswith('!'):
                command.runCommand(kwargs)

        rtm_client = RTMClient(token=__slack_token)
        rtm_client.start()
        
    main()


import os
import time
import event
from slackclient import SlackClient

class Bot(Object):
    def __init__(self):
        self.slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
        self.bot_name = "scale_sentry_bot"
        self.bot_id = self.get_bot_id()
        if self.bot_id is None:
            exit("Error, could not find " + self.bot_name)
        
        self.event = event.Event(self)
        self.listen()
    
    def get_bot_id(self):
        api_call = self.slack_client.api_call("users.list")
        if api_call.get('ok'):
            # Recupera todos los usuarios para encontrar al bot
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self.bot_name:
                    print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
                    return user.get('id')
            
            return None
    
    def listen(self):
        if self.slack_client.rtm_connect(with_team_state=False):
            print("Successfully connected, listening for commands")
            while True:
                self.event.wait_for_event()
                
                time.sleep(1)
        else:
            exit("Error, Connection Failed")

if __name__ == "__main__":
    bot = Bot()
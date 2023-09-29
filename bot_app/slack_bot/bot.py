import os
import slackclient

class Bot:
    def __init__(self, token):
        self.slack_client = slackclient.SlackClient(token)
        self.bot_name = "scale_sentry_bot"
        #self.bot_id = self.get_bot_id()
        if self.bot_id is None:
            exit("Error, could not find " + self.bot_name)
    
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
    
    def handle_message(self, event):
        message = event["text"]
        if message.startswith("<@%s>" % self.bot_id):
            self.slack_client.api_call("chat.postMessage", channel=event["channel"], text="Hola <@%s>!" % event["user"], as_user=True)
    
    def execute(self):
        self.slack_client.start()

if __name__ == "__main__":
    bot = Bot(os.environ.get('SLACK_BOT_TOKEN'))
    bot.start()
from .bot import Bot

class BotManager(object):

    def __init__(self, config=None):
        self.config = config
        self.active = False
        self.bot = None
        self.event = None

    def is_active(self):
        if self.bot == None:
            return False
        return self.bot.is_active()

    def start(self, listener, channel):
        if self.bot != None:
            if self.bot.is_active():
                return
        
        self.bot = Bot(
            config=self.config,
            listener=listener
        ).connect(channel)

    def stop(self):
        self.bot.shutdown()

    def get_config(self):
        return self.config

    def send_command_to_bot(self, command):        
        self.bot.receive(command)
        


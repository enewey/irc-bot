
class IrcConfig(object):

    def __init__(self, config=None):
        if config is not None:
            self.load_config(config)
        
    def load_config(self, data):
        self.host = data['host']
        self.port = data['port']
        self.user = data['user']
        self.token = data['token']
        self.channel = data['channel']
        return self
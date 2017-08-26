import json

from gui import GuiConfig
from irc import IrcConfig

# defaults
DEFAULT_CONFIG = {
    'host':'',
    'port':'',
    'user':'',
    'token':'',
    'channel':''
}

class Config(object):

    def __init__(self, config=None):
        if config is not None:
            self.load_config(config)
        
    def load_config(self, data):
        #Config blobs
        self.gui = GuiConfig(data['gui'])
        self.irc = IrcConfig(data['irc'])
        return self

    def load_json(self, filename):
        with open(filename) as d:
            data = json.load(d)
        print "Data loaded: %s\n" % data
        return self.load_config(data)

import json

from .gui import GuiConfig
from .irc import IrcConfig

class Config(object):

    def __init__(self, env=None):
        if env is not None:
            self.load_config(env)
        
    def load_config(self, env):
        #Config blobs
        print("env loaded", env)
        self.gui = GuiConfig(env['gui'])
        self.irc = IrcConfig(env['irc'])
        return self



class GuiConfig(object):

    def __init__(self, config=None):
        if config is not None:
            self.load_config(config)
        
    def load_config(self, data):
        self.font = data['font']
        return self
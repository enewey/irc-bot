import os

def env():
    return {
        'gui': {
            'font': os.environ['BOT_GUI_FONT']
        },
        'irc': {
            'token': os.environ['BOT_TOKEN'],
            'user': os.environ['BOT_USER'],
            'channel': os.environ['BOT_CHANNEL'],
            'host': os.environ['BOT_HOST'],
            'port': int(os.environ['BOT_PORT'])
        }
    }
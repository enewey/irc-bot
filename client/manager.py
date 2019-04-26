#!/usr/bin/python

import threading
from .bot import BotClient

class BotManager(object):

    def __init__(self, config=None):
        self.config = config
        self.active = False
        self.client = None
        self.event = None

    def is_active(self):
        return self.active

    def start(self, listener, channel):
        if self.active:
            return

        self.active = True
        self.client = BotClient(config=self.config, listener=listener).connect(channel=channel)
        self.event = threading.Event()

        threading.Thread(target=self.client.watch_event, args=(self.event,)).start()

    def stop(self):
        if not self.active:
            return

        self.active = False
        self.event.set()
        self.client.exit()

    def get_config(self):
        return self.config

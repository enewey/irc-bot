#!/usr/bin/python

import threading
from bot import BotClient

class BotManager(object):

	def __init__(self):
		self.active=False

	def isActive(self):
		return self.active

	def start(self, listener):
		if self.active:
			return

		self.active = True
		self.client = BotClient(listener=listener)
		self.event = threading.Event()
		
		threading.Thread(target=self.client.watchEvent, args=(self.event,)).start()

	def stop(self):
		if not self.active:
			return

		self.active = False
		self.event.set()
		self.client.exit()


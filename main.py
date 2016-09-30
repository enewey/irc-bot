#!/usr/bin/python
from client.manager import BotManager
from gui.gui import Gui

manager = BotManager()
gui = Gui(manager=manager)
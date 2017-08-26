#!/usr/bin/python
from client.manager import BotManager
from gui.gui import Gui
from config.config import Config

cfg = Config().load_json('config.json')
manager = BotManager(config=cfg.irc)

Gui(manager=manager, config=cfg.gui)

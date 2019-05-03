#!/usr/local/bin/python3
from client.manager import BotManager
from gui.gui import Gui
from config.config import Config
from config.env import env

cfg = Config(env())
manager = BotManager(config=cfg.irc)

Gui(manager=manager, config=cfg.gui)

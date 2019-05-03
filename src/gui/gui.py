#!/usr/bin/python

import tkinter as tk
from tkinter import messagebox
import time
import datetime
import math

from .namebox import Namebox
from .infobar import InfoBar
from .chatbox import Chatbox
from config.gui import GuiConfig

class Gui(object):

    events = {}

    def __init__(self, manager=None, config=None):
        if config is None:
            config = GuiConfig().load_config({
                'font':'arial'
            })

        self.manager = manager

        self.root = tk.Tk()
        self.root.title("Twitch Bot")

        #Channel input
        self.input_box = tk.Entry()
        self.input_box.config(font=(config.font, 12, ''))
        self.input_box.grid(row=0, column=0, sticky='nsew')
        #default channel in config.json
        self.input_box.insert(0, self.manager.get_config().channel)

        #Start/stop button
        self.button = tk.Button(text="Start", command=self.button_press)
        self.button.grid(ipady=5, ipadx=20, row=1, column=0, sticky='nsew')

        #Timer
        self.run_timer = False
        self.timer = tk.Label(width=7, font=(config.font, 12, ''),
            text="-:--:--", bg='white')
        self.timer.grid(ipady=5, ipadx=5, row=0, rowspan=2,
             column=1, columnspan=1, sticky='nsew')

        #Scrollbar
        self.scrollbar = tk.Scrollbar()
        self.scrollbar.grid(row=2, column=2, sticky='nsew')

        #Namebox
        self.box = Namebox()
        for name in ["Alice", "Bob", "Cindy", "David", "Erich"]:
            self.box.insert(0, name)
        self.box.grid(ipady=6, ipadx=6, row=2, 
            column=0, columnspan=2, sticky='nsew')
        self.box.config(font=(config.font, 12, ''), yscrollcommand=self.scrollbar.set)
        self.register_event(self.box.update_event, self.box.update)
        self.scrollbar.config(command=self.box.yview)

        #Chatbox
        # self.chat_frame = tk.Frame(width=60, height=60)
        self.chat = Chatbox(self.root, width=100, height=20, 
            justify=tk.LEFT, anchor=tk.SW, text="", 
            font=(config.font, 10, ''))
        self.chat.grid(ipady=2, ipadx=2, row=2, 
            column=2, columnspan=3, sticky='se')
        self.chat.config(font=(config.font, 12, ''))
        self.register_event(self.chat.update_event, self.chat.update)

        #Chat input
        self.chat_input_box = tk.Entry()
        self.chat_input_box.config(font=(config.font, 12, ''), 
            width=100, justify=tk.LEFT)
        self.chat_input_box.grid(ipady=2, ipadx=2, row=3, 
            column=2, columnspan=3, sticky='se')
        self.chat_input_box.bind('<Return>', self.on_chat_input_return)

        # self.chat_frame.grid(ipady=6, ipadx=6, row=2, column=2, columnspan=10)

        #Info bar at bottom
        self.info = InfoBar(self.root, font=(config.font, 10, ''), bg='white')
        self.info.grid(ipady=2, ipadx=2, row=3, 
            column=0, columnspan=2, sticky='nsew')
        self.info.config(anchor=tk.W)
        self.register_event(self.info.update_event, self.info.update)

        # Set event protocol handlers
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)

        #It's go time boys
        self.root.mainloop()

    def on_chat_input_return(self, event):
        self.send_to_channel(self.chat_input_box.get(), self.input_box.get())
        self.chat_input_box.delete(0, tk.END)

    ###########################
    # Protocol handlers
    ###########################

    def on_close(self):
        if self.manager.is_active():
            if messagebox.askokcancel("Quit", 
                "IRC Bot is running and will be disconnected.\n\
                Are you sure you want to quit?"):
                self.manager.stop()
                self.root.destroy()
        else:
            self.root.destroy()

    ###########################
    # Timer related functions
    ###########################

    def tick(self):
        secs = math.floor(time.time() - self.starttime)
        if self.uptime != secs:
            self.uptime = secs
            self.timer.config(text=str(datetime.timedelta(seconds=self.uptime)))
        
        if self.run_timer:
            self.timer.after(200, self.tick)

    def stop_timer(self):
        self.run_timer = False

    def start_timer(self):
        self.starttime = time.time()
        self.uptime = time.time()
        self.run_timer = True
        self.tick()

    ###########################
    # Start/stop related functions
    ###########################

    def button_press(self):
        if self.manager.is_active():
            self.manager.stop()
            self.input_box.config(state=tk.NORMAL)
            self.stop_timer()
            self.button.config(text="Start")
        else:
            self.box.refresh_box([])
            self.chat.refresh_box([])
            self.input_box.config(state=tk.DISABLED)
            self.manager.start(self.event_handler, self.input_box.get())
            self.start_timer()
            self.button.config(text="Stop")

    # Event handling
    #   Handle events to pass back to the GUI from the manager
    #   Pass event_handler to the manager.start method as the listener
    #   Events are functions that accept a single parameter "payload".
    #       Working on the structure of things still, but currently some
    #       gui components (NameBox, InfoBar) have an 'update' function
    #       that acts as their event handler.
    #       The NameBox expects a list in the update function, while
    #       the InfoBar simply expects a string.

    def register_event(self, key, event):
        self.events[key] = event

    def event_handler(self, payload):
        for key, fn in self.events.items():
            if payload[key]:
                fn(payload[key])

    def send_to_channel(self, send, channel):
        command = {
            'type': 'send_to_channel',
            'data': {
                'send': send,
                'channel': channel
            }
        }
        self.manager.send_command_to_bot(command)
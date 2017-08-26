#!/usr/bin/python

from Tkinter import *
import tkMessageBox
import time
import datetime
import math

from namebox import Namebox


class Gui(object):

    def __init__(self, manager=None):
        self.manager = manager

        self.root = Tk()
        self.root.title("Twitch Bot")

        #Channel input
        self.input_box = Entry(self.root)
        self.input_box.grid(row=0, column=0, sticky='nsew')

        #Start/stop button
        self.button = Button(self.root, text="Start", command=self.button_press)
        self.button.grid(ipady=5, ipadx=20, row=1, column=0, sticky='nsew')

        #Timer
        self.run_timer = False
        self.timer = Label(self.root, font=('arial', 12, ''), bg='white')
        self.timer.grid(ipady=5, ipadx=5, row=0, rowspan=2, column=1, columnspan=2, sticky='nsew')

        #Scrollbar
        self.scrollbar = Scrollbar(self.root)
        self.scrollbar.grid(row=2, column=2, sticky='nsew')

        #Namebox
        self.box = Namebox(self.root)
        for name in ["Alice", "Bob", "Cindy", "David", "Erich"]:
            self.box.insert(0, name)
        self.box.grid(ipady=6, ipadx=6, row=2, column=0, columnspan=2, sticky='nsew')

        #Set Scrollbar to namebox
        self.box.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.box.yview)

        # Set event protocol handlers
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        #It's go time boys
        self.root.mainloop()

    ###########################
    # Protocol handlers
    ###########################

    def on_close(self):
        if self.manager.is_active():
            if tkMessageBox.askokcancel("Quit", "IRC Bot is running and will be disconnected.\nAre you sure you want to quit?"):
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
            self.input_box.config(state=NORMAL)
            self.stop_timer()
            self.button.config(text="Start")
        else:
            self.box.refreshBox([])
            self.input_box.config(state=DISABLED)
            self.manager.start(self.box.refreshBox, self.input_box.get())
            self.start_timer()
            self.button.config(text="Stop")

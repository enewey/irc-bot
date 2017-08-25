#!/usr/bin/python

import Tkinter
import tkMessageBox
import time
import math

from namebox import Namebox


class Gui(object):

    def __init__(self, manager=None):
        self.manager = manager

        self.root = Tkinter.Tk()
        self.root.title("IRC Bot")

        self.box = Namebox(self.root)
        for name in ["Alice", "Bob", "Cindy", "David", "Erich"]:
            self.box.insert(0, name)
        self.box.grid(ipady=6, ipadx=6, row=1, column=0, sticky='nsew')
        self.box.resize()

        self.button = Tkinter.Button(self.root, text="Start", command=self.button_press)
        self.button.grid(ipady=20, ipadx=20, row=0, column=0, sticky='nsew')

        self.run_timer = False
        self.timer = Tkinter.Label(self.root, font=('arial', 12, ''), bg='white')
        self.timer.grid(ipady=5, ipadx=5, row=0, column=1, sticky='nsew')

        # Set event protocol handlers
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.root.mainloop()

    def tick(self):
        secs = math.floor(time.time() - self.starttime)
        if self.uptime != secs:
            self.uptime = secs
            self.timer.config(text=int(self.uptime))
        
        if self.run_timer:
            self.timer.after(200, self.tick)

    def stop_timer(self):
        self.run_timer = False

    def start_timer(self):
        self.starttime = time.time()
        self.uptime = time.time()
        self.run_timer = True
        self.tick()

    def button_press(self):
        if self.manager.is_active():
            self.manager.stop()
            self.stop_timer()
            self.button.config(text="Start")
        else:
            self.box.refreshBox([])
            self.manager.start(self.box.refreshBox)
            self.start_timer()
            self.button.config(text="Stop")

    def on_close(self):
        if self.manager.is_active():
            if tkMessageBox.askokcancel("Quit", "IRC Bot is running and will be disconnected.\nAre you sure you want to quit?"):
                self.manager.stop()
                self.root.destroy()
        else:
            self.root.destroy()

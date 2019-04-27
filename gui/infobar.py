import tkinter as tk

class InfoBar(tk.Label):

    update_event = 'info'

    def update(self, payload):
        self.config(text='Unique chatters: %i' % payload)

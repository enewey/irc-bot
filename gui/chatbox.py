import tkinter as tk

class Chatbox(tk.Listbox):

    update_event = 'chat'

    def refreshBox(self, log):
        self.delete(0, self.size())
        if len(log) > 10:
            log = log[len(log)-10:]
        self.insert(0, *log)

    def update(self, payload):
        self.refreshBox(payload)

    def resize(self):
        if self.cget('height') < self.size():
            self.config(height=self.size())

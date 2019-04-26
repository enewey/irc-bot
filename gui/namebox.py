import tkinter as tk

class Namebox(tk.Listbox):

    update_event = 'names'

    def refreshBox(self, names):
        self.delete(0, self.size())
        self.insert(0, *names)

    def update(self, payload):
        self.refreshBox(payload)

    def resize(self):
        if self.cget('height') < self.size():
            self.config(height=self.size())

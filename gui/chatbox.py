import tkinter as tk

def format_line(line):
    if str.find(line, "\n") > -1:
        sp = line.split("\n")
        return "\n  ".join(map(format_line, sp))
    elif len(line) > 100:
        return line[:100] + "\n  " + format_line(line[100:])
    
    return line

class Chatbox(tk.Label):

    update_event = 'chat'

    def refresh_box(self, log):
        self.config(text="\n".join(
            map(format_line, log)
        ))

    def update(self, payload):
        self.refresh_box(payload)

    def resize(self):
        if self.cget('height') < self.size():
            self.config(height=self.size())

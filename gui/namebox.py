import Tkinter

class Namebox(Tkinter.Listbox):

    def refreshBox(self, names):
        self.delete(0, self.size())
        for name in names:
            self.insert(0, name)
        self.resize()

    def resize(self):
        if self.cget('height') < self.size():
            self.config(height=self.size())

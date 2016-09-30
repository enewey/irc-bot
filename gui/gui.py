#!/usr/bin/python

import Tkinter
from namebox import Namebox

class Gui(object):

	def __init__(self, manager=None):
		self.manager = manager

		root = Tkinter.Tk()
		root.title("IRC Bot")

		self.box = Namebox(root)
		for name in ["Alice","Bob","Cindy","David","Erich"]:
			self.box.insert(0,name)
		self.box.grid(ipady=6, ipadx=6, row=1, column=0, sticky='nsew')
		self.box.resize()

		self.button = Tkinter.Button(root, text="Start", command=self.button_press)
		self.button.grid(ipady=20, ipadx=20, row=0, column=0, sticky='nsew')

		root.mainloop()

	def button_press(self):
		if self.manager.isActive():
			self.manager.stop()
			self.button.config(text = "Start")
		else:
			self.box.refreshBox([])
			self.manager.start(self.box.refreshBox)
			self.button.config(text = "Stop")


	




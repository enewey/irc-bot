#!/usr/bin/python

import Tkinter
from namebox import Namebox

class Gui(object):
	def __init__(self, manager=None):
		self.manager = manager

		root = Tkinter.Tk()
		self.box = Namebox(root)
		for name in ["Alice","Bob","Cindy","David","Erich"]:
			self.box.insert(0,name)
		self.box.pack(ipady=6, ipadx=6, fill='y')

		button = Tkinter.Button(root, text="Start", command=self.button_press)
		button.pack(pady=20, padx=20, side='right')

		root.mainloop()

	def button_press(self):
		if self.manager.isActive():
			self.manager.stop()
		else:
			self.box.refreshBox([])
			self.manager.start(self.box.refreshBox)


	




#!/usr/bin/python

# import thread
import Tkinter
import threading
from client.bot import BotClient

WAIT_TIME = 60

client = BotClient()
# client.watchDuration(60)

event = threading.Event()
threading.Thread(target=client.watchEvent, args=(event,)).start()
raw_input("Hit Enter to see user list...")
event.set()

print "\n-------------------------"
print "----Users who chatted----"
print "-------------------------\n"

users = client.getUserlist()
for user in users:
	print user


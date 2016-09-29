import time
import thread
from client.bot import BotClient

WAIT_TIME = 60

client = BotClient()

startTime = time.time()
timePassed = 0
while timePassed < WAIT_TIME:
	client.watch()
	timePassed = time.time() - startTime

print "\n-------------------------"
print "----Users who chatted----"
print "-------------------------\n"

users = client.getUserlist()
for user in users:
	print user


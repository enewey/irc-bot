import sys
import socket
import string
import time
import threading

HOST="irc.chat.twitch.tv"
PORT=6667
NICK="narcodis"
IDENT="narcodis"
REALNAME="narcodis"
CHANNEL="#gamej06"
PASSWORD="oauth:sabqly3c74rjkci3denq270b8helgo"

def is_blank(str):
	return bool(not str or str.isspace())

class BotClient(object):

	def __init__(self):
		self.sock=socket.socket()
		self.sock.connect((HOST, PORT))

		if PASSWORD:
			self.sock.send("PASS %s\r\n" % PASSWORD)
		self.sock.send("NICK %s\r\n" % NICK)
		self.sock.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
		self.sock.send("JOIN %s\r\n" % CHANNEL)

		self.userlist = {}

	# this is meant to be threaded... event is a threading.Event
	def watchEvent(self, event):
		buf = ""
		while not event.isSet():
			buf = self.watch(buf)

	# watch chat for a set duration of time
	def watchDuration(self, duration=60):
		startTime = time.time()
		elapsed = 0
		buf = ""
		while elapsed < duration:
			buf = self.watch(buf)
			elapsed = time.time() - startTime

	def watch(self, buf=""):	
		buf = buf + self.sock.recv(1024)
		split = string.split(buf, '\n')
		buf = split.pop()
		
		for line in split:
			if is_blank(line):
				continue

			line = string.rstrip(line)
			sp = string.split(line)

			if sp[0]=='PING':
				res = format("PONG %s\r\n" % sp[1])
				self.sock.send(res)
				print string.rstrip(res)

			elif sp[1] == 'PRIVMSG':
				user = string.split(sp[0], '!')
				user[0] = user[0][1:]
				self.userlist[user[0]] = True # track users chatting
				msg = string.split(line, ':') # lines are prefixed with a colon, so first item will be a blank string
				print format("[%s %s (%s)]: %s" % (sp[2], user[0], user[1], msg[2]))

			else:
				print line

		return buf

	def sendToChannel(self, send="", channel=CHANNEL):
		if is_blank(send):
			return
		self.sock.sendall("PRIVMSG %s :%s\r\n" % (channel, send))

	def sendToUser(self, send="", user=NICK):
		if is_blank(send):
			return
		self.sock.sendall("PRIVMSG %s :%s\r\n" % (user, send))

	def getUserlist(self):
		return self.userlist

# sock=connect()
# thread.start_new_thread(recv, (sock,))
#thread.start_new_thread( chat,  ( sock, ) )

# chat(sock)

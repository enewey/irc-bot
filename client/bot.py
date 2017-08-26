import socket
import string
import time

HOST="irc.chat.twitch.tv"
PORT=6667
NICK="narcodis"
IDENT="narcodis"
REALNAME="narcodis"
CHANNEL="#day9tv"
PASSWORD="oauth:sabqly3c74rjkci3denq270b8helgo"

def is_blank(str):
    return bool(not str or str.isspace())

class BotClient(object):

    def __init__(self, listener=None):
        self.listener = listener
        self.userlist = {}

    def connect(self, channel):
        self.sock = socket.socket()
        self.sock.connect((HOST, PORT))

        if PASSWORD:
            self.sock.send("PASS %s\r\n" % PASSWORD)
        self.sock.send("NICK %s\r\n" % NICK)
        self.sock.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
        if is_blank(channel):
            channel = CHANNEL
        if not channel.startswith("#"):
            channel = "#" + channel
        self.sock.send("JOIN %s\r\n" % channel)

        return self

    # this is meant to be threaded... event is a threading.Event
    def watch_event(self, event):
        buf = ""
        while not event.isSet():
            buf = self.watch(buf)

    # watch chat for a set duration of time
    def watch_duration(self, duration=60):
        start_time = time.time()
        elapsed = 0
        buf = ""
        while elapsed < duration:
            buf = self.watch(buf)
            elapsed = time.time() - start_time

    def watch(self, buf=""):
        buf = buf + self.sock.recv(1024)
        split = string.split(buf, '\n')
        buf = split.pop()

        for line in split:
            if is_blank(line):
                continue

            line = line.rstrip()
            sp = line.split()

            if sp[0] == 'PING':
                res = format("PONG %s\r\n" % sp[1])
                self.sock.send(res)
                print string.rstrip(res)

            elif sp[1] == 'PRIVMSG':
                user = string.split(sp[0], '!')
                user[0] = user[0][1:]
                self.updateUserlist(user[0]) # track users chatting
                msg = string.split(line, ':') # lines are prefixed with a colon,first item is blank string
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

    def updateUserlist(self, name):
        self.userlist[name] = True
        self.listener(self.userlist)

    def getUserlist(self):
        return self.userlist

    def exit(self):
        self.sock.shutdown(socket.SHUT_WR)
        self.sock.close()
        print "Client exited successfully"

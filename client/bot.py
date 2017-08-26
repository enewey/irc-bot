import socket
import string
import time

def is_blank(str):
    return bool(not str or str.isspace())

class BotClient(object):

    def __init__(self, config=None, listener=None):
        self.listener = listener
        self.userlist = {}
        self.config = config

    def connect(self, channel):
        nick = self.config.user
        ident = self.config.user
        realname = self.config.user
        host = self.config.host
        port = self.config.port
        chan = self.config.channel
        password = self.config.token

        #Open socket and connect to server
        self.sock = socket.socket()
        self.sock.connect((host, port))

        #Identify
        if password:
            self.sock.send("PASS %s\r\n" % password)
        self.sock.send("NICK %s\r\n" % nick)
        self.sock.send("USER %s %s bla :%s\r\n" % (ident, host, realname))

        #Join channel
        if is_blank(channel):
            channel = chan
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

    def sendToChannel(self, send="", channel="#admin"):
        if is_blank(send):
            return
        self.sock.sendall("PRIVMSG %s :%s\r\n" % (channel, send))

    def sendToUser(self, send="", user="admin"):
        if is_blank(send):
            return
        self.sock.sendall("PRIVMSG %s :%s\r\n" % (user, send))

    def updateUserlist(self, name):
        self.userlist[name] = True
        if self.listener is not None:
            self.listener_event()
    
    def listener_event(self):
        payload = {
            'info': len(self.userlist),
            'names': self.userlist
        }
        self.listener(payload)

    def getUserlist(self):
        return self.userlist

    def exit(self):
        self.sock.shutdown(socket.SHUT_WR)
        self.sock.close()
        print "Client exited successfully"

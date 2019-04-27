import socket
import time

def is_blank(str):
    return bool(not str or str.isspace())

class BotClient(object):

    def __init__(self, config=None, listener=None):
        self.listener = listener
        self.userlist = {}
        self.chat = []
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
            self.sock.send(("PASS %s\r\n" % password).encode())
        self.sock.send(("NICK %s\r\n" % nick).encode())
        self.sock.send(("USER %s %s bla :%s\r\n" % 
            (ident, host, realname)).encode()
        )

        #Join channel
        if is_blank(channel):
            channel = chan
        if not channel.startswith("#"):
            channel = "#" + channel
        self.sock.send(("JOIN %s\r\n" % channel).encode())

        return self

    # this is meant to be threaded... event is a threading.Event
    def watch_event(self, event):
        buf = b''
        while not event.isSet():
            buf = self.watch(buf)

    # watch chat for a set duration of time
    def watch_duration(self, duration=60):
        start_time = time.time()
        elapsed = 0
        buf = b''
        while elapsed < duration:
            buf = self.watch(buf)
            elapsed = time.time() - start_time

    def watch(self, buf=b''):
        try:
            buf = buf + self.sock.recv(1024)
        except OSError as err:
            # Socket closed while receiving buf, ignore
            if "[Errno 9]" in str(err):
                return
            else:
                raise err

        split = str.split(buf.decode(), '\n')
        buf = split.pop().encode()

        for line in split:
            if is_blank(line):
                continue

            line = line.rstrip()
            sp = line.split()
            cmd = sp[1]

            if cmd == 'PING':
                res = format("PONG %s\r\n" % sp[1])
                self.sock.send(res.encode())
                print(str.rstrip(res))

            elif cmd == 'PRIVMSG':
                channel = sp[2]
                user = str.split(sp[0], '!')
                username = user[0][1:]
                useraddr = user[1]
                self.updateUserlist(username) # track users chatting
                # lines are prefixed with a colon,first item is blank string
                msg = str.split(line, ':')[2]
                chatmsg = format("\033[1;32m[%s %s (%s)]:\033[0;37m %s" % 
                        (channel, username, useraddr, msg)
                    )
                self.updateChat(chatmsg)

            else:
                print("\033[0;31m%s\033[0;37m" % line)
        return buf

    def sendToChannel(self, send="", channel="#admin"):
        if is_blank(send):
            return
        self.sock.sendall(("PRIVMSG %s :%s\r\n" % (channel, send)).encode())

    def sendToUser(self, send="", user="admin"):
        if is_blank(send):
            return
        self.sock.sendall(("PRIVMSG %s :%s\r\n" % (user, send)).encode())

    def updateUserlist(self, name):
        self.userlist[name] = True
        if self.listener is not None:
            self.listener_event()

    def updateChat(self, msg):
        self.chat.append(msg)
        if self.listener is not None:
            self.listener_event()
    
    def listener_event(self):
        # each key in this payload corresponds to an update_event
        payload = {
            'info': len(self.userlist),
            'names': self.userlist,
            'chat': self.chat
        }
        self.listener(payload)

    def getUserlist(self):
        return self.userlist

    def shutdown(self):
        self.sock.shutdown(socket.SHUT_WR)
        self.sock.close()
        print("Client exited successfully")

import socket
import time
import threading

def is_blank(str):
    return bool(not str or str.isspace())

class Bot(object):

    def __init__(self, config=None, listener=None):
        self.listener = listener
        self.userlist = {}
        self.chat = []
        self.config = config
        self.command_queue = []
        # threading stuff
        self.lock = threading.Lock()
        self.event = threading.Event()
        self.active = False
    
    def is_active(self):
        return self.active

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
            self.sock.send(('PASS %s\r\n' % password).encode())
        self.sock.send(('NICK %s\r\n' % nick).encode())
        self.sock.send(('USER %s %s bla :%s\r\n' % 
            (ident, host, realname)).encode()
        )

        #Join channel
        if is_blank(channel):
            channel = chan
        if not channel.startswith('#'):
            channel = '#' + channel
        self.sock.send(('JOIN %s\r\n' % channel).encode())

        threading.Thread(
            target=self.watch_event,
            args=(self.event,)
        ).start()

        self.active = True

        return self

    def shutdown(self):
        if not self.active:
            return
        self.event.set()
        self.sock.shutdown(socket.SHUT_WR)
        self.sock.close()
        self.active = False
        print('Client exited successfully')

    #
    # Concurrent events
    #

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
            buf = buf + self.sock.recv(4096)
        except OSError as err:
            # Socket closed while receiving buf, ignore
            if '[Errno 9]' in str(err):
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

            if sp[0] == 'PING':
                res = format('PONG %s\r\n' % sp[1])
                self.sock.send(res.encode())
                print(str.rstrip(res))

            elif cmd == 'PRIVMSG':
                #channel = sp[2]
                #useraddr = user[1]
                user = str.split(sp[0], '!')
                username = user[0][1:]
                self.update_userlist(username) # track users chatting
                # lines are prefixed with a colon, first item is blank string
                # msg could contain ':', of course, so join with that.
                msg = ':'.join(str.split(line, ':')[2:])
                # need to filter out 0x10000+ characters, as per Tcl
                self.update_chat(username, msg)

            else:
                print('\033[0;31m%s\033[0;37m' % line)
        return buf
    
    #
    # Event emitter
    #

    def listener_event(self):
        if self.listener is None:
            return
        # each key in this payload corresponds to an update_event
        payload = {
            'info': len(self.userlist),
            'names': self.userlist,
            'chat': self.chat
        }
        self.listener(payload)

    #
    # Bot state management
    # Every time internal state of the bot is updated, the listener_event is
    #   called. In practice, this listener_event is provided by the GUI, and
    #   updates the GUI to reflect the state of the bot 
    #   (update chat window, etc)
    #

    # the userlist is an internal state that keeps track of all the
    #   UNIQUE chatters on the connected channel.
    def update_userlist(self, name):
        self.userlist[name] = True
        self.listener_event()

    # 'chat' is the internal state of the chat log. basically a big list
    #   that is human readable.
    def update_chat(self, username, msg):
        msg = ''.join(c for c in msg if len(c.encode('utf-8')) < 4)
        msg = format('[%s]: %s' % (username, msg))
        
        self.chat.append(msg)
        self.listener_event()

    #
    # Command processing
    # 'Commands' stem from user input (from the GUI), or in response to
    #   messages observed in the current IRC channel (not implemented yet)
    #

    def receive(self, command):
        if not self.active:
            return
        self.queue_command(command)

    def queue_command(self, command):
        self.lock.acquire(blocking=True)
        self.command_queue.append(command)
        self.lock.release()
        self.process_queue()
    
    def process_queue(self):
        self.lock.acquire(blocking=True)
        while len(self.command_queue) > 0:
            self.process_command(self.command_queue.pop(0))
        self.lock.release()
    
    def empty_queue(self):
        self.lock.acquire(blocking=True)
        self.command_queue = []
        self.lock.release()

    # command = { type: 'string', data: {} }
    def process_command(self, command):
        typ = command['type']
        data = command['data']
        if typ == 'send_to_channel':
            send = data['send']
            channel = data['channel']
            self.send_to_channel(send, channel)
            self.update_chat(self.config.user, send)
        elif typ == 'send_to_user':
            send = data['send']
            user = data['user']
            self.send_to_user(send, user)
        else:
            print('unknown command processed %s' % typ)
    
    #
    # Command handlers
    #

    def send_to_channel(self, send='', channel='#admin'):
        if is_blank(send):
            return
        self.sock.sendall(('PRIVMSG %s :%s\r\n' % (channel, send)).encode())

    def send_to_user(self, send='', user='admin'):
        if is_blank(send):
            return
        self.sock.sendall(('PRIVMSG %s :%s\r\n' % (user, send)).encode())


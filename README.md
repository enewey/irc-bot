# Basic Twitch IRC Bot

This is an ongoing toy project. Written for Python 3.7.x

Bottom line, the goal of this project is to make something which satisfies the following (in order of importance to me):
1. Fun
2. Neat
3. Written in Python
4. Marginally useful

### Usage and setup

Currently, this "bot". given a username/token from the Twitch API, can connect to a Twitch streamer's chat. You can also send messages through the GUI.

To run this bot, create a file called `.env` that contains all your desired configuration in the top-level directory of this project.
Example:
```
BOT_GUI_FONT=PT Mono
BOT_HOST=irc.chat.twitch.tv
BOT_PORT=6667
BOT_USER=your_username_here
BOT_TOKEN=oauth:your_crazy_oauth_token
BOT_CHANNEL=\#gamesdonequick
```

Then in that same directory, run `make`.

Observe the chat messages pour in! And send your own!

**Pretty Cool, Right?**

### On the Horizon

Eventually, I want to have the bot read and write messages automatically based upon some configuration.
For example, if someone were to type in "!hello" in chat, the bot might respond "Hey, how are you {username}?".
Still working on all that, of course.

This project involves some GUI programming using **Tkinter**, some raw sockets, and some threading.
It also respects the IRC protocol, partially.

Feel free to field me comments or issues or anything. This is purely for fun.

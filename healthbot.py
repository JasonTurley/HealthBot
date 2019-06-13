# healthbot.py

from constants import *
from socket import *
import re

class HealthBot:
        def __init__(self):
                """Initialize HealthBot object """
                self.irc = socket()

        def start(self):
                """Starts server and listen methods """
                self._setup_socket()
                self._listen()

        def send_encoded(self, message : str):
                """utf-8 wrapper for socket.send() """
                self.irc.send((message).encode("utf-8"))

        def recv_decoded(self, size : int):
                """utf-8 wrapper for socket.recv() """
                return self.irc.recv(size).decode("utf-8")

        def _setup_socket(self):
                """Sets up connection to Twitch server """
                print("Connecting to " + HOST + " on port " + str(PORT) + "...")

                self.irc.connect((HOST, PORT))

                self.send_encoded("PASS " + PASS + CARRIAGE_RETURN)
                self.send_encoded("NICK " + NICK + CARRIAGE_RETURN)
                self.send_encoded("JOIN #" + CHAN + CARRIAGE_RETURN)

                print("Successfully connected.")

        def _listen(self):
                """Listens for incoming chat messages """
                # TODO Clean up code
                while True:
                        response = self.recv_decoded(BUF_SIZE)

                        # If server sends a ping keep-alive message, respond with pong
                        if "PING" in response:
                                response = response.replace("PING", "PONG")
                                send_encoded(response)

                        # Check if command is entered in chat, otherwise ignore message
                        else:
                                username = re.search(r"\w+", response).group(0)
                                message = CHAT_MSG.sub("", response)

                                if message[0] == "!":
                                        cmd = message[1:].rstrip()
                                        self.exec_command(cmd)

        def send_privmsg(self, msg : str):
                """Constructs and sends a message to chat """
                privmsg = "PRIVMSG #" + CHAN + " :" + msg + CARRIAGE_RETURN
                self.send_encoded(privmsg)

        def exec_command(self, cmd : str):
                """Executes valid health bot commands """
                # TODO: read commands from database

                print("received command: " + cmd)

# healthbot.py

from config import *
from socket import *

BUF_SIZE = (1024)

class HealthBot:
        def __init__(self):
                """Initialize HealthBot object """
                self.irc = socket()

        def start(self):
                """Starts server and listen methods """
                self._setup_socket()
                self._listen()

        def send_encoded(self, message):
                """utf-8 wrapper for socket.send() """
                self.irc.send((message).encode("utf-8"))

        #def _recv_decoded(self):
        #        return

        def _setup_socket(self):
                """Sets up connection to Twitch server """
                print("Connecting to " + HOST + " on port " + str(PORT) + "...")

                self.irc.connect((HOST, PORT))

                self.send_encoded("PASS " + PASS + "\r\n")
                self.send_encoded("NICK " + NICK + "\r\n")
                self.send_encoded("JOIN #" + CHAN + "\r\n")

                print("Successfully connected.")

        def _listen(self):
                """Listens for incoming chat messages """
                while True:
                        response = self.irc.recv(BUF_SIZE).decode("utf-8")

                        if "PING" in response:
                                response = response.replace("PING", "PONG")
                                send_encoded(response)
                        else:
                                print(response)


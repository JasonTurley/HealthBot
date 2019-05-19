'''
health_bot.py - Twitch bot that promotes health and wellness by informing gamers
		with video games related health issues and facts.

@author Jason Turley
@date 19 May 2019 

Reference: user://github.com/twitchdev/chat-samples/blob/master/python/chatbot.py 
'''

import sys
import irc.bot
import requests
import signal
import random

class TwitchBot(irc.bot.SingleServerIRCBot):
	def __init__(self, username, client_id, token, channel):
        	self.client_id = client_id
        	self.token = token
        	self.channel = '#' + channel

        	# Get the channel id, we will need this for v5 API calls
        	url = 'https://api.twitch.tv/kraken/users?login=' + channel
        	headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        	r = requests.get(url, headers=headers).json()
        	self.channel_id = r['users'][0]['_id']

        	# Create IRC bot connection
        	server = 'irc.chat.twitch.tv'
        	port = 6667
        	print ('Connecting to ' + server + ' on port ' + str(port) + '...')
        	irc.bot.SingleServerIRCBot.__init__(self, [(server, port, token)], username, username)
        
	def on_welcome(self, c, e):
        	print ('Joining ' + self.channel)

        	# You must request specific capabilities before you can use them
        	c.cap('REQ', ':twitch.tv/membership')
        	c.cap('REQ', ':twitch.tv/tags')
        	c.cap('REQ', ':twitch.tv/commands')
        	c.join(self.channel)

	def on_pubmsg(self, c, e):

        	# If a chat message starts with an exclamation point, try to run it as a command
        	if e.arguments[0][:1] == '!':
            		cmd = e.arguments[0].split(' ')[0][1:]
            		print ('Received command: ' + cmd)
            		self.do_command(e, cmd)
        	return

	def do_command(self, e, cmd):
		c = self.connection

		# Print health bot instructions
		if cmd == "help":
			print_usage(c, self.channel)

		# Display misc. health facts
		elif cmd == "health":
			print_health_facts(c, self.channel)

		# Display sight information
		elif cmd == "sight":
			print_sight_facts(c, self.channel)

		elif cmd == "bacon":
			c.privmsg(self.channel, "Delicious!")
        	# The command was not recognized
		else:
			c.privmsg(self.channel, "Did not understand command: " + cmd)

# Helper functions

def get_rand_idx(size):
	"""
	Returns an index from the list at random.
	Keyword Arguments:
	size -- the length of the list
	"""
	return random.randint(0, size-1)

def signal_handler(signum, frame):
	"""
	Signal handler
	Keyword Arguments:
	signum -- the signal number
	frame  -- ?
	"""
	print("Signal handler called with signal", signum)
	sys.exit(0)

# Health functions

def print_usage(c, channel):
	"""
	Explains what health bot is
	c 	-- bot connection
	channel -- Twitch channel
	"""
	msg = "health bot provides health and wellness information to encourage users to live happy, healthy lives!"

	c.privmsg(channel, msg)

def print_health_facts(c, channel):
	"""
	Prints health related facts
	c 	-- bot connection
	channel -- Twitch channel
	"""
	health_list = [
		"Many people neglect their posture when sitting. Yoga and pilates are great ways to fix posture and strengthen your core!",
		"15-20 minutes of sunlight provides your body with a daily dose of vitamin D. Don't forget to apply sunscreen!"
	]

	idx = get_rand_idx(len(health_list))
	msg = health_list[idx]

	c.privmsg(channel, msg)

	
def print_sight_facts(c, channel):
	"""
	Prints sight related facts
	c 	-- bot connection
	channel -- Twitch channel
	"""
	sight_list = [
		"Long gameplay sessions can lead to dry eyes, headaches, eye pain, sensitivity to light, and difficulty focusing",
		"20-20-20 Rule: look away from your computer screen every 20 minutes at a spot 20 feet away for 20 seconds.",
		"Properly set the brightness and contrast settings to minimize fatigue."
	]

	idx = get_rand_idx(len(sight_list))
	msg = sight_list[idx]

	c.privmsg(channel, msg)


def main():
	# hardcoded values
	username = "turleybots"
	client_id = "g3khmxokq0d71bs5t9axp35wxalydb"
	token = "oauth:qojwosx8qknog15ahiwp5bvvjqlow7"
	channel = "turleybots"

	signal.signal(signal.SIGINT, signal_handler)

	bot = TwitchBot(username, client_id, token, channel)
	bot.start()

	signal.pause()

if __name__ == "__main__":
	main()

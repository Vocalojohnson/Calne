# CalneBot

# Constantly monitors its own feed.
# If someone tweets to it using the bots handle, it will take the next parameter as a command and the ones after as parameters
# and replies to the original tweet with something.

import sys
from twython import Twython
from twython import TwythonStreamer

import CalneModules

from config import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET, TWITTER_HANDLE

twit = Twython(TWITTER_CONSUMER_KEY,TWITTER_CONSUMER_SECRET,TWITTER_ACCESS_KEY,TWITTER_ACCESS_SECRET) #access twitter REST api

handle=TWITTER_HANDLE.lower()


class MyStreamer(TwythonStreamer): #create a stream class
    def on_success(self, data): #when it finds a hit (when mentioned)
    	print 'Stream Connected'
        if 'text' in data: #if the hit has text
			tID = data['id_str'] #pull out the tweet ID
			user = data['user']['screen_name'] #pull out the username
			word = data['text'].encode('utf-8').split() #pull out the tweet and splits it at spaces.
			print word
			if word[0].lower() == handle: #if it starts with bots handle (not case sensitive)
				command = word[1].lower() #pull command (not case sensitive)
				params = word[2:] #pull parameters (case sensitive)
				reply = '@'+user + '\n' #prep reply
				
			#DO THE THING
				
				if command == "weather": #if weather command
					reply += CalneModules.getWeather(params[0]) #create tweet with location	
				elif command == "poem":
					reply += CalneModules.getPoem(params) #make poem using phrase
				elif command == "8ball":
					reply += CalneModules.eightball() #Explore the mysteries of the future
				else: #if command not found
					reply += "Sorry, I don't know '"+command+"' yet :(" #apologise
					
				twit.update_status(status=reply, in_reply_to_status_id=tID) #post tweet as reply to user
    def on_error(self, status_code, data):
        print status_code

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()
        
        
stream = MyStreamer(TWITTER_CONSUMER_KEY,TWITTER_CONSUMER_SECRET,TWITTER_ACCESS_KEY,TWITTER_ACCESS_SECRET) #access twitter STREAM api
stream.user() #read user stream
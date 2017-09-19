# CalneBot Modules

import sys
import pyowm
from config import OWM_API_KEY

owm = pyowm.OWM(OWM_API_KEY)

###########################
def getWeather (location): #function that takes in a location and returns a string describing today and tomorrow
	###Current Observation
	observation = owm.weather_at_place(location)	#collect observation data on location
	w = observation.get_weather() #extract weather data from observation (also available: location data)
	l = observation.get_location() #extract the other info, for reasons
	temperature =  w.get_temperature(unit='celsius') #extract temperature
	temperature = str(temperature['temp']) #extract current temp
	status = w.get_detailed_status() #extract status
	###Forecast
	fc = owm.daily_forecast(location, limit=1) #get just tomorrows weather
	f = fc.get_forecast() #pull forecast from forecaster object (one forecast per day)
	for weather in f: #pull weather from forecast object
		forecast = weather.get_status() #get status from weather object

	tweet = 'Its currently '+ temperature + 'C in '+ location + ' with ' + status + '\nTomorrow will probably be ' + forecast
	return tweet
###########################
def getPoem (phrase):
	from collections import defaultdict
	import random

	words = open("dictionary.txt").read().splitlines()
	print(max(len(x) for x in words))

	def add(a, b): #function to add letter counts to tally
		return tuple(x+y for x, y in zip(a, b))

	def over(a, b): #function to check if word would would go over tally
		return any(x>y for x, y in zip(a, b))

	def counts(word): #creates a tuple that shows how many times each letter appears eg a:1 b:2 c:0 etc
		count = [0]*27 #create an array for each letter
		for c in word.lower(): #for each letter (lowercase)
			if not c.islower(): #if its not a letter
				continue #go to next character
			count[ord(c)-ord('a')] += 1 #add 1 to the array index corresponding to the letter
		return tuple(count) #return a tuple of count (tuples are just lists that cant be changed later.)

	anagrams = defaultdict(list) #create a dict to hold anagrams
	by_len = defaultdict(list) #create a dict to hold anagram tuples by length
	wordlist = [] #create list to hold all words

	for word in words: #for every word in dictionary
		if len(word) <= 6: #if the word is less than 6 characters, ignore it
			continue
		count = counts(word) #create a tuple of the letter count of each word
		anagrams[count].append(word) #append the word to the anagram dict with the key being the tuple of counts
		by_len[sum(count)].append(count) #append the tuple value to the by_len dict with key being letter count.

	def recurse(target, left, curr, sentence):
		for n in range(left, 0, -1): #for n, counting down from letters left
			for count in by_len[n]: #for count in words with longest number of letters
				new = add(curr, count) #store letters used in anagram
				if over(new, target): #if this word puts the letter count over...
					continue #skip it and try the next word
				wordlist.append(anagrams[new])

	phrase = " ".join(phrase)

	if len(phrase) < 10:
		return "Phrase too short :("
	req = phrase #use phrase passed in
	count = counts(req) #get tuple of sentence

	recurse(count, sum(count), tuple([0]*27), []) #recurse using tuple, sentence length, blank tuple, blank list


	for item in wordlist: #for each item in wordlist
		if len(item) > 1: #if the item has multiple entries...
			for i in item: #then for each of those...
				wordlist.append(i) #append the word to the main list

	finallist = [] #create list to hold final selection of anagrams
	for word in wordlist: #for each item in worldlist
		if len(word) == 1: #if the item has only one entry
			if word in finallist: #and if its not in the final list already
				continue
			finallist.append(word) #add it to the final list

	finallist = finallist[:-len(set(req))+1] #remove the last few entries because theyre just the unique letters in the sentence
	if len(finallist) < 9:
		return "not enough results generated :("

	selected_words = [] #create list to hold selected words
	for i in range(0,9): #for count 9
		selected_words.append(random.choice(finallist)[0]) #save a word

	#create tweet
	tweet = selected_words[0] + ", " +  selected_words[1] + ", " + selected_words[2] + "!\n"
	tweet += selected_words[3] + ", " +  selected_words[4] + ", " + selected_words[5] + "!\n"
	tweet += selected_words[6] + ", " +  selected_words[7] + ", " + selected_words[8] + "...\n"
	tweet += "\nDeath."

	return tweet
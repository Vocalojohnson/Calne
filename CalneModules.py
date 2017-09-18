# CalneBot Modules

import sys
import pyowm
from keys import OWM_API_KEY

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

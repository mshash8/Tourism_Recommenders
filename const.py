"""
File to Maintain a List of Constant Values Used in the Backend Code

This script has three important constant values which are needed to run
the program. Firstly, the weather codes which are constant values
ranging from 1 to 27 each depicting a particular weather condition
(clear, fog, rain, snow, etc.). Secondly, the Google Maps API URL,
which helps access the data of places from the API. Lastly, the encoded
API key without which the data cannot be obtained.

"""

WEATHER_CODES = {
'1'	: 'Clear',
'2'	: 'Fair',
'3'	: 'Cloudy',
'4'	: 'Overcast',
'5'	: 'Fog',
'6'	: 'Freezing Fog',
'7'	: 'Light Rain',
'8'	: 'Rain',
'9'	: 'Heavy Rain',
'10'	: 'Freezing Rain',
'11'	: 'Heavy Freezing Rain',
'12'	: 'Sleet',
'13'	: 'Heavy Sleet',
'14'	: 'Light Snowfall',
'15'	: 'Snowfall',
'16'	: 'Heavy Snowfall',
'17'	: 'Rain Shower',
'18'	: 'Heavy Rain Shower',
'19'	: 'Sleet Shower',
'20'	: 'Heavy Sleet Shower',
'21'	: 'Snow Shower',
'22'	: 'Heavy Snow Shower',
'23'	: 'Lightning',
'24'	: 'Hail',
'25'	: 'Thunderstorm',
'26'	: 'Heavy Thunderstorm',
'27'	: 'Storm'
}

GOOGLE_MAPS_API = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

ENCODED_GOOGLE_API_KEY = "QUl6YVN5RHZYWTZ6clNETGJQX3VOQ2M3VVYxeldxb2J0a2swbDdB"

import requests
import json

url = "https://travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com/v1/prices/cheap"
url_airports = "https://travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com/data/en-GB/airports.json"

headers = {
	"X-Access-Token": "9d9e8688a3055a1857b3173854264fdf",
	"X-RapidAPI-Key": "YvFz0Cq6Osmsh7pzZhAx0ydCZ66Zp1rpoxXjsnkqkzWBiDc9Cp",
	"X-RapidAPI-Host": "travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com"
}

#Query to get the initial search results with the departure city
querystring = {"origin":"SCO","page":"None","currency":"KZT","destination":"-"}
response = requests.get(url, headers=headers, params=querystring)
response_dict = response.json()
text = json.dumps(response_dict, indent = 4, sort_keys=True)

f = open("export.json", "wt")
f.write(text)

#Query to get the list of airports
airports = requests.get(url_airports, headers=headers)
airports_dict = airports.json()
airports_text = json.dumps(airports_dict, indent = 4, sort_keys=True)

r = open("airports.json", "wt")
r.write(airports_text)

#Query to get the second round search with the selected destination place and neighbouring departure cities
querystring_2 = {"origin":"AKX","page":"None","currency":"KZT","destination":"KUT"}
response_2 = requests.get(url, headers=headers, params=querystring_2)
response_dict_2 = response_2.json()
text_2 = json.dumps(response_dict_2, indent = 4, sort_keys=True)

f = open("recom.json", "wt")
f.write(text_2)
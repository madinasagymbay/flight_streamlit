#Import requests
import requests
#Import pandas
import pandas as pd 
#Import json
import json
# Import sys dependency to extract command line arguments
import sys
# Import data processing helper
from helper import process_dep_data
# Import os
import os

#Access tokens to the API
api_token = os.getenv('X_Access_Token')
api_key = os.getenv('X_RapidAPI_Key')
api_host = os.getenv('X_RapidAPI_Host')

headers = {
	"X-Access-Token": api_token,
	"X-RapidAPI-Key": api_key,
	"X-RapidAPI-Host": api_host
}

#Request urls from the the data will be retrieved
url = "https://travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com/v1/prices/cheap"
url_airports = "https://travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com/data/en-GB/airports.json"

def get_airports():
  #Query to get the list of airports
  airports = requests.get(url_airports, headers=headers)
  airports_dict = airports.json()
  airports_text = json.dumps(airports_dict, indent = 4, sort_keys=True)
  #Export the data to JSON object
  r = open("airports.json", "wt")
  r.write(airports_text)
  #return the query results
  return airports_text

def get_flights_dep(origin, currency, range_km):
  #Query to get the initial search results with the departure city
  #querystring = {"origin":"SCO","page":"None","currency":"KZT","destination":"-"}
  querystring = {"origin":origin,"page":"None","currency":currency,"destination":"-"}
  response = requests.get(url, headers=headers, params=querystring)
  response_dict = response.json()
  text = json.dumps(response_dict, indent = 4, sort_keys=True)
  #Export the data to JSON object
  f = open("export.json", "wt")
  f.write(text)
  #Get airports data
  raw_air_data = get_airports()
  #Proces data
  process_data_df = process_dep_data(text, raw_air_data, origin, range_km)
  #return the query results
  return process_data_df



def get_flights_arr(neigh_cities, currency, selected_city):
  #Query to get the second round search with the selected destination place and neighbouring departure cities
  #querystring_2 = {"origin":"AKX","page":"None","currency":"KZT","destination":"KUT"}
  querystring_2 = {"origin":neigh_cities,"page":"None","currency":currency,"destination":selected_city}
  response_2 = requests.get(url, headers=headers, params=querystring_2)
  response_dict_2 = response_2.json()
  text_2 = json.dumps(response_dict_2, indent = 4, sort_keys=True)
  #Export the data to JSON object
  f = open("recom.json", "wt")
  f.write(text_2)
  #Get airports data
  raw_air_data = get_airports()
  #Proces data
  process_data_df = process_dep_data(text_2, raw_air_data, neigh_cities, 10)
  print("process_data_df")
  print(process_data_df)
  #return the query results
  return process_data_df

# def get_recom(dep_city, destination, currency, selected_city):
#   result_df, neigh_df = get_flights_dep(dep_city, currency, range_km=10)
#   combined_results = pd.DataFrame()

#   # Iterate over each destination
#   for destination in neigh_df['destination']:
#       result, neigh_null = get_flights_arr(destination, currency, selected_city)
#       # Add the 'destination' column to the result DataFrame
#       result.insert(1,'origin_city', destination)
#       # Append the result DataFrame to the combined_results DataFrame
#       combined_results = pd.concat([combined_results, result], ignore_index=True)
#   return combined_results



# dep_city = "SCO"
# currency = "KZT"
# range_km = 10
# selected_city = "KUT"
# # # Call the process_data function

# result_df, neigh_df = get_flights_dep(dep_city, currency, range_km = 10)
# print(neigh_df)

# def process_selected_city(selected_city, neigh_df, currency):
#     # Initialize an empty DataFrame to store the results
#     combined_results = pd.DataFrame()
#     # Iterate over each destination
#     for destination in neigh_df['destination']:
#         result, neigh_null = get_flights_arr(destination, currency, selected_city)
#         # Add the 'destination' column to the result DataFrame
#         result.insert(1,'origin_city', destination)
#         # Append the result DataFrame to the combined_results DataFrame
#         combined_results = pd.concat([combined_results, result], ignore_index=True)
#     return combined_results

# combined_df = process_selected_city(selected_city, neigh_df, currency)
# print(combined_df)



# # Print the resulting DataFrame
# # print(result_df)
# # print(neigh_df)

# # Initialize an empty DataFrame to store the results
# combined_results = pd.DataFrame()

# # Iterate over each destination
# for destination in neigh_df['destination']:
#     result, neigh_null = get_flights_arr(destination, currency, selected_city)
#     # Add the 'destination' column to the result DataFrame
#     result.insert(1,'origin_city', destination)
#     # Append the result DataFrame to the combined_results DataFrame
#     combined_results = pd.concat([combined_results, result], ignore_index=True)

# print(combined_results)



# if __name__ == '__main__':
#     get_flights_dep(sys.argv[1])

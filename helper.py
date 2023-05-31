#Import pandas
import pandas as pd 
#Import numpy
import numpy as np 
#Import pycountry and countryinfo for further getting full country name
import pycountry
from countryinfo import CountryInfo
#Import sqldf to write sql queries
from pandasql import sqldf
#Importing the JSON library
import json


def process_dep_data(data_json_str, airport_json_str, origin, range_km):
  # Parse the JSON string into a dictionary
  data_json = json.loads(data_json_str)
  airport_json = json.loads(airport_json_str)
  #print(type(data_json))
  #print('data_json:', data_json)
  selected_city = origin
  #Create the dataframe with the columns stated below
  rows = []
  for destination, flights in data_json['data'].items():
      for key, flight in flights.items():
          row = {
              'currency': data_json['currency'],
              'destination': destination,
              'airline': flight['airline'],
              'flight_num': flight['flight_number'],
              'dep_at': flight['departure_at'],
              'arr_at': flight['return_at'],
              'price': flight['price']    
          }
          rows.append(row)
  df = pd.DataFrame(rows)

  #Convert the columns 'departure_at' and 'return_at' to datetime format
  df['dep_at'] = pd.to_datetime(df['dep_at'], utc=True) 
  df['arr_at'] = pd.to_datetime(df['arr_at'], utc=True) 
  # Extract date and time components into separate columns
  df['dep_date'] = df['dep_at'].dt.date
  df['dep_time'] = df['dep_at'].dt.time
  df['arr_date'] = df['arr_at'].dt.date
  df['arr_time'] = df['arr_at'].dt.time
  # Drop the original datetime columns
  df.drop(columns =['dep_at', 'arr_at'], inplace=True)

  df_airports, df_neighbours = airports(airport_json, selected_city, range_km)
  #Merge two dataframes on destination column and get airport_name and country_code columns
  df = df.merge(df_airports, on='destination', how='left')
  # Function to get full country name using pycountry library
  def get_country_name(code):
      try:
          country = pycountry.countries.get(alpha_2=code)
          return country.name
      except:
          return None
  #Add the full country name using the get_country_name function
  df['country_name'] = df['country_code'].apply(get_country_name)
  #print(df_neighbours)
  return df, df_neighbours

def airports(airports_json, selected_city, range_km):
  #Create the dataframe with the columns stated below
  rows_airports = []
  for a in airports_json:
      row_a = {
          'destination': a['city_code'],
          'airport_name': a['name'],
          'country_code': a['country_code'], 
          'coordinates': a['coordinates']
      }
      rows_airports.append(row_a)
  df_airports = pd.DataFrame(rows_airports)

  # Split the coordinates column into latitude and longitude
  df_airports['latitude'] = df_airports['coordinates'].apply(lambda x: x['lat'])
  df_airports['longitude'] = df_airports['coordinates'].apply(lambda x: x['lon'])
  #Drop coordinates column
  df_airports = df_airports.drop(columns = 'coordinates')

  # SQL query
  query = "WITH sel_country AS (SELECT * FROM df_airports WHERE destination = '{}') " \
          "SELECT b.*, ABS(a.latitude - b.latitude) AS diff_lat, ABS(a.longitude - b.longitude) AS diff_lon " \
          "FROM df_airports b JOIN sel_country a ON a.country_code = b.country_code " \
          "WHERE diff_lat < {} AND diff_lon < {}".format(selected_city, range_km, range_km)  # Execute the query
  neighb_cities = sqldf(query, locals())

  def get_continent_name(country_code):
    try:
        country = CountryInfo(country_code)
        return country.region()
    except KeyError:
        pass
    return None

  neighb_cities['continent'] = neighb_cities['country_code'].apply(get_continent_name)

  return df_airports, neighb_cities
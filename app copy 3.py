# Import base streamlit dependency
import streamlit as st
# Import pandas to load the analytics data
import pandas as pd
# Import subprocess to run tiktok script from command line
from subprocess import call
# Import plotly for viz
import plotly.express as px
# Import data processing helper
from flights import get_flights_dep
from flights import get_flights_arr

# Set page width to wide
st.set_page_config(layout='wide')

# Create sidebar
st.sidebar.markdown("<div><img src='https://storage.googleapis.com/blogs-images/ciscoblogs/1/2021/10/Predictive-analytics-2-300x300.png' width=100 /><h1 style='display:inline-block'>Flight Analytics</h1></div>", unsafe_allow_html=True)
st.sidebar.markdown("This dashboard allows to find the cheapest flights from selected location with free departure date: Made using Python and Streamlit.")
st.sidebar.markdown("To get started <ol><li>Enter the <i><b>departure city, currency, range in km</b></i> to find even cheaper flights tickets from neighbouring cities in your country</li> <li>Hit <i><b>Get Data</b></i></li> <li>Get your results 🥳</li></ol>",unsafe_allow_html=True)

# Input 
dep_city = st.text_input('Insert your departure city', value="")
currency = st.selectbox('Pick the currency', ['KZT', 'USD', 'GBP'])
st.markdown('If you would like to get even cheaper prices with the departure city close to your location, go to "Neighbouring cities analysis"')
st.markdown('Select the range in km (default 10 km) from your location and you will get the closest neighbouring cities')
range_km = st.number_input('Pick a range in km', 0, 20)
# Call the process_data function
df, neigh_df = get_flights_dep(dep_city, currency, 10) 

# Button
if st.button('Get Data'):
  # Plot the bar chart
  mean_prices = df.groupby('airport_name')['price'].mean().round(2).reset_index()
  mean_prices = mean_prices.merge(df[['airport_name', 'country_name']], on='airport_name')
  mean_prices = mean_prices.drop_duplicates(subset=['airport_name'])
  fig1 = px.bar(mean_prices, x='airport_name', y='price', color='country_name', orientation='v',
        title='Departures per Airport Grouped by Country',
        labels={'price': 'Average price', 'airport_name': 'Destination'})
  st.plotly_chart(fig1, use_container_width=True)
  # Plot the scatter plot
  fig2 = px.scatter(df, x='dep_date', y='price', color='country_name',
                 title='Departures: Price vs Departure Date',
                 labels={'dep_date': 'Departure Date', 'price': 'Price'},
                 hover_data=['airport_name'],
                 size='price')
  st.plotly_chart(fig2, use_container_width=True)

  #Default range is 10 km, otherwise selected range
  if range_km == 0:
    df, neigh_df = get_flights_dep(dep_city, currency, 10)
  else: 
    df, neigh_df = get_flights_dep(dep_city, currency, range_km)

  # Plotly map visualization here
  fig3 = px.scatter_geo(neigh_df, lat='latitude', lon='longitude', hover_name='airport_name',
                    hover_data=['country_code'], projection='natural earth', 
                    title='Neighbouring cities',
                    scope=neigh_df['continent'].unique()[0].lower())
  st.plotly_chart(fig3, use_container_width=True)

  st.markdown('Did you select where to go?')
  # Define the list of options for the dropdown menu
  options = df['airport_name']
  # Create a dropdown menu and store the selected option
  selected_city = st.selectbox('Select your arrival city', options)
  recom_df = update_results(selected_city)
  recom_df


def update_results(selected_city):
  # Initialize an empty DataFrame to store the results
  combined_results = pd.DataFrame()
  # Iterate over each destination
  for destination in neigh_df['destination']:
      result, neigh_null = get_flights_arr(destination, currency, selected_city)
      # Add the 'destination' column to the result DataFrame
      result.insert(1,'origin_city', destination)
      # Append the result DataFrame to the combined_results DataFrame
      combined_results = pd.concat([combined_results, result], ignore_index=True)
  return combined_results


  # # Split columns
  # left_col, right_col = st.columns(2)

  # # First Chart - video stats
  # scatter1 = px.scatter(df, x='stats_shareCount', y='stats_commentCount', hover_data=['desc'], size='stats_playCount', color='stats_playCount')
  # left_col.plotly_chart(scatter1, use_container_width=True)

    # # Second Chart
    # scatter2 = px.scatter(df, x='authorStats_videoCount', y='authorStats_heartCount', hover_data=['author_nickname'], size='authorStats_followerCount', color='authorStats_followerCount')
    # right_col.plotly_chart(scatter2, use_container_width=True)







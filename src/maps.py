import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster
import pandas as pd


def creating_map(df, lat, lon, zoom=10):

    # Creating a map centered on the coordinates
    city_map = folium.Map(location=[lat, lon], zoom_start=zoom)
    
    data_dict={'Design company': ['pink','briefcase'],
               'Airport': ['blue', 'plane'], 
               'Preschool' : ['lightblue', 'baby-carriage'],
               'Primary and Secondary School': ['darkblue', 'graduation-cap'],
               'Train Station': ['darkred', 'train'],
               'Night Clubs': ['darkpurple', 'martini-glass'],
               'Vegan Restaurant': ['green', 'utensils'],
               'Basketball Stadium':['orange', 'basketball'],
               'Starbucks': ['cadetblue', 'mug-saucer'],
               'Dog Grooming': ['gray', 'dog']
              }
    for key, value in data_dict.items():
        data = df[df['data'] == key]
        # Iterating over the rows of the DataFrame
        for index, row in data.iterrows():
            name = row['name']
            latitude = row['latitude']
            longitude = row['longitude']

             # Creating a custom icon for the design company
            icon = folium.Icon(color=value[0], icon=value[1], prefix='fa')
    
            # Adding a marker to the map for each office
            folium.Marker([latitude, longitude], icon=icon, popup=name).add_to(city_map)

    icon = Icon (color = "red", icon_color = "white", icon = "star", prefix = "fa")
    city_location = Marker(location = [lat, lon], tooltip = "Location", icon = icon)
    city_location.add_to(city_map)

    return city_map


from getpass import getpass
from dotenv import load_dotenv
import pandas as pd
import requests
import os
import folium
import matplotlib.pyplot as plt
import seaborn as sns

def foursquare_access():
    load_dotenv()
    token = os.getenv("token")
    return token


def category_from_foursquare (lat, lon, category):
    token = foursquare_access()
    url = f"https://api.foursquare.com/v3/places/search?&ll={lon}%2C{lat}&categories={category}&sort=DISTANCE&limit=1"
    
    headers = {
        "accept": "application/json",
        "Authorization": token
    }

    response = requests.get(url, headers=headers).json()
    return response


def query_from_foursquare (query, lat, lon):
    token = foursquare_access()
    url = f"https://api.foursquare.com/v3/places/search?query={query}&ll={lon}%2C{lat}&sort=DISTANCE&limit=1"

    headers = {
        "accept": "application/json",
        "Authorization": token
    }

    response = requests.get(url, headers=headers).json()
    return response


def everything_from_foursquare (one_element, data):

    name = one_element["name"]
    lat = one_element["geocodes"]["main"]["latitude"]
    lon = one_element["geocodes"]["main"]["longitude"]
    distance = one_element["distance"]
    
    dict_ = {"name": name, "latitude": lat, "longitude": lon, "data": data, "distance": distance}
    
    return dict_


def df_foursquare(df, lat, lon, city):
    
    category_dict={"Airport": "19040", "Preschool":"12056", "Primary and Secondary School":"12057", "Train Station":"19046",
                   "Night Clubs":"10032", "Vegan Restaurant":"13377", "Basketball Stadium":"18008"}
    
    query_list=["Starbucks","Dog Grooming"]
    
        
    for key, value in category_dict.items():
        response=category_from_foursquare(lon, lat, value)
        new_list = []
        for i in response["results"]:
            new_list.append(everything_from_foursquare (i, key))

        df1 = pd.DataFrame(new_list)
        df = pd.concat([df, df1])
                
                
    for query in query_list:
        response=query_from_foursquare (query,lon, lat)
        new_list = []
        for i in response["results"]:
            new_list.append(everything_from_foursquare (i, query))

        df1 = pd.DataFrame(new_list)
        df = pd.concat([df, df1])    
    
    if city == "London":
        df.loc[len(df)] = ["Jessica's Dog Grooming", "51.5141844", "-0.1863357", "Dog Grooming", 1500.0]
    
    df['city'] = city
    
    df.reset_index(drop=True, inplace=True)
    
    return df


def best_locations_df(df_nyc, df_sf, df_lon):
    dfs = (df_nyc, df_sf, df_lon)
    cities = ["New York", "San Francisco", "London"]
    data= ["Airport", "Preschool", "Primary and Secondary School", "Train Station", "Night Clubs", "Vegan Restaurant", 
          "Basketball Stadium", "Starbucks", "Dog Grooming"]

    distance_dict= {}

    for i in data:
        distance_dict[i] = {}
        for df, city in zip(dfs, cities):
            distance_value = df.loc[df['data'] == i, 'distance'].values[0]
            distance_dict[i][city] = distance_value

    df = pd.DataFrame(distance_dict, index=["New York", "San Francisco", "London"])
    return df


def distance_locations_plot(df):

    fig, ax = plt.subplots()

    columns = [col for col in df.columns if col != 'Airport']
    values = df.loc[:, columns].values

    colors = ['#FFC107', '#FF4081', '#536DFE']  
    bar_width = 0.25 

    for i, city in enumerate(df.index):
        pos = [j + bar_width*i for j in range(len(columns))]  # Posición de las barras
        ax.bar(pos, values[i], width=bar_width, alpha=0.7, color=colors[i], label=city)

    ax.legend()
    ax.set_title('Distance between city locations and places',fontweight='bold')


    ax.set_xticks([j + bar_width for j in range(len(columns))])
    ax.set_xticklabels(columns, rotation=45, ha='right')
    ax.set_ylabel('Distance (meters)')

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)

    plt.show()


def closest_distance_points(df):
    for column in df.columns:
        sorted_values = df[column].sort_values(ascending=False)
        df[column] = df[column].apply(lambda x: 2 if x == sorted_values.iloc[0] else 1 if x == sorted_values.iloc[1] else 0)

    return df

def cities_grades_plot(df):

    grade = ((df.sum(axis=1)/18)*9).round(1)

    fig, ax = plt.subplots()

    colors = ['#FFC107', '#FF4081', '#536DFE']
    bar_width = 0.5  
    ax.bar(grade.index, grade, width=bar_width, alpha=0.7, color=colors)

    for i, val in enumerate(grade):
        ax.text(i, val -1 , str(val), ha= "center",color='black', size=14)

    ax.set_title("Best requirements count per location", fontsize=14, fontweight='bold')
    ax.set_ylabel('Requirements (8 in total)', fontsize=12)

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)

    plt.show()



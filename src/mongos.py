from pymongo import MongoClient
import pandas as pd
import time
import re
import requests
import json
from getpass import getpass
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np
import os

def mongo_access(name, collection):
    client = MongoClient("localhost:27017")
    db = client[name]
    c = db.get_collection(collection)
    return c


def mongo_design_query(c):
    condition1= {"total_money_raised": {"$regex": "[MB]$"}}
    condition2={"tag_list": {"$regex": "design"}}
    condition3={"category_code": "design"}

    query = {"$and": [condition1 ,{"$or": [condition2, condition3]}]}
    projection={"name":1, "_id":0, "total_money_raised":1, 
                "tag_list":1, "description":1, "offices":1, "category_code":1 }

    design_companies=list(c.find(query, projection).sort('offices.country_code'))
    df=pd.DataFrame(design_companies)
    return df


def cleaning_df(df):
    df['city'] = ''
    for index, row in df.iterrows():
        offices = row['offices']  
        for i in range(len(offices)):  
            city = offices[i].get('city', '')  
            df.at[index, 'city'] += (city + ' ,')
            
    df['state_code'] = ''
    for index, row in df.iterrows():
        offices = row['offices']  
        for i in range(len(offices)):  
            x = offices[i].get('state_code', '')  
            df.at[index, 'state_code'] += (str(x) + ' ,')
            
    cities_list=list(df['city'])  
    cities = [city.strip() for cities in cities_list for city in cities.split(',')]
    cities = [city for city in cities if city != '']
    
    df.to_csv("dataframes/design_companies.csv", index=False)
    return df, cities


def designers_cities_plot(cities,df):

    unique_cities, city_counts = np.unique(cities, return_counts=True)

    #Sort the cities and counts in descending order
    sorted_indices = np.argsort(city_counts)[::-1]
    unique_cities = unique_cities[sorted_indices]
    city_counts = city_counts[sorted_indices]

    #Create a bar plot
    plt.bar(unique_cities, city_counts, color='skyblue')

    #Set the labels and title
    plt.xlabel('City')
    plt.ylabel('Count')
    plt.title('Companies with Designers per City')

    #Rotate the x-axis labels for better visibility
    plt.xticks(rotation=90)

    #Adjust the layout
    plt.tight_layout()

    # Save the plot as an image and display the plot
    plt.savefig('figures/designers_cities_plot.png')
    os.system("start figures/designers_cities_plot.png")
    plt.show()



def mongo_games_query(c):

    condition1={"total_money_raised":  {"$regex": "M$"}}
    condition2={"description": {"$regex": "gam"}}
    condition3={"category_code": "games-video"}

    query = {"$and": [condition1,{"$or": [condition2, condition3]}]}
    projection={"name":1, "_id":0, "total_money_raised":1, 
                "tag_list":1, "description":1, "offices":1, "category_code":1 }

    gaming_money_raised=list(c.find(query, projection))
    
    df=pd.DataFrame(gaming_money_raised)
    return df

def cleaning_df2(df2):
    df2['currency'] = ''
    # Iterate over the rows and update the 'currency' column based on the symbols
    for index, row in df2.iterrows():
        if '€' in row['total_money_raised']:
            df2.at[index, 'currency'] = '€'
        elif '$' in row['total_money_raised']:
            df2.at[index, 'currency'] = '$'
        elif '¥' in row['total_money_raised']:
            df2.at[index, 'currency'] = '¥'
    
    # Remove non-numeric elements from the 'total_money_raised' column
    df2['total_money_raised'] = df2['total_money_raised'].str.replace(r'\D', '', regex=True)
    df2['total_money_raised'] = df2['total_money_raised'].astype(float)
    
    for index, row in df2.iterrows():
        if row["currency"] == "€":
            df2.at[index, 'total_money_raised'] *= 1.2
        elif row["currency"] == "¥":
            df2.at[index, 'total_money_raised'] *= 0.0074
    
    df2['total_money_raised'] =df2['total_money_raised'].round(1)
    df2 = df2.sort_values('total_money_raised',ascending=False)
    df2 = df2.reset_index(drop=True)
    
    df2['city'] = ''
    for index, row in df2.iterrows():
        offices = row['offices']  
        for i in range(len(offices)):  
            city = offices[i].get('city', '')  
            df2.at[index, 'city'] += (city + ' ,')
            
    df2['country_code'] = ''
    for index, row in df2.iterrows():
        offices = row['offices']  
        for i in range(len(offices)):  
            code = offices[i].get('country_code', '')  
            df2.at[index, 'country_code'] += (code + ' ')
    
    df2.to_csv("dataframes/game_companies.csv", index=False)
    
    return df2


def game_cities_df(df2):
    
    cities_list = df2[df2['total_money_raised'] >= 200]['city'].values
    
    cities = [city.strip() for cities in cities_list for city in cities.split(',')]
    cities = [city for city in cities if city != '']
    

    # Create a DataFrame from the list of cities
    df3 = pd.DataFrame({'city': cities})

    # Get the count of occurrences for each city
    city_counts = df3['city'].value_counts()

    # Create a new DataFrame with the top occurring values
    game_top_cities = pd.DataFrame({'city': city_counts.index, 'count': city_counts.values})

    # DataFrame with the top occurring values
    game_top_cities.to_csv("dataframes/game_200M_cities.csv", index=False)
    
    return game_top_cities


def game_cities_plot(game_top_cities):

    # Group cities with count 1 as 'Others'
    game_top_cities.loc[game_top_cities['count'] == 1, 'city'] = 'Others'

    # Calculate the sum of counts for each city
    city_counts = game_top_cities.groupby('city')['count'].sum()

    # Define colors for the pie slices
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6', '#c2f0f0', '#ffb3b3', '#ccff99', '#dab3ff']

    # Create a pie plot
    plt.pie(city_counts, labels=city_counts.index, autopct='%1.1f%%', colors=colors, startangle=90)

    # Add a shadow to the pie plot
    plt.gca().add_artist(plt.Circle((0, 0), 0.7, color='white'))

    # Set the aspect ratio to be equal
    plt.axis('equal')

    # Set the title and adjust the layout
    plt.title('Top count of Game Companies Offices by city and Raised Amount')
    plt.tight_layout()

     # Save the plot as an image and display the plot
    plt.savefig('figures/game_cities_plot.png')
    os.system("start figures/game_cities_plot.png")
    plt.show()


def design_gaming_df(c):

    condition={"total_money_raised":  {"$regex": "M$"}}
    condition1={"total_money_raised":  {"$regex": "[MB]$"}}
    condition2={"tag_list": {"$regex": "design"}}
    condition3={"category_code": "design"}
    condition4={"offices.city": "New York"}
    condition5={"offices.city": "London"}
    condition6={"offices.city": "San Francisco"}

    query = {"$and": [{"$or": [condition, condition1]}, {"$or": [condition4,condition5,condition6]}, {"$or": [condition2, condition3]}]}
    projection={"name":1, "_id":0, "total_money_raised":1, 
                "tag_list":1, "description":1, "offices":1, "category_code":1 }

    design_gaming_money =list(c.find(query, projection))
    
    df3=pd.DataFrame(design_gaming_money)
    
    # Define the desired cities
    desired_cities = ["New York", "London", "San Francisco"]

    # Apply the filter on the "offices" column
    df3['offices'] = df3['offices'].apply(lambda x: [office for office in x if any(city in office.get('city', '') for city in desired_cities)])

    
    return df3


def cleaning_df3(df):
    # Crear una lista para almacenar las filas adicionales
    new_rows = []

    # Recorrer el DataFrame
    for index, row in df.iterrows():
        offices = row['offices']
        if len(offices) > 1:
            # Si la lista tiene más de un diccionario, crear una nueva fila por cada diccionario
            for i in offices:
                new_row = row.copy()
                new_row['offices'] = [i]
                new_rows.append(new_row)
        else:
            # Si la lista tiene solo un diccionario, mantener la fila original
            new_rows.append(row)


    # Crear un nuevo DataFrame con las filas adicionales
    df= pd.DataFrame(new_rows)
    df.reset_index(drop=True, inplace=True)

    
    data_type=['longitude', 'latitude', 'city', 'address1', 'address2', 'state_code', 'country_code']
    
    for i in data_type:
        df[i] = ''
        for index, row in df.iterrows():
            offices = row['offices']
            for office in offices:
                x = office.get(i, '')
                df.at[index, i] += str(x)

    df = df.drop("offices", axis=1)
    
    netbiscuits_lon= '-73.93230'
    netbiscuits_lat= '40.69517'
    
    # Update the value of the "longitude" and "latitude" column
    df.loc[(df['name'] == 'Netbiscuits') & (df['state_code'] == 'NY'), 'longitude'] = netbiscuits_lon
    df.loc[(df['name'] == 'Netbiscuits') & (df['state_code'] == 'NY'), 'latitude'] = netbiscuits_lat
    
    offices_dict= {'Wix': ['-122.40507','37.75672'],
                  'Squarespace': ['-74.00087','40.72081'],
                  'Banyan Branch':['-73.93230','40.69517'],
                  'Moonfruit':['-0.11016','51.51913'],
                      }     
        
    for key, value in offices_dict.items():   
        df.loc[df['name'] == key, 'longitude'] = value[0]
        df.loc[df['name'] == key,'latitude'] = value[1]
        # Update the value of the "longitude" column

    df["data"] = "Design company"
    df.to_csv("dataframes/design_coordinates.csv", index=False)
    
    return df


def cities_dfs(df3):
    df_sf= df3[df3['city'] == 'San Francisco'][['name', 'latitude', 'longitude', 'data']].copy()
    df_sf.to_csv("dataframes/df_sanfrancisco.csv", index=False)
    
    df_nyc= df3[df3['city'] == 'New York'][['name', 'latitude', 'longitude','data']].copy()
    df_nyc.to_csv("dataframes/df_newyork.csv", index=False)
    
    df_lon= df3[df3['city'] == 'London'][['name', 'latitude', 'longitude','data']].copy()
    df_lon.to_csv("dataframes/df_london.csv", index=False)
    
    return df_sf, df_nyc, df_lon








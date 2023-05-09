# Project 2 - MONGOGAME COMPANY: Where should we locate our new office? 

![image](https://user-images.githubusercontent.com/127286755/236945195-71be2e84-1262-47f8-928b-66ad27c0d19d.png)

## Introduction

Mongo Game is a new company in the gaming industry, they want to open their first office and they are looking for the perfect place. 
All the employees were asked to show their preferences on where to place the new office, our goal is to place the new company offices in the best place for the company to grow.

- Designers like to go to design talks and share knowledge. There must be some nearby companies that also do design.
- 30% of the company staff have at least 1 child, so we want a Preeschool and Primary/Secondary school close by.
- Developers like to be near successful tech startups that have raised at least 1 Million dollars.
- Executives like Starbucks a lot.
- Account managers need to travel a lot.
- Everyone in the company is between 25 and 40, we will look for a good night club.
- The CEO is vegan, we want a vegan restaurant as close as possible.
- The maintenance guy loves basketball.
- The office dog—"Dobby" needs a hairdresser every month, we need one not too far away.

## Methods
To start the analysis we used a Mongo's database with more than 18k start ups data. Using **mongo queries and regex**, we looked for the count of design companies located in each city, so that we can locate our company in one of those cities. We also looked for the best gaming companies location, we want our office to be as close to them to follow their steps. We grouped the top 20 game companies that raised more than $200M and we created two plots to see the results:
![designers_cities_plot](https://user-images.githubusercontent.com/127286755/236945428-c8048b2d-432d-443b-bfb2-ac4c0de3ebec.png)

![game_cities_plot](https://user-images.githubusercontent.com/127286755/236945479-c5c7c2dd-6d59-452b-82c7-6714d2e9b2f2.png)

As you can see, **San Francisco, New York and London** are the cities with the most designers close by and the best gaming companies (taking into account their money raised). 
So, we started our analysis based on three locations, each located in one of the selected three cities. We used the **Foursquare API** and folium to create new data information and added it to a map of each city.
We looked for the closest Airport, Train Station, Preschool, Primary and Secondary School, Night Clubs, Vegan Restaurant, Basketball Stadium, Starbucks and Dog Grooming. And we created the maps:

### - San Francisco location: 
Near Minted (design company) that has raised $52.7M, located at 747 Front Street, close to the Embarcadero.
![image](https://user-images.githubusercontent.com/127286755/236947797-aaea6732-807d-43ab-96f9-03e076093ca4.png)

### - New York location: 
Near Gilt Groupe (design company) that has raised $236M raised, located at 2 Park Ave Fl 4, close to the Empire State
![image](https://user-images.githubusercontent.com/127286755/236948083-6c2b45b6-0025-4f72-99a2-518773d1ebc2.png)

### - London location:
Near Netbiscuits (design company) that has raised $27M, located at 25 North Row, close to the Hyde Park
![image](https://user-images.githubusercontent.com/127286755/236948043-d320c8b3-9e5b-4128-98fb-62552a7d60ad.png)

## Result

We created two plots to check which location was the best, based on the nearests venues:

![distance_locations_plot](https://user-images.githubusercontent.com/127286755/236948516-b88e9470-6186-473a-b889-1d3a44ba6acd.png)

As you can see NEW YORK location has the closests: Train Station, Starbucks, Basketball stadium and Airport (we did not show airport on the plot, as the three of them were outliers for the bar plots). SAN FRANCISCO location had the closests: Primary and Secondary School, Night clubs and Vegan restaurant. And LONDON has the closests Preschool and Dog Grooming.

Finally, we created a "points" method, the location with the closest venue got 2 points, the second one got 1 point and the third one got 0 points. The location with the highest number of points was the one that followed more preferences and requirements, and it was NEW YORK!

![image (1)](https://user-images.githubusercontent.com/127286755/236949364-684a9bb5-26a9-4bdc-b51f-c4eadfd7478f.png)

![cities_grades_plot](https://user-images.githubusercontent.com/127286755/236948546-979f39b9-6741-4aed-a15b-ecf8d395ad83.png)

## Files

- dataframes: folder with four csv dataframes.
- maps: folder with three thtml files with the folium maps generates.
- figures: folder with four png files. Those are the charts that we created.
- jupyter notebooks: two jupyter notebook files with all the previous researching, cleaning and transforming.
- src: three pyhton files with downloading, cleaning and vizualization functions.
- README.md
- main.jpyn: The main file, you need to execute the file with jupyter notebook and see the results of the analysis.

## Technologies

Jupyter notebook
Mongo's database
Folium
Python
Html
Os

### Libraries used:

from pymongo import MongoClient
import re
import requests
import json
from getpass import getpass
import time
from dotenv import load_dotenv
import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster
import pandas as pd
import os
import matplotlib.pyplot as plt

Git clone and you can execute the code on your terminal using: pyhton main.py

## Next steps:

- Web scrape real state sites to get the best prices and choose a neighbourhood, a block or an adress.

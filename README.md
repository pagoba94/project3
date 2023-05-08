# Project 2 - MONGOGAME COMPANY: Where should we locate our new office? 

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
To start the analysis we used a Mongo's database with more than 18k start ups data. Using mongo queries, we looked for the count of design companies located in each city, so that we can locate our company in one of those cities. We also looked for the best gaming companies location, we want our office to be as close to them to follow their steps. 

## Result


## Files

- data: folder with four csv dataframes.
- figures: folder with four html files and four png files. Those are the charts that we created.
- jupyter notebooks: two jupyter notebook files with all the previous researching, cleaning and transforming.
- src: three pyhton files with downloading, cleaning and vizualization functions.
- README.md
- main.py: The main file, you need to execute the file using *pyhton main.py* and see the results of the analysis.


## Technologies

Jupyter notebook
Mongo's database
Folium
Python
html
os

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

## References: 


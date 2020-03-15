'''
This program gives you a translation of I love you in a vareity of languages.

Author: Sahra Ghalebikesabi
'''


# packages
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pprint import pprint

# read in web page
link = r"http://www.aeppelsche-homepage.de/liebe.htm"
f = requests.get(link)

# replace <br> for preserving linebreaks
replaced_br = f.text.replace('<br>', 'newtransl') 

# read in tables into data frames
dfs = pd.read_html(replaced_br)

# merge data frames
frames = dfs[2:]
langs_table = pd.concat(frames)
langs_table = langs_table.reset_index().drop('index', axis=1)

# create dictionary
langs_dict = dict(zip(langs_table.iloc[:,0], langs_table.iloc[:,1]))


# drop if column 1 is na (Deutsche Dialekte)
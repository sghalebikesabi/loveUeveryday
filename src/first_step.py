'''
This file gives you a translation of I love you in a vareity of 
languages in form of a list of tuples. Run this the first time
you execute the code and make sure that 'data/langs_alphabet.txt'
and 'data/langs_time.txt' are empty if you never said 'I love you'
in any language yet. Otherwise change the files accordingly.

Author: Sahra Ghalebikesabi
'''

from bs4 import BeautifulSoup
# import codecs
import html5lib
import random
import requests
import pandas as pd
import pickle
from pprint import pprint


######----------------------------- preprocess data from web page-----------------------------######

# read in web page
link = r"http://www.aeppelsche-homepage.de/liebe.htm"
f = requests.get(link)

# replace <br> for preserving linebreaks
replaced_br = f.text.replace('<br>', 'newtransl') 
# sometimes a language has multiple translations, separate these with 'newtransl'

# save html file
# with open('data/liebe.htm', 'w') as file:
#    file.write(replaced_br)

# read in tables into data frames
dfs = pd.read_html(replaced_br, encoding='ISO-8859-1')

# merge data frames
frames = dfs[2:]
langs_table = pd.concat(frames)
langs_table.loc[:,'new_index'] = list(range(len(langs_table)))
langs_table = langs_table.set_index('new_index')

# drop rows with NAs (here only title 'Deutsche Dialekte')
# uncomment following line to display those rows with NA values
# langs_table[langs_table.isna().any(axis=1)]
langs_table = langs_table.dropna()

# split those rows with multiple translations
translations = list(langs_table[1])
nonflat_translations = [[j.strip() for j in translations[i].split('newtransl')] for i in range(len(translations))]
translations = [j.strip() for i in range(len(translations)) for j in translations[i].split('newtransl')]

# create list of languages, enumerate those with multiple translations
languages = list(langs_table[0])
languages = [lang.replace(' :', '') for lang in languages]
languages = [
    languages[lang_index] + (' ' + str(j+1))*(j>0)
    for lang_index in range(len(languages)) for j in range(len(nonflat_translations[lang_index]))
]

# drop those translations which are only comments (handpicked) and add comments to translation they belong to 
only_comments = ['Fränkisch 4', 'Hebräisch 5', 'Holländisch 17', 'Klingon 6', 'Lettisch 2', 'Punjabi 4', 'Urdu 7']
only_comments_idx = [languages.index(lang) for lang in only_comments]
for i in only_comments_idx:
    translations[(i-2):i] = [' '.join(translations[(i-2):i])]
languages = [lang for lang in languages if lang not in only_comments]


######----------------------------- add further languages-----------------------------######

# animals
animal_languages = ['Katze', 'Hund', 'Pferd', 'Schaf', 'Schwein', 'Kuh', 'Affe', 'Huhn', 'Hahn', 'Vogel', 'Eule', 'Ente', 'Gans', 'Truthahn', 'Fliege', 'Grashüpfer', 'Frosch', 'Löwe']
animal_translations = ['meow', 'woof', 'neigh', 'baa', 'oink', 'moo', 'hee-haw', 'cluck', 'cock-a-doodle-do', 'chirp', 'Hoot', 'quack', 'honk', 'gobble', 'buzz', 'chirp', 'ribbit', 'roar']
languages += animal_languages
translations += animal_translations

# reverse of each language
reverse_languages = [lang + ' rückwärts' for lang in languages]
reverse_translations = [transl[::-1] for transl in translations]
languages += reverse_languages
translations += reverse_translations


######----------------------------- create a dictionary -----------------------------######

# create dictionary
langs_dict = dict(zip(languages, translations))

# rename some languages
langs_dict['Brasilianisch'] = langs_dict.pop('Portugiesisch/Brazilian')
langs_dict['Amharisch'] = langs_dict.pop('Amharic (Äthiopien)')
langs_dict['Malay'] = langs_dict.pop('Malay/Indonesien:')


######----------------------------- read in old languages -----------------------------######
# comment this section if you do not already have a list of languages you used
with open('data/langs_alphabet.txt', 'r') as alph_file, open('data/langs_time.txt', 'r') as time_file:
    alphabet_list = alph_file.read()
    timeord_list = time_file.read()

alphabet_set = set(alphabet_list.split('\n'))
timeord_set = set(timeord_list.split('\n'))

# make sure all languages are in timeord_set; analyse
alphabet_set - timeord_set 
timeord_set - alphabet_set

# make sure languages in timeord_set are sensible
list(timeord_set - set(langs_dict.keys()))

# drop already used languages
for key in timeord_set: 
    delthis = langs_dict.pop(key, None)


######----------------------------- output list of languages (with date) and corresponding list of translations -----------------------------######
a_loveu_everyday = list(langs_dict.items())
random.shuffle(a_loveu_everyday)

with open('data/a_loveu_everyday.pkl', 'wb') as file:
    pickle.dump(a_loveu_everyday, file, protocol=pickle.HIGHEST_PROTOCOL)
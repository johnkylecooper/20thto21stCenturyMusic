#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 20:25:10 2020

@author: johnkylecooper
"""

# import the library we use to open URLs
from urllib.request import Request, urlopen

from random import randint

import requests

year=randint(1958,2016)

# specify which URL/web page we are going to be scraping
url = "https://playback.fm/charts/top-100-songs/"+str(year)

req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(req).read()
page = page.decode("utf-8")

# import the BeautifulSoup library so we can parse HTML and XML documents
import bs4 as BeautifulSoup

# parse the HTML from our URL into the BeautifulSoup parse tree format
soup = BeautifulSoup.BeautifulSoup(page, 'html.parser')

# Use either View Source command on your web page or the BeautifulSoup function 'prettify' to
# look at the HTML underlying our chosen web page
# print(soup.prettify())

# play around with some of the HTML tags and bring back the page 'title' and the data between the start and end 'title' tags
soup.title
# refine this a step further by specifying the 'string' element and only bring back the content without the 'title' tags
soup.title.string

# use the 'find_all' function to bring back all instances fo the 'table' tag in the HTML and store in 'all_tables' variable
all_tables=soup.find_all("table")

right_table=soup.find('table', class_='chartTbl')

# Extract information from table
A=[]
B=[]
C=[]
D=[]

for row in right_table.findAll('tr'):
    cells=row.findAll('td')
    if len(cells)==4:
        A.append(cells[0].find(text=True))
        B.append(cells[1].find(text=""))
        C.append(cells[2].find(text=""))
        D.append(cells[3].find(text=""))

# Find Song URL
idx=0
for tag in enumerate(D):
    D[idx] = str(tag)[14:-10]
    idx+=1

# Find Song URL
idx=0
for tag in enumerate(C):
    C[idx] = str(tag)[:-13]
    C[idx] = C[idx].split('>')[len(C[idx].split('>'))-1]
    idx+=1

song_number = randint(0,len(D))
import string
song_tag = D[song_number].replace('\"','')

file1 = open("songs.txt")
past_songs = file1.read()
file1.close()
while song_tag in past_songs:
    print('discovered repeat...')
    print('generating new song info...')
    song_number = randint(0,len(D))
    song_tag = D[song_number].replace('\"','')
# Write to a text file that lists the already posted songs
file1 = open("songs.txt","a")
file1.write(song_tag+'\n')
file1.close()
    
song_url = "https://playback.fm/"+song_tag

req = Request(song_url, headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(req).read()
page = page.decode("utf-8")

# # import the BeautifulSoup library so we can parse HTML and XML documents
# import bs4 as BeautifulSoup

# # parse the HTML from our URL into the BeautifulSoup parse tree format
# soup = BeautifulSoup.BeautifulSoup(page, 'html.parser')
# html = str(soup)
# idx = html.find('videoId')
# videoId = html[idx+10:idx+21]
# yt_url = "https://www.youtube.com/watch?v="+videoId

# Generate song_title for searching wikipedia
song_title = C[song_number]
song_title_sep = song_title.translate(str.maketrans('', '', string.punctuation)).split()
song_tag_sep = song_tag.split('/')
song_combo = song_tag_sep[len(song_tag_sep)-1].split('-')

# Extract Artist
song_artist = [i for i in song_combo if i not in song_title_sep]
song_artist = ' '.join(song_artist)

import urllib.request

textToSearch = song_title+" by "+song_artist
query = urllib.parse.quote(textToSearch)
url = "https://www.youtube.com/results?search_query=" + query
response = requests.get(url)
soup = BeautifulSoup.BeautifulSoup(response.text, 'html.parser')
text_idx = response.text.find("\"videoId\"")
result = response.text[text_idx:text_idx + 22].split(":")[1].strip('\"')

yt_url = "https://www.youtube.com/watch?v="+result

import wikipedia
print(wikipedia.search(song_title+song_artist+' (song)'))
print(' ')
if wikipedia.search(song_title+song_artist+' (song)') is []:
    search_query = wikipedia.search(song_title+'('+song_artist+' song)')
else:
    search_query = wikipedia.search(song_title+song_artist+' (song)')[0]
song_info = wikipedia.summary(search_query, sentences=2)
status = song_info + '\n' + yt_url
if len(status) > 300:
    song_info = wikipedia.summary(search_query, sentences=1)
    status = song_info + '\n' + yt_url
print(status)

# Collect Keys
keys = open("keys.txt").read().split()

import twitter
api = twitter.Api(consumer_key=keys[0],
                  consumer_secret=keys[1],
                  access_token_key=keys[2],
                  access_token_secret=keys[3])
api.PostUpdate(status)
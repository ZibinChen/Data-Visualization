#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 10:47:02 2018

@author: zibinchen
"""

import requests
import json
import time
import csv
    
# (b)
#api_key = "b65d2312aadde0ea58a32e10df4227b6"
API = {"api_key":api_key}
Selected_Genre = 'Comedy'

request_list = requests.request("GET", "https://api.themoviedb.org/3/genre/movie/list", data=API)
genre = request_list.json()

for i in genre['genres']:
    if i['name'] == Selected_Genre:
        genre_id = i['id']
        
after_date = '2000-01-01'

page = 1
N_movie = 1
Movie = []
while N_movie <= 300:
    payload_movie = {"api_key":api_key,"sort_by":"popularity.desc","with_genres":genre_id,"page":page,
                     "primary_release_date.gte":after_date}
    movie_json = requests.request("GET", "https://api.themoviedb.org/3/discover/movie", data=payload_movie)
    time.sleep(0.25)
    movie_list = json.loads(movie_json.text)
    list_result = movie_list["results"]
    
    for j in list_result:
        Movie.append([str(j["id"]), j["title"]])
        N_movie += 1
        if N_movie > 300:
            break
    page += 1
    
with open('movie_ID_name.csv', 'w', newline='',encoding = 'utf-8') as result:
     write_csv = csv.writer(result, delimiter=',')
     for row in Movie:
         write_csv.writerow(row)

# (c)
'''
# 
Movie = []
with open('movie_ID_name.csv','r',newline = '') as result:
    read_csv = csv.reader(result)
    for row in read_csv:
        Movie.append(row)
'''

No_Similar = 5
similar_ID = []
for i in Movie:

    N = 0
    Request = requests.request("GET", "https://api.themoviedb.org/3/movie/"+i[0]+"/similar", data=API)
    time.sleep(0.25)
    
    Movie_list = json.loads(Request.text)
    for j in Movie_list["results"]:
        similar_ID.append([str(i[0]),str(j['id'])])
        N += 1
        if N >= No_Similar:
            break

# remove duplication
N_similar = len(similar_ID)
final_list = []
for i in range(N_similar):
    
    ID1 = similar_ID[i]
    i = 0
    for j in range(i+1,N_similar):
        
        ID2 = similar_ID[j]
        
        if ID1[0] == ID2[1] and ID1[1] == ID2[0]:
            i += 1
            similar_ID[j][0] = min(ID1[0], ID1[1])
            similar_ID[j][1] = max(ID1[0], ID1[1])
            
    if i >= 1 :
        final_list = final_list
        
    else:
        final_list.append(ID1)

with open('movie_ID_sim_moive_ID.csv', 'w', newline='',encoding = 'utf-8') as result:
     write_csv = csv.writer(result, delimiter=',')
     for row in final_list:
         write_csv.writerow(row)




import numpy as np
import pandas as pd
import time
import random
from prettytable import PrettyTable
import csv
from distances_func import distance_map
teams=open('matchups.txt', 'r')
data=teams.readlines()
#print data[0].split('\r')
divisions={}
print distance_map.keys()
city_team={}
for row in data[0].split('\r')[1:]:
	row=row.split('\t')
	team=row[0].strip('\xca')
	div=row[1]
	city=row[2]
	city_team[team]=city
	print row
	if div in divisions:
		divisions[div].append(team)
	else:
		divisions[div]=[team]

#print divisions
matchups={}

target = open('divmatches.csv', 'w')

writer = csv.writer(target)			

writer.writerow(['Matchup', 'Division','Distance'])

for div in divisions:
	teams=divisions[div]
	matchups[div]=[]
	for i, team1 in enumerate(teams):
		for j, team2 in enumerate(teams[i+1:]):
			matchup='%s vs %s ' %(team1, team2)
			c1=city_team[team1]
			c2=city_team[team2]
			dist=distance_map[c1][c2]

			matchups[div].append(matchup)
			writer.writerow([matchup, div,dist])


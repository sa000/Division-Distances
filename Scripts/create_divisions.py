import numpy as np
import pandas as pd
import time
import random
from prettytable import PrettyTable
import csv
distances=pd.read_csv('../Data/distances_30.csv')
distance_map={}
teams=distances.columns[1:]
teams_set=set(teams)
team_division={}

#Debugging, display the divisions 
def print_divisions(divisions):
	total=0
	for i in xrange(8):
		print 'Division %s' % i, sorted(list(divisions[i]['teams']))
		total+=divisions[i]['distance']
	print total
	return total
#Get distance of a division
def get_distance(division):
	dist=0
	teams=list(division)
	for idx, team in enumerate(teams):
		for idx2, team2, in enumerate(teams[idx+1:]):
			dist+=distance_map[team][team2]
	return dist

#Find partner team to switch with current team to minimize overall distance
def find_partner(team1, teams_left,divisions):
	team_to_switch=None
	distance_saved_sofar=1
	for team2 in teams_left:
		d1, d2=team_division[team1], team_division[team2]
		if d1 ==d2:
			continue
		div1, div2 = set(divisions[d1]['teams']), set(divisions[d2]['teams'])
		cur_dist=get_distance(div1)+get_distance(div2)
		
		div1.add(team2)
		div1.remove(team1)

		div2.add(team1)
		div2.remove(team2)

		swapping_distance=get_swap_distance(div1, div2)

		cur_savings=max(cur_dist-swapping_distance,0)

		if cur_savings>distance_saved_sofar:
			team_to_switch=team2
			distance_saved_sofar=cur_savings
	#print "distance saved", distance_saved_sofar
	return team_to_switch
#get the distance of the two divisions
def get_swap_distance(div1,div2):
	dist1=get_distance(div1)
	dist2=get_distance(div2)
	return dist1+dist2



#Creates an n x n symmetric distance map to map from 1 team to another
for team in teams:
	distance_map[team]={}


for idx, row in distances.iterrows():
	team1	=row.values[0]
	for team2 in teams:
		dist=row[team2]
		distance_map[team1][team2]=dist 
		distance_map[team2][team1]=dist
divisions=[[] for i in xrange(8)]

#Create a random, feasible division
def random_divisions():
	random.shuffle(teams.values)
	divisions={}
	for i in xrange(8):
		divisions[i]={} 
		divisions[i]['teams']=set()
		divisions[i]['distance']=0
	i=0

	for team in teams:
		divisions[i]['teams'].add(team)
		team_division[team]=i
		i+=1
		i=i%8

	for i in xrange(8):
		divisions[i]['distance']=get_distance(divisions[i]['teams'])
	return divisions

#Set the distances large and start minimizing
min_dist=1000000
cur_dist=1000000
min_divisions={}
#for i in range(100):
divisions=random_divisions()
	 
changes=1
#Run this n times
for i in range(100):
	while changes>0:
		unvisited=set(teams)
		changes=0
		while unvisited:

			team1=unvisited.pop()

			team2=find_partner(team1, unvisited,divisions)
			if team2:
				changes+=1
				#print_divisions(divisions)
				d1, d2=team_division[team1], team_division[team2]
				div1, div2=divisions[d1]['teams'], divisions[d2]['teams']
				div1.add(team2)
				div1.remove(team1)
				div2.add(team1)
				div2.remove(team2)


				divisions[d1]['distance']=get_distance(div1)

				divisions[d2]['distance']=get_distance(div2)

				team_division[team1]=d2
				team_division[team2]=d1
				
				
				
				unvisited.remove(team2)

	cur_dist=print_divisions(divisions)
	#Keep track of the best set of divisions
	if cur_dist<min_dist:
		min_dist=cur_dist
		min_divisions=divisions
	print "final"

print print_divisions(min_divisions)


#Write output

tot=0
target = open('distance_8.csv', 'w')
writer = csv.writer(target)
writer.writerow(['Team', 'dist', 'Division'])
for i in xrange(8):
	min_divisions[i]['distance']=get_distance(min_divisions[i]['teams'])
	teams=min_divisions[i]['teams']
	dist=min_divisions[i]['distance']
	for team in teams:
		data=[team, dist, 'Division %s' %str(i+1)]
		line = '{}\t{}\tDivision {}\n'.format(team, dist, i+1)
		writer.writerow(data)
print tot
# print_divisions(divisions)





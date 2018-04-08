import urllib
import json
import sys

import csv

import time
cities=[]
googleaddress = "https://maps.googleapis.com/maps/api/directions/json?"
#Create our distance csv using google api
with open('nba_cities.txt') as f:
	for line in f:
		cleanLine=line.strip()
		cities.append(cleanLine)
target=open('distances2.csv', 'wb')
csvwriter=csv.writer(target)
csvwriter.writerow([" "]+cities)
cache={}
print 'starting'


for starting_point in cities:
	distances=[starting_point]
	for end_point in cities:	
		reverse=end_point+'_'+starting_point
		if starting_point==end_point or reverse in cache:
			if reverse in cache:
				dist=cache[reverse]
			else:
				dist=0
		else:
			response = urllib.urlopen(googleaddress + "origin=" + starting_point + "&destination=" + end_point + "&sensor=false&mode=driving&key=AIzaSyBCdk69uKrjGomVFLRTwBC5BoBWzwk5bvs")
			pyresponse = json.load(response)
			#print starting_point, end_point, pyresponse
			#print pyresponse
			results = pyresponse["routes"]
			for i in range(len(results)):
				for key in results[i]:
					if key =="legs":
						dist=results[i][key][0]["distance"]["text"]
						dist=dist.split(' ')[0]
						print 'on', starting_point, end_point, dist
						route=starting_point+'_'+end_point
						cache[route]=dist
		distances.append(dist)
		
	print "finished", starting_point, distances
	csvwriter.writerow(distances)
print "done"

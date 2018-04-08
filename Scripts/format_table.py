import numpy as np
import pandas as pd
import time
import random
from prettytable import PrettyTable
import csv
# distances=pd.read_csv('distances.csv')
# distance_map={}
# teams=distances.columns[1:]
# teams_set=set(teams)
# team_division={}

#Create matchupes to display
text_file = open("Output.txt", "w")
f=open('match_table.txt','r')
content=f.readlines()[0].split('\r')


for idx, line in enumerate(content):
	data=line.split('\t')
	string=''
	for i, item in enumerate(data):
		if len(item)>0:
			if i%2==1:
				string+=item+'|'
			else:
				string+=item+':'

	string=string[:-1]
	string+='\n'
	text_file.write(string)


text_file.close()

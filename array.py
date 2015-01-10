#!/usr/bin/env python

import sys, json, collections 

input = open(sys.argv[1])
# data = json.load(input) #data now a dict
lis = []

for item in input:
  lis.append(item)

counts = collections.Counter(lis)
new_list = sorted(lis, key=lambda x: -counts[x]) #count uniques
listt = [] #create new list

from collections import Counter
c = Counter(new_list)
for key, values in c.most_common(100): #find first 100 unique items
  print key.strip()
  listt.append(key.strip()) #append in list

with open('sorted-unique.json', 'w') as outfile:
  json.dump(listt, outfile)
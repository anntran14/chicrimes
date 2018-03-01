#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import train_test_split
from datetime import datetime
from sklearn import cross_validation
from sklearn.metrics import accuracy_score
from sklearn import metrics

import random

import numpy as np 
import pandas as pd
import csv
import time
import io

############################

def get_data_list_of_dicts(filename):
    list = []
    with io.open(filename, "r", encoding="utf-8-sig") as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            list.append(row)
    return list

def get_headers(filename):
    with io.open(filename, "r", encoding="utf-8-sig") as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
    return headers

def del_column(dict_list, remove_list, headers):
	for elem in dict_list:
		for column_name in remove_list:
			if column_name in elem:
				del elem[column_name]
	new_headers = list()
	for header in headers:
		if header not in remove_list:
			new_headers.append(header)
	return (dict_list, new_headers)

def clean_date(dict_list):
	for elem in dict_list:
		cur_time = elem["Date"]
		time = cur_time.split(" ")
		hour = time[1].split(":")
		elem["Date"] = hour[0]
		#dt = time.strptime(date_string, "%d/%m/%Y %I:%M:%S")
		#elem["Date"] = dt.tm_hour

def write_data_dicts(filename, headers, rows_list_of_dicts):
    with open(filename,'w') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(rows_list_of_dicts)

def cleaning (filename, remove_list, newfile):
	dict_list = get_data_list_of_dicts(filename)
	headers = get_headers(filename)
	(dict_list, headers) = del_column(dict_list, remove_list, headers)
	write_data_dicts(newfile, headers, dict_list)

#####################

remove_list = {"Primary Type", "Description", "Year", "Case Number", 
"Arrest", "Domestic", "Block", "FBI Code"}
# Case Number	Date	Block	IUCR	Location Description	
# Arrest	Domestic	Beat	Ward	FBI Code	X Coordinate	Y Coordinate	
# Latitude	Longitude

#cleaning
cleaning("2002_cleaned.csv", remove_list, "2002_mod.csv")

crimes_filter = pd.read_csv('2002_mod.csv')

predictions = []
actual = []
acc = []

X = pd.concat([pd.get_dummies(crimes_filter['Date'], prefix = 'P'), 
	pd.get_dummies(crimes_filter['Beat'], prefix = 'NL'), 
#	pd.get_dummies(crimes_filter['X Coordinate'], prefix = 'xc'), 
#	pd.get_dummies(crimes_filter['Location Description'], prefix = 'ld'),
#	pd.get_dummies(crimes_filter['Y Coordinate'], prefix = 'yc'), #label encoder? 
	pd.get_dummies(crimes_filter['Ward'], prefix = 'xc')], axis = 1)

Y = crimes_filter['IUCR']

X_train = X[:200000]
Y_train = Y[:200000]
X_test = X[200000:400000]
Y_test = Y[200000:400000] #data without header, with header, train size 2/3 

clf = MultinomialNB()
clf.fit(X_train,Y_train)

pred = clf.predict(X_test)
accuracyDT = accuracy_score(Y_test, pred)

acc.append(accuracyDT) 

print 'Accuracy', np.mean(acc)

print(metrics.classification_report(Y_test, pred))
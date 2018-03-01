from time import time
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import train_test_split

import random

import numpy as np 
import pandas as pd

############################

def get_data_list_of_dicts(filename):
    list = []
    with io.open(filename, 'r', encoding='utf-8-sig') as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            list.append(row)
    return list

def get_headers(filename):
    with io.open(filename, 'r', encoding='utf-8-sig') as f:
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
	clean_date(dict_list)
	write_data_dicts(newfile, headers, dict_list)

#####################

remove_list = {"Primary Type", "Description", "Year", "Location", "Case Number", "X Coordinate", "Y Coordinate", 
"Latitude", "Longitude", "Location Description", "Arrest", "Domestic"}

cleaning("2002_cleaned.csv", remove_list, "2002_mod.csv")

crimes = pd.read_csv('2002_mod.csv')
crimes2 = crimes.copy()
targets = crimes2["IUCR"].unique()

hi = "hello"
print (hi)
print (type(crimes))

for v in variables:
	crimes_filter[v] = crimes2[v]

features = list(crimes_filter.columns[0:])

X = crimes_filter[features]
y = crimes2["Target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.4, random_state=0)


classifier = MultinomialNB()
classifier.fit(X, y)

MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
print(X)
print(classifier.predict(X[2:3]))


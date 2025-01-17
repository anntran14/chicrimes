import numpy as np 
import pandas as pd 
import csv
import io

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn import cross_validation
from sklearn import datasets
from sklearn import preprocessing

# _FILEPATH = "2002_slice_cleaned.csv"
# _POSTCLEANEDPATH = "2002_slice_postcleaned.csv"

_FILEPATH = "2002_cleaned.csv"
_POSTCLEANEDPATH = "2002_postcleaned.csv"

def get_headers(filename):
    with open(filename) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
    return headers

def get_data_slice(column_name, list_of_dicts):
    list = []
    for dict in list_of_dicts:
        list.append(dict[column_name])
    return list

def get_data_list_of_dicts(filename):
    dict_list = []
    with open(filename) as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
        	dict_list.append(row)
    #print dict_list
    return dict_list

# Given a list of dicts and list of categorial headers, return a l
# list of dictionaries with all headers as numerical values where 
# encoders are the mappings.
def handle_categorical(dict_list, cat_headers):
	encoders = list()
	for header in cat_headers:
		encoder = preprocessing.LabelEncoder()
		col_data = get_data_slice(header, dict_list)
		encoder.fit(col_data)
		encoders.append(encoder)
		transformed = encoder.transform(col_data)
		for i in range (0, len(dict_list)):
			dict_list[i][header] = transformed[i]
	return (dict_list, encoders)

def split_dataset(data, train_percentage, headers, target_header):
    X_train, X_test, y_train, y_test = train_test_split(data[headers], data[target_header], train_size=train_percentage, random_state=42)
    return X_train, X_test, y_train, y_test

def post_cleaning(dict_list, headers, filename):
	with open(filename,'w') as f:
		f_csv = csv.DictWriter(f, headers)
		f_csv.writeheader()
		f_csv.writerows(dict_list)

def main():
	# Clean data
	dict_list = get_data_list_of_dicts(_FILEPATH)
	headers = get_headers(_FILEPATH)
	(dict_list, encoders) = handle_categorical(dict_list, ['Case number', 'IUCR', 'Block', 'Location Description', 'FBI Code'])
	post_cleaning(dict_list, headers, _POSTCLEANEDPATH)

	# Read data
	data = pd.read_csv(_POSTCLEANEDPATH)
	data = data.fillna(0)
	print data.describe()

	# Remove unnecessary headers
	headers.remove("IUCR")
	headers.remove("Case number")

	X_train, X_test, y_train, y_test = split_dataset(data, 0.8, headers, ) # hour is 10%, Mo is 16%, Weekday is %17, iucr is 9%
	print "X_train Shape: ", X_train.shape
	print "y_train Shape: ", y_train.shape
	print "X_test Shape: ", X_test.shape
	print "y_test Shape: ", y_test.shape

	mnb = MultinomialNB()
	mnb.fit(X_train, y_train)
	print("Trained model: ", mnb)
	predictions = mnb.predict(X_test)

	###
	cnf_matrix_mnb = confusion_matrix(y_test, predictions)
	print(cnf_matrix_mnb)
	# kf = cross_validation.KFold(len(y2), n_folds=2)
	####

	print "Train Accuracy: ", accuracy_score(y_train, mnb.predict(X_train))
	print "Test Accuracy: ", accuracy_score(y_test, predictions)

if __name__ == "__main__":
	main()
	
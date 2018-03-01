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

################
from sklearn.datasets import load_iris
iris = load_iris()

# iris data
X_i = iris.data
y_i = iris.target
data = pd.DataFrame(X_i, columns=iris.feature_names)
print "\ndata as X:", iris.feature_names
print "target (species):", iris.target
print type(data)

X_train, X_test, y_train, y_test = train_test_split(X_i, y_i, train_size= 0.33, random_state=42)

mnb = MultinomialNB()
mnb.fit(X_train, y_train)
print("Trained model: ", mnb)
predictions = mnb.predict(X_test)

print "Train Accuracy: ", accuracy_score(y_train, mnb.predict(X_train))
print "Test Accuracy: ", accuracy_score(y_test, predictions)

# crime data
use_cols = ['Block','Location Description','Arrest','Domestic','Beat','Ward','FBI Code','Hour','Weekday','Monthday','Month']
crimes = pd.read_csv('2002_slice_cleaned.csv')
crimes2 = pd.DataFrame(crimes, columns=use_cols)
x_c = crimes2.copy()
print type(crimes2)

# Split the data into a training set and a test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

mnb = MultinomialNB()
mnb.fit(X_train, y_train)
y_pred_mnb = mnb.predict(X_test)
# OR y_pred_mnb = mnb.fit(X_train, y_train).predict(X_test)

cnf_matrix_mnb = confusion_matrix(y_test, y_pred_mnb)
print(cnf_matrix_mnb)

kf = cross_validation.KFold(len(y2), n_folds=2)

# accuracyDT = accuracy_score(Y_test, pred)
# acc.append(accuracyDT)
# print 'Accuracy', np.mean(acc)
# print(metrics.classification_report(y_test, pred))
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


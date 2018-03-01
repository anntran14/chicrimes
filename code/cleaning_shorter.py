import csv
import time
import io

#0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
#"Primary Type", "Description", "Year", "Location"

def cleaning (filename, newfile):
	index = 0
	with open(newfile ,'w') as outFile:
	    fileWriter = csv.writer(outFile)
	    with open(filename,'r') as inFile:
	        fileReader = csv.reader(inFile)
	        for row in fileReader:
	        	index = index + 1
	        	fileWriter.writerow(row)
	        	if index == 100:
	        		break

cleaning("../data/2002_violent_cleaned.csv", "../data/2002_violent_slice_cleaned.csv")



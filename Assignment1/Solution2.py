### Problem 2 Solution
import numpy
import urllib
import scipy.optimize
import random
### from sklearn import svm

def parseData(fname):
  for l in urllib.urlopen(fname):
    yield eval(l)

print "Reading data..."
data = list(parseData("http://jmcauley.ucsd.edu/cse255/data/amazon/book_descriptions_50000.json"))
print "done"

### Probabililty that a book has category "Romance" (a)

hasRomance = ["Romance" in b['categories'] for b in data]
hasRomance = sum(hasRomance) * 1.0 / len(hasRomance)

# Probabililty that a book doesn't have category "Romance"

negHasRomance = 1 - hasRomance

# Probability that book mentions "love" in description given it is Romance (b)

loveInDescription = ['love' in b['description'] for b in data if "Romance" in b['categories']]
loveInDescription = sum(loveInDescription) * 1.0 / len(loveInDescription)

### Problem 2.2

pNum = ["Romance" in b['categories'] for b in data if 'love' in b['description'] and 'beaut' in b['description']]
pNum = sum(pNum) * 1.0 / len(pNum)

pDem = ["Romance" not in b['categories'] for b in data if 'love' in b['description'] and 'beaut' in b['description']]
pDem = sum(pDem) * 1.0 / len(pDem)

bayes = pNum / pDem

print "Value we get from running bayes on the two probabilities: " + str(bayes)

print "The string 'beaut' is more effective than separating 'beauty'/'beautiful' because we need a "
print "mutually exclusive calculation - just use 'beaut'. This is so we can exclude multiple "

### Problem 2.3
# Calculating love not in description
pNum1 = ["Romance" in b['categories'] for b in data if 'love' not in b['description'] and 'beaut' in b['description']]
pNum1 = sum(pNum1) * 1.0 / len(pNum1)

pDem1 = ["Romance" not in b['categories'] for b in data if 'love' not in b['description'] and 'beaut' in b['description']]
pDem1 = sum(pDem1) * 1.0 / len(pDem1)

bayes1 = pNum1 / pDem1

print "Value we get when calculating love not in description: " + str(bayes1)

# Calculating beaut not in description
pNum2 = ["Romance" in b['categories'] for b in data if 'love' in b['description'] and 'beaut' not in b['description']]
pNum2 = sum(pNum2) * 1.0 / len(pNum2)

pDem2 = ["Romance" not in b['categories'] for b in data if 'love' in b['description'] and 'beaut' not in b['description']]
pDem2 = sum(pDem2) * 1.0 / len(pDem2)

bayes2 = pNum2 / pDem2

print "Value we get when calculating beaut not in description: " + str(bayes2)

# Calculating beaut and love not in description
pNum3 = ["Romance" in b['categories'] for b in data if 'love' not in b['description'] and 'beaut' not in b['description']]
pNum3 = sum(pNum3) * 1.0 / len(pNum3)

pDem3 = ["Romance" not in b['categories'] for b in data if 'love' not in b['description'] and 'beaut' not in b['description']]
pDem3 = sum(pDem3) * 1.0 / len(pDem3)

bayes3 = pDem3/pNum3

print "Value we get when calculating love and beaut not in description: " + str(bayes3)

# Calculate the TP TN FP FN

def number3(datam):
	TP = 0
	TN = 0
	FP = 0
	FN = 0
	for b in datam:
		if 'love' in b['description'] and 'beaut' in b['description']:
			if "Romance" in b['categories']:
				FN += 1
			else:
				FP += 1
		elif 'love' in b['description'] and 'beaut' not in b['description']:
			if "Romance" in b['categories']:
				FN += 1
			else:
				FP += 1
		elif 'love' not in b['description'] and 'beaut' in b['description']:
			if "Romance" in b['categories']:
				FN += 1
			else:
				FP += 1
		elif 'love' not in b['description'] and 'beaut' not in b['description']:
			if "Romance" in b['categories']:
				TN += 1
			else:
				TP += 1
	feat = [TP]
	feat.extend([TN,FP,FN])
	return feat





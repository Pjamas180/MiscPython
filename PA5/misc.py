#PA 4

import re
import sys

"Miscellaneous functions to practice Python"

class Failure(Exception):
    """Failure exception"""
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return repr(self.value)

# Problem 1

# data type functions

def closest_to(l,v):
    """Return the element of the list l closest in value to v.  In the case of
       a tie, the first such element is returned.  If l is empty, None is returned."""
    if l == []:
        return None
    returnValue = l[0]
    # For loop that will loop through all the values in l checking for the closest value
    for loopValue in l:
        if(abs(v - loopValue) < abs(v-returnValue)):
            returnValue = loopValue
    return returnValue

def make_dict(keys,values):
    """Return a dictionary pairing corresponding keys to values."""
    dictionary = {}
    for i in range(len(keys)):
        dictionary[keys[i]] = values[i]
    return dictionary

# file IO functions
def word_count(fn):
    """Open the file fn and return a dictionary mapping words to the number
       of times they occur in the file.  A word is defined as a sequence of
       alphanumeric characters and _.  All spaces and punctuation are ignored.
       Words are returned in lower case"""
    # Opens a file for reading
    input_file = open(fn,'r')
    input_file2 = open(fn, 'r')
    word_number = {}
    for line in input_file:
        line_list = re.split('\W+',line)
        for word in line_list:
            if word != '':
                lower = word.lower()
                word_number[lower] = 0
    for line in input_file2:
        line_list = re.split('\W+',line)
        for word in line_list:
            if word != '':
                lower = word.lower()
                word_number[lower] = word_number[lower] + 1
    return word_number


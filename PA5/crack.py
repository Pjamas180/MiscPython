# Crack class which contains methods to find passwords for accounts

from misc import *
import crypt
import re

def load_words(filename,regexp):
    """Load the words from the file filename that match the regular
       expression regexp.  Returns a list of matching words in the order
       they are in the file."""
    f = open(filename, 'r')
    listOfWords = []
    for line in f:
        m = re.match(regexp,line)
        if m != None:
            listOfWords.append(m.group(0))
    return listOfWords

def transform_reverse(str):
    """Reverse the string and return it in a list with the original string"""
    revStr = ""
    for letter in str:
        revStr = letter + revStr
    return [str,revStr]

def string_concat(list,charac):
    """Helper function which concats strings to all values of a list"""
    newList = []
    for x in list:
        x = x + charac
        newList.append(x)
    return newList

def transform_capitalize(str):
    """ Find all possible values of a string in upper and lower case values and return
    the list."""
    listOfWords = []
    if str == "":
        return [""]
    # Recursively find possibilites of the string and use the helper function
    else:
        lowercase = str.lower()
        strList = list(lowercase)
        lastChar = strList[len(strList)-1]
        newList = strList[0:len(strList)-1]
        newString = ''.join(newList)
        listOfWords.extend(string_concat(transform_capitalize(newString), lastChar))
        if lastChar.isalpha():
            listOfWords.extend(string_concat(transform_capitalize(newString), lastChar.upper()))
    return listOfWords


def transform_digits(str):
    """ Find all possible values of a string where the letters could represent digits and return
    the possibilites in a list. """
    listOfWords = []
    if str == "":
        return [""]
    # Recursively find possibilities of the string and use the helper function
    else:
        strList = list(str)
        lastChar = strList[len(strList)-1]
        newList = strList[0:len(strList)-1]
        newString = ''.join(newList)
        if lastChar.lower() == 'o':
            listOfWords.extend(string_concat(transform_digits(newString), lastChar))
            listOfWords.extend(string_concat(transform_digits(newString), '0'))
        elif lastChar.lower() == 'z':
            listOfWords.extend(string_concat(transform_digits(newString), lastChar))
            listOfWords.extend(string_concat(transform_digits(newString), '2'))
        elif lastChar.lower() == 'a':
            listOfWords.extend(string_concat(transform_digits(newString), lastChar))
            listOfWords.extend(string_concat(transform_digits(newString), '4'))
        elif lastChar.lower() == 'b':
            listOfWords.extend(string_concat(transform_digits(newString), lastChar))
            listOfWords.extend(string_concat(transform_digits(newString), '6'))
            listOfWords.extend(string_concat(transform_digits(newString), '8'))
        elif lastChar.lower() == 'i' or lastChar.lower() == 'l':
            listOfWords.extend(string_concat(transform_digits(newString), lastChar))
            listOfWords.extend(string_concat(transform_digits(newString), '1'))
        elif lastChar.lower() == 'e':
            listOfWords.extend(string_concat(transform_digits(newString), lastChar))
            listOfWords.extend(string_concat(transform_digits(newString), '3'))
        elif lastChar.lower() == 's':
            listOfWords.extend(string_concat(transform_digits(newString), lastChar))
            listOfWords.extend(string_concat(transform_digits(newString), '5'))
        elif lastChar.lower() == 't':
            listOfWords.extend(string_concat(transform_digits(newString), lastChar))
            listOfWords.extend(string_concat(transform_digits(newString), '7'))
        elif lastChar.lower() == 'g' or lastChar.lower() == 'q':
            listOfWords.extend(string_concat(transform_digits(newString), lastChar))
            listOfWords.extend(string_concat(transform_digits(newString), '9'))
        else:
            listOfWords.extend(string_concat(transform_digits(newString), lastChar))
    return listOfWords

def check_pass(plain,enc):
    """Check to see if the plaintext plain encrypts to the encrypted
       text enc"""
    salt = enc[0:2]
    return crypt.crypt(plain,salt) == enc

def load_passwd(filename):
    """Load the password file filename and returns a list of
       dictionaries with fields "account", "password", "UID", "GID",
       "GECOS", "directory", and "shell", each mapping to the
       corresponding field of the file."""
    passwd_file = open(filename,'r')
    dictArray = []
    fields = ['account','password','UID','GID','GECOS','directory','shell']
    for line in passwd_file:
        dictLine = {}
        strList = line.split(':')
        for i in range(7):
            dictLine[fields[i]] = strList[i]
        dictArray.append(dictLine)
    return dictArray

def crack_pass_file(fn_pass,words,out):
    """Crack as many passwords in file fn_pass as possible using words
       in the file words"""

    # returns a list of dictionaries of accounts with passwords etc."""
    passDictList = load_passwd(fn_pass)
    passDictList1 = load_passwd(fn_pass)
    # returns a list of words from the words file that are 6-8 characters long"""
    wordsList = load_words(words, r"[a-zA-Z0-9\-]{6,8}$")

    # Load the output file and flush everytime we update it """
    output = open(out,'w')

    # Find all non-transformed passwords first then eliminate them """
    for passDict in passDictList:
        for word in wordsList:
            if check_pass(word,passDict["password"]):
                outputStr = passDict["account"] + '=' + word + '\n'
                output.write(outputStr)
                output.flush()
                # Removing the value so we don't iterate over it again
                passDictList1.remove(passDict)
                break
            elif check_pass(transform_reverse(word)[1],passDict["password"]):
                outputStr = passDict["account"] + '=' + word + '\n'
                output.write(outputStr)
                output.flush()
                # Removing the value so we don't iterate over it again
                passDictList1.remove(passDict)
                break
            else:
                continue
            break

    passDictList2 = passDictList1

    # use transform_digits and check for any solved passwords
    for passDict in passDictList1:
        for word in wordsList:
            differentDigit = transform_digits(word)
            for digit in differentDigit:
                if check_pass(digit,passDict["password"]):
                    outputStr = passDict["account"] + '=' + digit + '\n'
                    output.write(outputStr)
                    output.flush()
                    # Using a different passDictList because we miss a value if we use original
                    passDictList2.remove(passDict)
                    break
                elif check_pass(transform_reverse(digit)[1],passDict["password"]):
                    outputStr = passDict["account"] + '=' + transform_reverse(digit)[1] + '\n'
                    output.write(outputStr)
                    output.flush()
                    passDictList2.remove(passDict)
                    break
                else:
                    continue
                break
            else:
                continue
            break

    # Find the transformed passwords
    for passDict in passDictList2:
        for word in wordsList:
            differentCapit = transform_capitalize(word)
            for capit in differentCapit:
                if check_pass(capit,passDict["password"]):
                    outputStr = passDict["account"] + '=' + capit + '\n'
                    output.write(outputStr)
                    output.flush()
                    break
                elif check_pass(transform_reverse(capit)[1],passDict["password"]):
                    outputStr = passDict["account"] + '=' + transform_reverse(capit)[1] + '\n'
                    output.write(outputStr)
                    output.flush()
                    break
                else:
                    continue
                break
            else:
                continue
            break

    output.close()


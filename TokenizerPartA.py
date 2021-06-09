"""Student name: Juanwei Hu
UCIntelID: juanweih
Student ID: 43376858
Assignment 1: text processing PartA.py"""

import re
import sys

class tokenization():

    """This function takes a filename as its parameter and open the file read all words as tokens into a list, excluding non-ascii characters"""
    #Runtime complexity could be: [O(N), O(1), 0(N log N)]
    #O N log N is only for sort() function, other commands are also either O(N), O(1)
    #This function runtime complexite: O(N)+O(N)....+O(1) = O(N)
    def tokenize(self, file):
        token_list = [] #empty list
        try:
            with open(file, "r") as file:
                for line in file:
                    # split text file word by word
                    # check regex101.com for reference: \W matches any non-word character (equivalent to [^a-zA-Z0-9_])
                    word_list = re.split(r'(\W+)', line)
                    for word in word_list:
                        #Decode ascii will throw an exception if programs encounters non-ascii chacaters like Chinese characters （我是[I am]Juanwei Hu）
                        #except block will prevent program from crashing
                        try:
                            word.encode(encoding='utf-8').decode('ascii')
                            if word.isalnum() == True:
                                word = word.lower() # change word to lower in order to avoid confusion, considering Apple, APPLE, aPPLE as the same token
                                token_list.append(word)
                        except UnicodeDecodeError:
                            pass 
        except IOError:
            print("File did not find.")
            sys.exit()    
        return token_list

    """This function takes a list contains all words from the test file and computee its freequencies"""
    #Same logic from tokenize function, O(1) for set item, O(N) for FOR loop and set item command in loop
    #Runtime complexity: O(N)
    def computeWordFrequencies(self, lst):
        frequency = dict()
        for word in lst:
            if word in frequency:
                frequency[word] += 1
            else:
                frequency[word] = 1
        return frequency

    """This function takes in a dictionary and print the words and its corresponding frequencies"""
    #Runtime complexiety: O(N log N) because sort() is O(N log N)
    def printFrequencies(self, dict1):
        # sort dict first by reverse = True for largest -> smallest value
        dict1 = {k: v for k,v in sorted(dict1.items(), key=lambda item: item[1], reverse=True)}
        for k, v in dict1.items():
            print('{k}={v}'.format(k=k, v=v))
            

if __name__ == "__main__":

    #first arg is py file and second is name of the text file.
    if len(sys.argv) != 2:
        print("Invalid arguments. It has to be two arguments.")
        sys.exit()

    #construct class instance
    token = tokenization()
    
    #list, argv[1] is the file name
    tokenList = token.tokenize(sys.argv[1])

    #compute frequencies
    tokenDict = token.computeWordFrequencies(tokenList)

    #print
    token.printFrequencies(tokenDict)
    

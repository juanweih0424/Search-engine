"""Student name: Juanwei Hu
UCIntelID: juanweih
Student ID: 43376858
Assignment 1: text processing PartB.py"""

from PartA import *

def find_common(dictA, dictB):
    
    """This functions takes two dictionaries and output the number of common words"""
    #runtime complexity is O(N log N)+O(N)
    #because sort() function complexity time is O(N log N), and for loop is O(N) 
    common = 0
    #sort two dictionary.
    dictA = {k: v for k,v in sorted(dictA.items(), key=lambda item: item[1], reverse=True)}
    dictB = {k: v for k,v in sorted(dictB.items(), key=lambda item: item[1], reverse=True)}
    #find numbers of common word in both dictA and dictB
    for word in dictA:
        if word in dictB:
            common += 1
    return common
    
if __name__ == "__main__":
    #first arg is py file and second is name of the text fileA amd last is the name of the text fileB
    if len(sys.argv) != 3:
        print("Invalid arguments. It has to be three arguments.")
        sys.exit()

    #construct 2 classes instance
    tokenA = tokenization()
    tokenB = tokenization()
    
    #list, argv[1] is the file name
    tokenListA = tokenA.tokenize(sys.argv[1])
    tokenListB = tokenB.tokenize(sys.argv[2])
    
    #compute frequencies
    tokenDictA = tokenA.computeWordFrequencies(tokenListA)
    tokenDictB = tokenB.computeWordFrequencies(tokenListB)

    #print the number of common words
    print(find_common(tokenDictA,tokenDictB))
    
    

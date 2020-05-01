#!/usr/bin/env python

"""
Reducer aggregates word counts by class and emits frequencies.

INPUT:
    partitionKey \t word \t class0_partialCount,class1_partialCount
OUTPUT:   
    word \t class0_totalCount \t class1_totalCount \t class0_Cprobability \t class1_Cprobability

"""

import sys                                                  
import numpy as np  

#################### YOUR CODE HERE ###################

import re
import sys

# initialize trackers
current_word = None
class0_wordCount_total, class1_wordCount_total = 0,0
class0_totalwords, class1_totalwords, class0_document_total, class1_document_total = 0,0,0,0
vocab_size = 0
# read from standard input
for line in sys.stdin:
   # print(line, line.split('\t'))
    # parse input
    key, word, class0_partialCount, class1_partialCount = line.strip().split('\t')
    
############ YOUR CODE HERE #########
    if word == current_word:
       # print("correct word: ", word, '\n')        
        if word == '!class0_wordCount':                    
            class0_totalwords = class0_totalwords + float(class0_partialCount)         
            
        elif word == '!class1_wordCount':                    
            class1_totalwords = class1_totalwords +float(class1_partialCount)          
            
        elif word == '!class0_document_total':                    
            class0_document_total = class0_document_total + float(class0_partialCount)          
            
        elif word == '!class1_document_total':                    
            class1_document_total = class1_document_total + float(class1_partialCount)  
          
        else:            
            if class0_partialCount != '0':            
                class0_wordCount_total = int(class0_partialCount) + class0_wordCount_total
             
            elif class1_partialCount != '0':           
                class1_wordCount_total = int(class1_partialCount) + class1_wordCount_total
              
    else:         
        
        if word == '!class0_wordCount':                    
            class0_totalwords = class0_totalwords + float(class0_partialCount)          
            
        elif word == '!class1_wordCount':                    
            class1_totalwords = class1_totalwords +float(class1_partialCount)           
            
        elif word == '!class0_document_total':                    
            class0_document_total = class0_document_total + float(class0_partialCount)           
            
        elif word == '!class1_document_total':                    
            class1_document_total = class1_document_total + float(class1_partialCount)              
            
            
        elif current_word != '!class0_wordCount' and current_word != '!class1_wordCount' and  current_word != '!class0_document_total' and current_word != '!class1_document_total':    
            vocab_size += 1
            print("{}\t{},{},{},{}".format(current_word, class0_wordCount_total ,class1_wordCount_total, float(class0_wordCount_total)/float(class0_totalwords), float(class1_wordCount_total)/float(class1_totalwords) ))
  
        current_word = word
        class0_wordCount_total = 0
        class1_wordCount_total = 0
        if current_word != '!class0_wordCount' and current_word != '!class1_wordCount' and  current_word != '!class0_document_total' and current_word != '!class1_document_total':
                if class0_partialCount != '0':
                    class0_wordCount_total = int(class0_partialCount)
                    class1_wordCount_total = 0
                elif class1_partialCount != '0':
                    class1_wordCount_total = int(class1_partialCount)
                    class0_wordCount_total = 0


if current_word != '!class0_wordCount' and current_word != '!class1_wordCount' and  current_word != '!class0_document_total' and current_word != '!class1_document_total':
    print("{}\t{},{},{},{}".format(current_word, class0_wordCount_total ,class1_wordCount_total, float(class0_wordCount_total)/float(class0_totalwords), float(class1_wordCount_total)/float(class1_totalwords) ))
vocab_size = vocab_size + 1 # Counting the last word
print("{}\t{},{},{},{}".format('!vocab_size', vocab_size  ,vocab_size,  class0_totalwords  ,class1_totalwords))

print("{}\t{},{},{},{}".format("ClassPriors", class0_document_total ,class1_document_total, float(class0_document_total)/float(class0_document_total + class1_document_total), float(class1_document_total)/float(class0_document_total + class1_document_total) ))


#################### (END) YOUR CODE ###################
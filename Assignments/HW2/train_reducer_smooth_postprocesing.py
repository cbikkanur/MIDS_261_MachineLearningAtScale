#!/usr/bin/env python
"""
Reducer aggregates word counts by class and emits Laplace +1 smoothing frequencies.
INPUT:
    word \t class0_totalCount \t class1_totalCount \t class0_Cprobability \t class1_Cprobability
OUTPUT:   
    word \t class0_totalCount \t class1_totalCount \t class0_Cprobability_smoothed \t class1_Cprobability_smoothed
    
"""
import sys                                                  
import numpy as np  
vocab_size, class0_totalwords, class1_totalwords = 0,0,0
# read from standard input
for line in sys.stdin:  
    # parse input     
    #word, class0_totalCount, class1_totalCount, class0_Cprobability, class1_Cprobability = line.strip().split('\t')  
    
    word, payload = line.strip().split('\t')  
    class0_totalCount, class1_totalCount, class0_Cprobability, class1_Cprobability = payload.split(',')
    # Capture vocab size, class0_totalwords and class1_totalwords
    #print(word)
    if word == '!vocab_size':
        vocab_size += int(class0_totalCount)
        class0_totalwords = float(class0_Cprobability)
        class1_totalwords = float(class1_Cprobability)
    elif word == 'ClassPriors':
        word_C, class0_totalCount_C, class1_totalCount_C, class0_Cprobability_C, class1_Cprobabilit_C =  word, class0_totalCount, class1_totalCount, class0_Cprobability, class1_Cprobability
    else:
        class0_Cprobability_smoothed = (int(class0_totalCount)+1)/float(class0_totalwords + vocab_size) # Laplace +1 Smoothing
        class1_Cprobability_smoothed = (int(class1_totalCount)+1)/float(class1_totalwords + vocab_size) # Laplace +1 Smoothing
        print("{}\t{},{},{},{}".format(word, class0_totalCount ,class1_totalCount, class0_Cprobability_smoothed, class1_Cprobability_smoothed)) 

print("{}\t{},{},{},{}".format(word_C, int(float((class0_totalCount_C))), int(float((class1_totalCount_C))), class0_Cprobability_C, class1_Cprobabilit_C)) 

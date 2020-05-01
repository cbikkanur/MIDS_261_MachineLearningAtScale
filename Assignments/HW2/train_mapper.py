#!/usr/bin/env python
"""
Mapper reads in text documents and emits word counts by class.
INPUT:                                                    
    DocID \t true_class \t subject \t body                
OUTPUT:                                                   
    partitionKey \t word \t class0_partialCount,class1_partialCount       
    

Instructions:
    You know what this script should do, go for it!
    (As a favor to the graders, please comment your code clearly!)
    
    A few reminders:
    1) To make sure your results match ours please be sure
       to use the same tokenizing that we have provided in
       all the other jobs:
         words = re.findall(r'[a-z]+', text-to-tokenize.lower())
         
    2) Don't forget to handle the various "totals" that you need
       for your conditional probabilities and class priors.
       
Partitioning:
    In order to send the totals to each reducer, we need to implement
    a custom partitioning strategy.
    
    We will generate a list of keys based on the number of reduce tasks 
    that we read in from the environment configuration of our job.
    
    We'll prepend the partition key by hashing the word and selecting the
    appropriate key from our list. This will end up partitioning our data
    as if we'd used the word as the partition key - that's how it worked
    for the single reducer implementation. This is not necessarily "good",
    as our data could be very skewed. However, in practice, for this
    exercise it works well. The next step would be to generate a file of
    partition split points based on the distribution as we've seen in 
    previous exercises.
    
    Now that we have a list of partition keys, we can send the totals to 
    each reducer by prepending each of the keys to each total.
       
"""

import re                                                   
import sys                                                  
import numpy as np      

from operator import itemgetter
import os

#################### YOUR CODE HERE ###################
# Intitilizing and updating # of reducers
num_reducers = 2
try:
    num_reducers = os.environ["numReduceTasks"]
except KeyError:
    pass


def makeKeyHash(key, num_reducers):
    """
    Mimic the Hadoop string-hash function.
    
    key             the key that will be used for partitioning
    num_reducers    the number of reducers that will be configured
    """
    byteof = lambda char: int(format(ord(char), 'b'), 2)
    current_hash = 0
    for c in key:
        current_hash = (current_hash * 31 + byteof(c))
    return current_hash % num_reducers

def getPartitionCuts(num_reducers):
    """
    Args:    number of reducers
    Returns: List of characters partitioned in num_reducers groups    
    """
    if num_reducers == 2:
        pCuts = [chr(c) for c in range(ord('a'),  ord('z')+1, 10)]
    else: 
        pCuts = [chr(c) for c in range(ord('a'),  ord('z')+1, 26//(num_reducers-1))]
        
    return pCuts

def getPartitionsFromWord(num_reducers):
    """
    Args:   word to be partitioned, numberof reducers
    Returns:    partition_keys (sorted list of strings)
                partition_values (descending list of char)          
   
    """
    # use the first N uppercase letters as custom partition keys
    N = num_reducers
    partition_cuts = sorted(getPartitionCuts(N), reverse = False)[1:]
    KEYS = list(map(chr, range(ord('A'), ord('Z')+1)))[:N]
    partition_keys = sorted(KEYS, key=lambda k: makeKeyHash(k,N))
    return partition_keys, partition_cuts

pKeys, pCuts = getPartitionsFromWord(num_reducers)
#print(pKeys, pCuts )

# Intitilizing counts
class0_document_total = 0
class1_document_total = 0
class0_wordCount = 0
class1_wordCount = 0

for line in sys.stdin:      
    # parse input
    docID, _class, subject, body = line.split('\t')
    # tokenize
    words = re.findall(r'[a-z]+', (subject + ' ' + body).lower())
    # increment total documnts in each class
    if _class == '0':            
            class0_document_total += 1
    elif _class == '1':           
            class1_document_total += 1
            
    for word in words:
        #pkey = getPartitionsFromWord(word, num_reducers)
        for key,cutpoint in zip(pKeys,pCuts):
            if word[0] < cutpoint:
                pkey = key
                break   
        
        if _class == '0':
            print(f'{pkey}\t{word}\t{1}\t{0}')
            #print("{}\t{}\t{}\t{}".format(pkey, word , 1, 0))
            class0_wordCount += 1
        elif _class == '1':
            print(f'{pkey}\t{word}\t{0}\t{1}')
            #print("{}\t{}\t{}\t{}".format(pkey, word , 0, 1))
            class1_wordCount += 1

KEYS = list(map(chr, range(ord('A'), ord('Z')+1)))[:num_reducers]
partition_keys = sorted(KEYS, key=lambda k: makeKeyHash(k,num_reducers))

for pkey in partition_keys:
        
        print(f'{pkey}\t{"!class0_wordCount"}\t{class0_wordCount}\t{0}')
        print(f'{pkey}\t{"!class1_wordCount"}\t{0}\t{class1_wordCount}')
        print(f'{pkey}\t{"!class0_document_total"}\t{class0_document_total}\t{0}')
        print(f'{pkey}\t{"!class1_document_total"}\t{0}\t{class1_document_total}')
 

#################### (END) YOUR CODE ###################
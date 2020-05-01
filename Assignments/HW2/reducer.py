#!/usr/bin/env python
"""
Reducer takes words with their class and partial counts and computes totals.
INPUT:
    word \t class \t partialCount 
OUTPUT:
    word \t class \t totalCount  
"""
import re
import sys

# initialize trackers
current_word = None
spam_count, ham_count = 0,0

# read from standard input
for line in sys.stdin:
    # parse input
    word, is_spam, count = line.split('\t')
    
############ YOUR CODE HERE #########
    if word == current_word:
        if is_spam == '0':
            ham_count = int(count) + ham_count           
        elif is_spam == '1':
            spam_count = int(count) + spam_count
    else:
        if spam_count != 0:             
            print("{}\t{}\t{}".format(current_word, '1' ,spam_count))
        if ham_count != 0:
            print("{}\t{}\t{}".format(current_word, '0' ,ham_count))
        current_word = word
        if is_spam == '0':
            ham_count = int(count)
            spam_count = 0
        elif is_spam == '1':
            spam_count = int(count)
            ham_count = 0
        
if ham_count != 0:             
    print("{}\t{}\t{}".format(current_word,'0',ham_count))
if spam_count != 0: 
    print("{}\t{}\t{}".format(current_word,'1',spam_count))


############ (END) YOUR CODE #########
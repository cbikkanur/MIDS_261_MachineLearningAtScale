#!/usr/bin/env python
"""
This script reads word counts from STDIN and aggregates
the counts for any duplicated words.

INPUT & OUTPUT FORMAT:
    word \t count
USAGE (standalone):
    python aggregateCounts_v2.py < yourCountsFile.txt

Instructions:
    For Q7 - Your solution should not use a dictionary or store anything   
             other than a single total count - just print them as soon as  
             you've added them. HINT: you've modified the framework script 
             to ensure that the input is alphabetized; how can you 
             use that to your advantage?
"""

# imports
import sys



################# YOUR CODE HERE #################

word0 = 'a'
count0 = 0
for line in sys.stdin: 
   word, count  = line.split()
   if word == word0:
        count = int(count) + count0
        count0 = count
   else:
       print("{}\t{}".format(word0,count0))
       word0 = word
       count0 = int(count)

################ (END) YOUR CODE #################

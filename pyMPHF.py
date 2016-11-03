# (Minimal) Perfect Hash Functions Generator (key, value) value in this code is the key counter during reading but can be any number

# implementing the MOS Algorithm II CACM92 , and Amjad M Daoud Thesis 1993 at VT; 
# based on Steve Hanof implementation http://stevehanov.ca/blog/index.php?id=119.

# Download as http://iswsa.acm.org/mphf/mphf.py

# You need Python; runs linearly even on a Android phone; it runs without modifications at http://www.compileonline.com/execute_python_online.php

# For minimal perfect hashing use:  size = len(dict)

import sys

import math

# first level simple hash ... used to disperse patterns using random d values

def hash( d, str ):

    #if d == 0: d = 0x01000193

    if d == 0: d =   0x811C9DC5

    # Use the FNV-1a hash

    for c in str:

        #h = (h ^ p[i]) * 16777619
        #d = ( (d * 0x01000193) ^ ord(c) ) & 0xffffffff;

        d = d ^ ord(c) * 16777619 & 0xffffffff

    return d 

def isprime(x):

	x = abs(int(x))

	if x < 2:

		return "Less 2", False

	elif x == 2:

		return True

	elif x % 2 == 0:

		return False	

	else:

		for n in range(3, int(x**0.5)+2, 2):

			if x % n == 0:

				return False

		return True

def nextprime(x):

    while ( True ):

       if isprime(x): break

       x += 1

    return x  

# create PHF with MOS(Map,Order,Search), g is specifications array

def CreatePHF( dict ):

    size = len(dict) 

    size = nextprime(len(dict)+len(dict)/4)

    print "Size = %d" % (size)

    #nextprime(int(size/(6*math.log(size,2)))) 
    #c=4 corresponds to 4 bits/key
    # for fast construction use size/5
    # for faster construction use gsize=size
    gsize = size/5 

    print "G array size = %d" % (gsize)

    sys.stdout.flush()

 

    #Step 1: Mapping

    patterns = [ [] for i in range(gsize) ]

    g = [0] * gsize #initialize g

    values = [None] * size #initialize values

    

    for key in dict.keys():

        patterns[hash(0, key) % gsize].append( key )

 

    # Step 2: Sort patterns in descending order and process 

    patterns.sort( key= len, reverse=True )        

    for b in xrange( gsize ):

        pattern = patterns[b]

        if len(pattern) <= 1: break

        

        d = 1

        item = 0

        slots = []

 

    # Step 3: rotate patterns and search for suitable displacement

        while item < len(pattern):

            slot = hash( d, pattern[item] ) % size

            if values[slot] != None or slot in slots:

                d += 1

                if d < 0 : break

                item = 0

                slots = []

            else:

                slots.append( slot )

                item += 1

 

        if d < 0: 

           print "failed"

           return

           

        g[hash(0, pattern[0]) % gsize] = d

        for i in range(len(pattern)):

            values[slots[i]] = dict[pattern[i]]

 

        if ( b % 100 ) == 0:

           print "%d: pattern %d processed" % (b,len(pattern))

           sys.stdout.flush()

 

    # Process patterns with one key and use a negative value of d 

    freelist = []

    for i in xrange(size): 

        if values[i] == None: freelist.append( i )

 

    for b in xrange(b+1,gsize ):

        pattern = patterns[b]

        if len(pattern) == 0: break

        #if len(pattern) > 1: continue;

        slot = freelist.pop()

        # subtract one to handle slot zero

        g[hash(0, pattern[0]) % gsize] = -slot-1 

        values[slot] = dict[pattern[0]]

        

        if (b % 1000) == 0:

           print "-%d: pattern %d processed" % (b,len(pattern))

           sys.stdout.flush()

    print "PHF succeeded"

    return (g, values)        

    

# Look up a value in the hash table, defined by g and V.

def lookup( g, V, key ):

    d = g[hash(0,key) % len(g)]

    if d < 0: return V[-d-1]

    return V[hash(d, key) % len(V)]

    

# main program

 

#reading keyset size is given by num

DICTIONARY = "dict.txt"

 

num = 100000

print "Reading %d Unix user dict words"% (num)

dict = {}

line = 1

for key in open(DICTIONARY, "rt").readlines():

    dict[key.strip()] = line

    line += 1

    if line > num: break

 

#creating phf

print "Creating perfect hash for the first %d Unix user dict words"% (num)

(g, V) = CreatePHF( dict )

 

#printing phf specification

print "Printing g[] for Unix user dict"

print g

 

#fast verification for few (key,value) count given by num1

num1 = 5

print "Verifying hash values for the first %d words"% (num1)

line = 1

for key in open(DICTIONARY, "rt").readlines():

    line = lookup( g, V, key.strip() )

    print "Word %s occurs on line %d" % (key.strip(), line)

    line += 1

    if line > num1: break
   

#!/usr/bin/python
import sys
# number of edges to draw is passed as a command-line parameter

fileName = "ulam.txt"
numEdges = int(sys.argv[1]) / 2
current = 1
vector = [1, 0]
delta = [-1, -1]
pos = [0, 0]

# delete the current contents of the file
f = open(fileName, 'w')
f.seek(0)
f.truncate()

def progress():
    for i in xrange(2):
        pos[i] += vector[i]

def turn():
    for i in xrange(2):
        if vector[i] == 1:
            delta[i] = -1
        elif vector[i] == -1:
            delta[i] = 1

        vector[i] += delta[i]

def isPrime(n):
        d = 2
        while d * d <= n:
            if n % d == 0:
                return False
            d += 1
            
        return n > 1

for progressionCount in xrange(1, numEdges + 1):
    for j in xrange(2):
        for step in xrange(progressionCount):
            if isPrime(current):
                f.write("%d %d\n" % (pos[0], pos[1]))
            current += 1
            progress()
        turn()

f.close()

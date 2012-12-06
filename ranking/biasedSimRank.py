#!/usr/bin/env python
'''
Input: user-file-graph, simrank.pickled
Output: simrank-biased.txt
'''
import pickle
import sys
import math
import sagh

DEFAULT_POPULARITY_BIAS = 0.5

popularityBias = float(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_POPULARITY_BIAS
graphFileName = sagh.suffixWithArgs('user-file-graph', 1)
tableFileName = sagh.suffixWithArgs('user-user-simrank', 1)
biasedTableFileName = sagh.suffixWithArgs('user-user-simrank.biased', 2)

print >>sys.stderr, "loading %s" % graphFileName
graph = pickle.load(open(graphFileName))
print >>sys.stderr, "loading %s" % tableFileName
score = pickle.load(open(tableFileName))

lDevelopers = []
for node in graph.nodes(data=True):
    if (node[1]['type']=='Developer'): lDevelopers.append(node[0])
numDevs = len(lDevelopers)

biasedScore = {}
for i in range(numDevs):
    if i % (numDevs / 10) == 0:
        print >>sys.stderr, "%d developers done so far" % i
    for j in range(i+1, numDevs):
        biasedScore[(i,j)] = score[(i,j)] * pow(len(graph.neighbors(lDevelopers[j])), popularityBias)
        biasedScore[(j,i)] = score[(i,j)] * pow(len(graph.neighbors(lDevelopers[i])), popularityBias)

for i in range(numDevs):
    # to normalize, we need 2-passes
    biasedScore_i = [None] * numDevs
    # first, collect the values and compute max
    for j in range(numDevs):
        if i == j: continue
        biasedScore_i[j] = biasedScore[(i,j)]
    max_i = max(biasedScore_i)
    if max_i > 0:
        for j in range(numDevs):
            if i == j: continue
            s = biasedScore_i[j]
            if s > 0:
                print lDevelopers[i], lDevelopers[j], s / max_i #, s


print >>sys.stderr, "storing %s" % biasedTableFileName
pickle.dump(biasedScore, open(biasedTableFileName, 'w'))

#!/usr/bin/env python
'''
Input: Commit Log File from standard input
Output: Pickled bipartite developers-files graph in DF-graph.txt
'''

import networkx as nx
from collections import defaultdict
import pickle
import sys
import re
import sagh

graphFileName = 'user-file-graph'

DFbipartite = nx.Graph()
flag = False
count  = 1

author_id = '';
for line in sys.stdin:
    
    if (flag==True and line=="\n"):
            count-=1
            continue
            
    if ('files changed' in line or 'file changed' in line): 
        count=1
        flag = False
        continue
    
    if (count==0):
        file_name = line[0:line.find('|')].strip()
        #print file_name
        DFbipartite.add_node(file_name, type='File')
        if (author_id, file_name) in DFbipartite.edges():
            data= DFbipartite.get_edge_data(author_id, file_name)
            DFbipartite.add_edge(author_id,file_name, w=data['w']+1)
        else: DFbipartite.add_edge(author_id,file_name, w=1)
        continue
        
    if 'Author:' in line:
        flag = True
        author_id = line[len('Author: '):].strip()
        author_id = re.sub(r'\s+', '', author_id)
        
        #print
        #print author_id, author_name
        DFbipartite.add_node(author_id, type='Developer')
        #print >>sys.stderr, author_id
    
pickle.dump(DFbipartite, open(graphFileName, 'w'))

graph = DFbipartite
score = defaultdict(int)
lDeveloper = []

for files in graph.nodes(data=True):
    
    if(files[1]['type']!='File'): continue
    lDeveloper = graph.neighbors(files[0])
    
    for i in range(len(lDeveloper)):
        for j in range(i+1,len(lDeveloper)):
            score[(lDeveloper[i],lDeveloper[j])] += 1
            score[(lDeveloper[j],lDeveloper[i])] += 1
  
lDeveloper = []  
for developer in graph.nodes(data=True):
    if(developer[1]['type']!='Developer'): continue
    lDeveloper.append(developer[0])

#Output the scores of the graph
#f = open('DD-score.txt', 'w')

for i in range(len(lDeveloper)):
    for j in range(i+1,len(lDeveloper)):
        s = score[(lDeveloper[i],lDeveloper[j])]
        if s > 0:
            print "%s\t%s\t%d" % (lDeveloper[i], lDeveloper[j], s)
            #f.write(lDeveloper[i]+'\t'+lDeveloper[j]+'\t'+str(score[(lDeveloper[i],lDeveloper[j])])+'\n')

#f.close()

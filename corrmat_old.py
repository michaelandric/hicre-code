#!/usr/bin/python

import pandas as pd
import numpy as np
import networkx as nx
from community import *

df = pd.read_csv('hicre4andric.csv')
groups = set(df.loc[:,'group (CB, LB)'])   # set(df.iloc[:,4]) also works for this

for g in groups:
    g = df[df.loc[:,'group (CB, LB)'] == g]

#subsetting the data
CB = df[df.iloc[:,4] == 'CB'].iloc[:,5:31]
LB = df[df.iloc[:,4] == 'LB'].iloc[:,5:31]
scb = df[df.iloc[:,4] == 'scb'].iloc[:,5:31]
slb = df[df.iloc[:,4] == 'slb'].iloc[:,5:31]

CBcorr = np.triu(CB.corr()) 
np.fill_diagonal(CBcorr, 0)

CBsrtd = np.sort(CBcorr[CBcorr != 0])
threshd = CBsrtd[int(len(CBsrtd)*.5):]
ix = np.in1d(CBcorr.ravel(), threshd).reshape(CBcorr.shape)

inds = zip(np.where(ix)[0], np.where(ix)[1])

G = nx.Graph()
for ii in inds:
    G.add_edge(ii[0], ii[1])

bestpart = best_partition(G)
modscore = modularity(bestpart, G)
#deg = np.mean(nx.degree(G).values())

'''For random graph'''
np.mean(nx.degree(G).values())

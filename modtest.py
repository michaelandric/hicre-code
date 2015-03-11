#!/usr/bin/python

import pandas as pd
import numpy as np
import networkx as nx
from community import *

df = pd.read_csv('hicre4andric.csv')
groups = set(df.loc[:,'group (CB, LB)'])   # set(df.iloc[:,4]) also works for this


dat = df[df.iloc[:,4] == g].iloc[:,5:31]

def frange(x, y, jump):
    while x < y:
        yield x
        x += jump

def get_modularity(dat, thresh_density, niter):
    '''
    This returns the max Q value of niter solutions
    dat: the data, formatted as a matrix
    thresh_density: the graph density to threshold by
    niter: number of iterations to maximize over
    '''
    datcorr = np.triu(dat.corr())
    np.fill_diagonal(datcorr, 0)
    datsrtd = np.sort(datcorr[datcorr != 0])
    threshd = datsrtd[int(len(datsrtd)*thresh_density):]
    ix = np.in1d(datcorr.ravel(), threshd).reshape(datcorr.shape)
    inds = zip(np.where(ix)[0], np.where(ix)[1])
    G = nx.Graph()
    for ii in inds:
        G.add_edge(ii[0], ii[1])
    modscores = np.empty(niter)
    for i in xrange(niter):
        part = best_partition(G)
        modscores[i] = modularity(bestpart, G)
    #return np.max(modscores)
    return modscores


for g in groups:
    dat = df[df.iloc[:,4] == g].iloc[:,5:31]
    for i in frange(.25,.75,.05):
        get_modularity(dat, i, 100)


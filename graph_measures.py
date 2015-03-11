#!~/anaconda/bin/python

import pandas as pd
import numpy as np
import networkx as nx
import random
import os
from community import *
from shlex import split
from subprocess import call

def get_graph(dat, thresh_density, outname):
    '''
    This returns the max Q value of niter solutions
    dat: the data, formatted as a matrix
    thresh_density: the graph density to threshold by
    niter: number of iterations to maximize over
    '''
    datcorr = np.triu(dat.corr())
    np.fill_diagonal(datcorr, 0)
    datsrtd = np.sort(datcorr[datcorr != 0])
    threshd = datsrtd[int(len(datsrtd)*(1-thresh_density)):]
    ix = np.in1d(datcorr.ravel(), threshd).reshape(datcorr.shape)
    inds = zip(np.where(ix)[0], np.where(ix)[1])
    G = nx.Graph()
    for ii in inds:
        G.add_edge(ii[0], ii[1])
    nx.write_edgelist(G, outname, data=False)

def get_modularity(edgelist, treeoutname, modscorename):
    f = open(treeoutname, 'w')
    m = open(modscorename, 'w')
    cmdargs = split('/home/michaeljames.andric/Community_latest/community -l -1 '+edgelist+'.bin')
    call(cmdargs, stdout=f, stderr=m)
    f.close()
    m.close()

def get_rand_graph(graph, outname):
    randn = nx.random_regular_graph(int(np.mean(graph.degree().values())), 148) 
    nx.write_edgelist(randn, outname, data=False)

def get_rand_modularity(edgelist, modscorename):
    m = open(modscorename, 'w')
    cmdargs = split('/home/michaeljames.andric/Community_latest/community -l -1 '+edgelist+'.bin')
    call(cmdargs, stdout=open(os.devnull, 'wb'), stderr=m)   # this for the random graphs, not saving trees so took away stdout
    m.close()

def get_degrees(graph, outname):
    deg = graph.degree()
    zd = [i for i in range(0,148) if i not in deg.keys()]
    ZeroD = dict(zip(zd, np.zeros(len(zd), dtype=np.int8)))
    outD = dict(deg, **ZeroD)
    f = open(outname, 'w')
    f.write('\n'.join(map(str, outD.values())))
    f.close()

def get_betweenness_centrality(graph, outname):
    bc = nx.betweenness_centrality(graph)
    zd = [i for i in range(0,148) if i not in bc.keys()]
    ZeroD = dict(zip(zd, np.zeros(len(zd), dtype=np.int8)))
    outD = dict(bc, **ZeroD)
    f = open(outname, 'w')
    f.write('\n'.join(map(str, outD.values())))
    f.close()

def get_edge_betweenness_centrality(graph, outname):
    ebc = nx.edge_betweenness_centrality(graph)
    zd = [i for i in range(0,148) if i not in ebc.keys()]
    ZeroD = dict(zip(zd, np.zeros(len(zd), dtype=np.int8)))
    outD = dict(ebc, **ZeroD)
    f = open(outname, 'w')
    f.write('\n'.join(map(str, outD.values())))
    f.close()


def get_shortest_path_length(graph, outname):
    sp = nx.shortest_path_length(graph)
    zd = [i for i in range(0,148) if i not in sp.keys()]
    ZeroD = dict(zip(zd, np.zeros(len(zd), dtype=np.int8)))
    outD = dict(sp, **ZeroD)
    f = open(outname, 'w')
    f.write('\n'.join(map(str, outD.values())))
    f.close()

if __name__ == "__main__":
    groups = ['CB', 'SCB', 'LB', 'SLB']
    for g in groups:
        for i in np.arange(.10,.61,.1):
            edgelist = '/home/michaeljames.andric/hicre/graphs/%s_dens%s.edgelist' % (g, i)
            outname = '/home/michaeljames.andric/hicre/shortest_path_length/%s_dens%s.spl' % (g, i)
            graph = nx.read_edgelist(edgelist, nodetype=int)
            #get_degrees(graph, outname)
            #get_betweenness_centrality(graph, outname)
            get_shortest_path_length(graph, outname)



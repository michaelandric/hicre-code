#!~/anaconda/bin/python

import pandas as pd
import numpy as np
import networkx as nx
import random
import os
from community import *
from shlex import split
from subprocess import call

def frange(x, y, jump):
    while x < y:
        yield x
        x += jump

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

def get_rand_modularity(edgelist, treeoutname, modscorename):
    m = open(modscorename, 'w')
    f = open(treeoutname, 'w')
    cmdargs = split('/home/michaeljames.andric/Community_latest/community -l -1 '+edgelist+'.bin')
    #call(cmdargs, stdout=open(os.devnull, 'wb'), stderr=m)   # this for the random graphs, not saving trees so took away stdout
    call(cmdargs, stdout=f, stderr=m)   # this for the random graphs, saving trees 
    m.close()
    f.close()



if __name__ == "__main__":
    #df = pd.read_csv('hicre4andric.csv')
    df = pd.read_csv('CTallregionsBOTH.csv')
    #groups = set(df.loc[:,'group (CB, LB)'])   # set(df.iloc[:,4]) also works for this
    groups = set(df.loc[:,'Group'])   # set(df.iloc[:,4]) also works for this
    #for g in groups: ALREADY DID 'SCB' AND 'SLB' BECAUSE URI GAVE ME ONLY PART OF THE DATA
    """for nn in xrange(100):
        scb1 = random.sample(df[df.loc[:,'Group']=='SCB'].index.tolist(), 9)
        cb1 = random.sample(df[df.loc[:,'Group']=='CB'].index.tolist(), 9)
        dat = df.iloc[random.sample(scb1+cb1, len(scb1+cb1)),3:]
        g = 'Null_CB'
        for i in np.arange(.1,.61,.1):
            outname = '/home/michaeljames.andric/hicre/null_graphs/%s_dens%s.graph%s.edgelist' % (g, i, nn)
            get_graph(dat, i, outname)
            cmdargs = split('community_convert -i '+outname+' -o '+outname+'.bin')
            call(cmdargs)
            graph = nx.read_edgelist(outname)
            for n in xrange(100):
                treeoutname = '/home/michaeljames.andric/hicre/null_trees/%s_dens%s_tree.graph%s.iter%s.tree' % (g, i, nn, n)
                modscorename = '/home/michaeljames.andric/hicre/null_Qvals/%s_dens%s.graph%s.iter%s.Qval' % (g, i, nn, n)
                get_modularity(outname, treeoutname, modscorename)
                randgraphname = '/home/michaeljames.andric/hicre/null_random_graphs/rand_%s_dens%s_edgelist.graph%s.iter%s.txt' % (g, i, nn, n)
                get_rand_graph(graph, randgraphname)
                cmdargsRand = split('community_convert -i '+randgraphname +'  -o '+randgraphname +'.bin')
                call(cmdargsRand)
                rand_Q_name = '/home/michaeljames.andric/hicre/null_random_Qvals/rand_%s_dens%s.graph%s.iter%s.Qval' % (g, i, nn, n)
                get_rand_modularity(randgraphname, rand_Q_name)"""
    

    """Orig section for runs. Above doing resample effort"""
    for g in ['CB','SCB','LB','SLB']:
        #dat = df[df.iloc[:,4] == g].iloc[:,5:31]
        #dat = df[df.loc[:,'Group'] == g].iloc[:,3:]
        for i in np.arange(.10,.61,.1):
            #outname = '/home/michaeljames.andric/hicre/graphs/%s_dens%s.edgelist' % (g, i)
            #get_graph(dat, i, outname)
            #cmdargs = split('community_convert -i '+outname+'  -o '+outname+'.bin')
            #call(cmdargs)
            #graph = nx.read_edgelist(outname)
            for n in xrange(100):
                #treeoutname = '/home/michaeljames.andric/hicre/trees/%s_dens%s_tree.iter%s.tree' % (g, i, n)
                #modscorename = '/home/michaeljames.andric/hicre/Qvals/%s_dens%s.iter%s.Qval' % (g, i, n)
                #get_modularity(outname, treeoutname, modscorename)
                randgraphname = '/home/michaeljames.andric/hicre/random_graphs/rand_%s_dens%s_edgelist.iter%s.txt' % (g, i, n)
                #get_rand_graph(graph, randgraphname)
                #cmdargsRand = split('community_convert -i '+randgraphname +'  -o '+randgraphname +'.bin')
                #call(cmdargsRand)
                rand_Q_name = '/home/michaeljames.andric/hicre/random_Qvals/rand_%s_dens%s.iter%s.Qval' % (g, i, n)
                rand_treename = '/home/michaeljames.andric/hicre/random_trees/rand_%s_dens%s.iter%s.tree' % (g, i, n)
                get_rand_modularity(randgraphname, rand_treename, rand_Q_name) 


#!~/anaconda/bin/python

import pandas as pd
import numpy as np
import networkx as nx
import os
from community import *
from shlex import split
from subprocess import call
from glob import glob
from scipy.stats import ks_2samp

niter = 100
groups = ['CB', 'LB', 'SCB', 'SLB']
cols = list(groups)
for i in np.arange(.1,.61,.1):
    dat = np.array([np.zeros(niter)]*4).T
    df = pd.DataFrame(dat, columns=cols)
    for g in groups: 
        print g
        filelist = glob('Qvals/%s*dens%s*Qval' % (g, i))   # specify 'g' for group and 'i' for density level
        nfiles = len(filelist)
        Qs = np.array(np.zeros(nfiles))
        for n in xrange(nfiles):
            with open('Qvals/%s_dens%s.iter%s.Qval' % (g, i, n), 'r') as f:
            #with open(filelist[n], 'r') as f:
                Qs[n] = f.readline()
        df.loc[:,g] = Qs
    df.to_csv('Qscores_all_dens%s.csv' % i)

print ks_2samp(df.loc[:,'CB'], df.loc[:,'LB'])
print ks_2samp(df.loc[:,'CB'], df.loc[:,'scb'])
print ks_2samp(df.loc[:,'CB'], df.loc[:,'slb'])
print ks_2samp(df.loc[:,'LB'], df.loc[:,'scb'])
print ks_2samp(df.loc[:,'LB'], df.loc[:,'slb'])
print ks_2samp(df.loc[:,'scb'], df.loc[:,'slb'])

'''for random Q vals'''
for i in np.arange(.1,.61,.1):
    randdat = np.array([np.zeros(niter)]*4).T
    dfr = pd.DataFrame(randdat, columns=cols)
    for g in groups:
        randfiles = glob('random_Qvals/*%s*dens%s*Qval' % (g, i))
        nfiles = len(randfiles)
        randQs = np.array(np.zeros(nfiles))
        for rr in xrange(nfiles):
            with open(randfiles[rr], 'r') as f:
                randQs[rr] = f.readline()
        dfr.loc[:,g] = randQs
    dfr.to_csv('randQscores_dens%s' % i )



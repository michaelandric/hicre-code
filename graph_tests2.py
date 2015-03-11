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
ngraphs = 100
groups = ['CB', 'LB', 'SCB', 'SLB']
cols = list(groups)
#cols = ['NullCB']
"""for i in np.arange(.1,.61,.1):
    #dat = np.array([np.zeros(niter*ngraphs)]).T
    dat = np.array([np.zeros(ngraphs)]).T
    df = pd.DataFrame(dat, columns=cols)
    st = 0
    en = 100
    for nn in np.arange(100):
        filelist = glob('null_Qvals/Null_CB_dens%s.graph%s.*Qval' % (i, nn))   # specify 'g' for group and 'i' for density level
        nfiles = len(filelist)
        Qs = np.array(np.zeros(nfiles))
        for n in xrange(nfiles):
            with open(filelist[n], 'r') as f:
                Qs[n] = f.readline()
        #df.iloc[st:en,0] = Qs
        df.iloc[nn,0] = np.max(Qs)
        #st=st+100
        #en=en+100
    df.to_csv('Null_Qscores_maxQ_dens%s.csv' % i)"""

for i in np.arange(.1,.61,.1):
    dat = np.array([np.zeros(niter)]*len(groups)).T
    df = pd.DataFrame(dat, columns=cols)
    for g in groups: 
        print g
        #filelist = glob('Qvals/%s*dens%s*Qval' % (g, i))   # specify 'g' for group and 'i' for density level
        #filelist = glob('N_mods/%s*dens%s*.Nmods' % (g, i))   # specify 'g' for group and 'i' for density level
        filelist = glob('N_mods_nonSingle/%s*dens%s*.Nmods' % (g, i))   # specify 'g' for group and 'i' for density level
        #filelist = glob('random_N_mods/rand_%s_dens%s*.Nmods' % (g, i))   # specify 'g' for group and 'i' for density level
        #filelist = glob('random_N_mods_nonSingle/rand_%s_dens%s*.Nmods' % (g, i))   # specify 'g' for group and 'i' for density level
        #filelist = glob('null_Qvals/%s*dens%s*Qval' % (g, i))   # specify 'g' for group and 'i' for density level
        nfiles = len(filelist)
        Qs = np.array(np.zeros(nfiles))
        for n in xrange(nfiles):
            with open(filelist[n], 'r') as f:
                Qs[n] = f.readline()
        df.loc[:,g] = Qs
    #df.to_csv('Qscores_all_dens%s.csv' % i)
    #df.to_csv('N_modules_all_dens%s.csv' % i)
    #df.to_csv('Null_Qscores_all_dens%s.csv' % i)
    #df.to_csv('rand_N_modules_all_dens%s.csv' % i)
    #df.to_csv('rand_N_modules_all_nonSingle_dens%s.csv' % i)
    df.to_csv('N_modules_all_nonSingle_dens%s.csv' % i)

#print ks_2samp(df.loc[:,'CB'], df.loc[:,'LB'])
#print ks_2samp(df.loc[:,'CB'], df.loc[:,'scb'])
#print ks_2samp(df.loc[:,'CB'], df.loc[:,'slb'])
#print ks_2samp(df.loc[:,'LB'], df.loc[:,'scb'])
#print ks_2samp(df.loc[:,'LB'], df.loc[:,'slb'])
#print ks_2samp(df.loc[:,'scb'], df.loc[:,'slb'])

'''for random Q vals
for i in np.arange(.1,.61,.1):
    randdat = np.array([np.zeros(niter)]*len(groups)).T
    dfr = pd.DataFrame(randdat, columns=cols)
    for g in groups:
        randfiles = glob('random_Qvals/*_%s*dens%s*Qval' % (g, i))
        nfiles = len(randfiles)
        randQs = np.array(np.zeros(nfiles))
        for rr in xrange(nfiles):
            with open(randfiles[rr], 'r') as f:
                randQs[rr] = f.readline()
        dfr.loc[:,g] = randQs
    dfr.to_csv('randQscores_dens%s' % i )
'''


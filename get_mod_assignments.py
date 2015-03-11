#!~/anaconda/bin/python

import pandas as pd
import numpy as np
import networkx as nx

dfcols = ['region', 'community']
groups = ['SCB']
for i in np.arange(.1,.11,.1):
    df = pd.read_csv('Qscores_all_dens%s.csv' % i)
    ct = pd.read_csv('CTallregionsBOTH.csv')
    ctnames = pd.Series(ct.columns[3:151])
    for g in groups:
        maxiter = df.loc[:,g].argmax()
        cols = ['nodes', 'coms']
        tree = pd.DataFrame(np.loadtxt('tree_highest/%s_dens%s_tree.iter%s.highesttree' % (g, i, maxiter)), columns=cols)
        G = nx.read_edgelist('graphs/%s_dens%s.edgelist' % (g, i), nodetype=int)
        tree = tree.iloc[G.nodes(),:]
        #newd = pd.DataFrame(np.array([np.arange(tree.shape[0])]*2).T, columns=dfcols)
        nnames = []
        modid = []
        for com in set(tree.loc[:,'coms']):
            list_nodes = map(int, tree.loc[:,'nodes'][tree.loc[:,'coms']==com])
            nnames.append(ctnames[list_nodes])
            modid.append(np.repeat(com, len(list_nodes)))
            #nn.to_csv('%s_mod%s.inclusionlist.csv' % (g, com))
        nnames = list(np.concatenate(nnames))
        modid = list(np.concatenate(modid))
        newd = pd.DataFrame(zip(nnames, modid), columns=dfcols)
        newd.to_csv('%s.inclusionlist.csv' % g)
        


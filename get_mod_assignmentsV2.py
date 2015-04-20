# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 17:18:49 2015

@author: andric
"""

import os
import pandas as pd
import numpy as np
import networkx as nx

dfcols = ['region', 'community']
cols = ['nodes', 'coms']
groups = ['CB', 'SCB']

hr_dir = 'hicre/regular'
base_dir = os.path.join(os.environ['t2'], hr_dir)
os.chdir(base_dir)
print 'Now working in '
print os.getcwd()
modularity_dir = 'modularity'
tree_dir = 'tree_highest'
graph_dir = 'graphs'

ct = pd.read_csv('CTallregionsBOTH.csv')
ctnames = pd.Series(ct.columns[3:151])

for dens in ['0.2', '0.3', '0.4', '0.5', '0.6']:
    for g in groups:
        qscores = '%s.dens_%s.Qval' % (g, dens)
        dat = np.genfromtxt(os.path.join(modularity_dir, qscores))
        maxiter = dat.argmax()
        print 'Group: %s, density: %s, maxiter: %d' % (g, dens, maxiter)
        tree_name = 'iter%d.%s.dens_%s.tree_highest' % (maxiter, g, dens)
        tree_name_path = os.path.join(tree_dir, tree_name)
        tree = pd.DataFrame(np.loadtxt(tree_name_path), columns=cols)
        G_name = '%s.dens_%s.edgelist.gz' % (g, dens)
        G = nx.read_edgelist(os.path.join(graph_dir, G_name), nodetype=int)
        tree = tree.iloc[G.nodes(), :]
        nnames = []
        modid = []
        for com in set(tree.loc[:, 'coms']):
            list_nodes = map(int,
                             tree.loc[:, 'nodes'][tree.loc[:, 'coms'] == com])
            nnames.append(ctnames[list_nodes])
            modid.append(np.repeat(com, len(list_nodes)))
        nnames = list(np.concatenate(nnames))
        modid = list(np.concatenate(modid))
        newd = pd.DataFrame(zip(nnames, modid), columns=dfcols)
        mod_list_name = '%s.inclusionlist.dens_%s.csv' % (g, dens)
        newd.to_csv(os.path.join(base_dir, mod_list_name))

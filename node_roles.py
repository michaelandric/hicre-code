#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 16:23:40 2015

@author: andric
"""

import os
import networkx as nx
import bct
import pandas as pd
import numpy as np


def make_networkx_graph(n_nodes, edgelist_name):
    g = nx.Graph()
    g.add_nodes_from(range(n_nodes))
    ed = nx.read_edgelist(edgelist_name, nodetype=int)
    g.add_edges_from(ed.edges())
    return g


def mymodule_degree_zscore(W, Ci, flag=0):
    """
    The within-module degree z-score is a within-module version of degree
    centrality.
    Inputs:     W,      binary/weighted, directed/undirected connection matrix
               Ci,      community affiliation vector
             flag,		0: undirected graph = default
                        1: directed graph in degree
                        2: directed graph out degree
                        3: directed graph in and out degree
    Output:     Z,      within-module degree z-score.
    Note: The output for directed graphs is the "out-neighbor" z-score.
    """
    if flag == 2:
        W = W.copy()
        W = W.T
    elif flag == 3:
        W = W.copy()
        W = W + W.T
    n = len(W)
    Z = np.zeros((n, ))
    for i in xrange(int(np.max(Ci))+1):
        Koi = np.sum(W[np.ix_(Ci == i, Ci == i)], axis=1)
        Z[np.where(Ci == i)] = (Koi-np.mean(Koi))/np.std(Koi)

    Z[np.where(np.isnan(Z))] = 0
    return Z


if __name__ == '__main__':

    dat_dir = '/Users/andric/Documents/workspace/hicre/'
    graph_dir = dat_dir+'/graphs/'
    role_dir = dat_dir+'/node_roles'
    if not os.path.exists(role_dir):
        os.makedirs(role_dir)
    nnodes = 148
    cols = ['nodes', 'coms']
    for subjid in ['CB', 'SCB']:
        thresh_dens = '0.1'
        qscores = 'Qscores_all_dens%s.csv' % thresh_dens
        df = pd.read_csv(os.path.join(dat_dir, qscores))
        maxiter = df.loc[:, subjid].argmax()
        tree_loc = 'tree_highest'
        tree_name = '%s_dens%s_tree.iter%s.highesttree' % \
            (subjid, thresh_dens, maxiter)
        tree_in = os.path.join(dat_dir, tree_loc, tree_name)
        tree = pd.DataFrame(np.loadtxt(tree_in), columns=cols)
        coms = tree.loc[:, 'coms']

        graph_name = '%s_dens%s.edgelist' % (subjid, thresh_dens)
        g = make_networkx_graph(nnodes, os.path.join(graph_dir, graph_name))
        ga = nx.adjacency_matrix(g).toarray()

        pc = bct.participation_coef(ga, coms)
        wz = bct.module_degree_zscore(ga, coms)

        pc_out_name = '%s_dens%s_part_coef.txt' % (subjid, thresh_dens)
        np.savetxt(os.path.join(role_dir, pc_out_name), pc, fmt='%.4f')
        wz_out_name = '%s_dens%s_within_mod_Z.txt' % (subjid, thresh_dens)
        np.savetxt(os.path.join(role_dir, wz_out_name), wz, fmt='%.4f')

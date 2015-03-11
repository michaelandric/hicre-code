#!~/anaconda/bin/python

import math
import numpy as np
import pandas as pd
import networkx as nx
from community import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import pygraphviz

def make_plot(graph, tree, ctnames, outname, g):
    gprog = 'nxcircular'
    G = graph
    ebc = nx.edge_betweenness_centrality(G)
    for e in G.edges():
        G.add_edge(e[0], e[1], weight=ebc[e]*20)
    tree = tree.iloc[G.nodes(),:]
    #pos = nx.graphviz_layout(G, prog=gprog)
    pos = nx.circular_layout(G)
    #acc = plt.get_cmap('hsv')
    """com_norm = (tree.loc[:,'coms'] - tree.loc[:,'coms'].min()) / (tree.loc[:,'coms'].max() + tree.loc[:,'coms'].min())
    acc_dict = dict(zip(sorted(map(int, set(tree.loc[:,'coms']))), sorted(set(com_norm))))
    nodecolors = [acc(acc_dict[nn]) for nn in map(int, tree.loc[:,'coms'])]"""
    n_coms = len(tree['coms'])
    new_rgb = np.array(np.zeros(n_coms*3)).reshape(n_coms, 3)
    clrs = pd.read_csv('colorsSCB_CB.csv')
    clrs_frc = []
    for i in xrange(len(clrs.loc[:,'colorRGB'])):
                clrs_frc.append([round(num/255.,5) for num in map(int, clrs.loc[:,'colorRGB'][i].split())])
    tt = clrs[clrs.loc[:,'group']==g]
    for i in xrange(n_coms):
        new_rgb[i,:] = clrs_frc[tt[tt['module']==tree.iloc[i,]['coms']].index[0]]
    new_rgb = np.column_stack((new_rgb, np.repeat(1, n_coms)))
    #nodesizes = [(v)*4000 for v in nx.betweenness_centrality(G).values()]
    nodesizes = [G.degree(v)*10 for v in G]
    #nx.draw_networkx_nodes(G, pos, node_size=nodesizes, node_color = nodecolors)
    nx.draw_networkx_nodes(G, pos, node_size=nodesizes, node_color = new_rgb)
    nx.draw_networkx_edges(G, pos, width=[w['weight'] for (u,v,w) in G.edges(data=True)])
    #nx.draw_networkx_labels(G, pos, ctnames, font_size=7)
    plt.axis('off')
    plt.savefig('names.%s.%s' % (gprog, outname))
    plt.hold(False)
    for com in set(tree.loc[:,'coms']):
        com = int(com)
        list_nodes = map(int, tree.loc[:,'nodes'][tree.loc[:,'coms']==com])
        thiscom_sizes = [nodesizes[i[0]] for i in enumerate(G.nodes()) if i[1] in list_nodes]
        #subpos = nx.graphviz_layout(G.subgraph(list_nodes), prog=gprog)
        subpos = nx.circular_layout(G.subgraph(list_nodes))
        #nx.draw_networkx_nodes(G.subgraph(list_nodes), pos, list_nodes, node_size=thiscom_sizes, node_color=acc(acc_dict[com]))
        #nx.draw_networkx_nodes(G.subgraph(list_nodes), subpos, list_nodes, node_size=thiscom_sizes, node_color=acc(acc_dict[com]))
        nx.draw_networkx_nodes(G.subgraph(list_nodes), subpos, list_nodes, node_size=thiscom_sizes, node_color=clrs_frc[tt[tt['module']==com].index[0]])
        #nx.draw_networkx_edges(G.subgraph(list_nodes), pos)
        nx.draw_networkx_edges(G.subgraph(list_nodes), subpos, width=[w['weight'] for (u,v,w) in G.subgraph(list_nodes).edges(data=True)])
        nx.draw_networkx_labels(G.subgraph(list_nodes), subpos, dict(ctnames[list_nodes]), font_size=7)
        #nx.draw_networkx_labels(G.subgraph(list_nodes), pos, dict(zip(list_nodes,list_nodes)), font_size=8)
        plt.axis('off')
        plt.savefig('%s.names.%s.%s' % (com, gprog, outname))
        plt.hold(False)

"""def make_plot(graph, tree, outname):
    G = graph
    ebc = nx.edge_betweenness_centrality(G)
    for e in G.edges():
        G.add_edge(e[0], e[1], weight=(ebc[e]*100))
    tree = tree.iloc[G.nodes(),:]
    pos = nx.graphviz_layout(G, prog='sfdp')
    #G.positions = nx.circular_layout(G)
    #GA = nx.to_agraph(G)
    #GA.layout(prog='fdp')
    #GA.draw('tt.png', format='png')
    acc = plt.get_cmap('Set3')
    com_norm = (tree.loc[:,'coms'] - tree.loc[:,'coms'].min()) / (tree.loc[:,'coms'].max() - tree.loc[:,'coms'].min())
    acc_dict = dict(zip(sorted(map(int, set(tree.loc[:,'coms']))), sorted(set(com_norm))))
    nodecolors = [acc_dict[nn] for nn in map(int, tree.loc[:,'coms'])]
    #gr1 = pgv.AGraph(colorscheme='set19')
    #gr1.add_nodes_from(G.nodes())
    #gr1.add_edges_from(G.edges())
    nodesizes = [(v*2000) for v in nx.betweenness_centrality(G).values()]
    #nodesizes = [G.degree(v) for v in G]
    nx.draw_networkx_nodes(G, pos, node_size=nodesizes, node_color = nodecolors)
    nx.draw_networkx_edges(G, pos, width=[w['weight'] for (u,v,w) in G.edges(data=True)])
    plt.axis('off')
    plt.savefig(outname)"""

"""def make_plot(graph, tree, outname):
    G = graph
    tree = tree.iloc[graph.nodes(),:]
    size = float(len(set(tree.loc[:,'coms'])))
    pos = nx.graphviz_layout(G, prog='fdp')
    acc = plt.get_cmap('Set3')
    com_norm = (tree.loc[:,'coms'] - tree.loc[:,'coms'].min()) / (tree.loc[:,'coms'].max() - tree.loc[:,'coms'].min())
    acc_dict = dict(zip(sorted(map(int, set(tree.loc[:,'coms']))), sorted(set(com_norm))))
    for com in set(tree.loc[:,'coms']):
        com = int(com)
        list_nodes = map(int, tree.loc[:,'nodes'][tree.loc[:,'coms']==com])
        nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 24, node_color = acc(acc_dict[com]))
    nx.draw_networkx_edges(G,pos, alpha=0.5)
    plt.axis('off')
    plt.savefig(outname)"""

groups = ['CB', 'SCB', 'LB', 'SLB']

#for i in np.arange(.1,.61,.1):
for i in np.arange(.1,.11,.1):
    df = pd.read_csv('Qscores_all_dens%s.csv' % i)
    ct = pd.read_csv('CTallregionsBOTH.csv')
    ctnames = pd.Series(ct.columns[3:151])
    #for g in groups:
    for g in ['SCB']:
        maxiter = df.loc[:,g].argmax()
        cols = ['nodes', 'coms']
        tree = pd.DataFrame(np.loadtxt('tree_highest/%s_dens%s_tree.iter%s.highesttree' % (g, i, maxiter)), columns=cols)
        graph = nx.read_edgelist('graphs/%s_dens%s.edgelist' % (g, i), nodetype=int)
        outname = '%s_dens%s_graphplot_TESTclrs2.png' % (g, i)
        make_plot(graph, tree, ctnames, outname, g)
#

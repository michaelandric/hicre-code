#!~/anaconda/bin/python

# import pandas as pd
import numpy as np
import networkx as nx
import os
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
    cmdargs = split('/home/michaeljames.andric/Community_latest/community \
                    -l -1 '+edgelist+'.bin')
    call(cmdargs, stdout=f, stderr=m)
    f.close()
    m.close()


def get_rand_graph(graph, outname):
    randn = nx.random_regular_graph(int(np.mean(graph.degree().values())),
                                    148)
    nx.write_edgelist(randn, outname, data=False)


def get_rand_modularity(edgelist, modscorename):
    m = open(modscorename, 'w')
    cmdargs = split('/home/michaeljames.andric/Community_latest/community -l -1 '+edgelist+'.bin')
    call(cmdargs, stdout=open(os.devnull, 'wb'), stderr=m)   # this for the random graphs, not saving trees so took away stdout
    m.close()


def make_networkx_graph(n_nodes, el_name):
    # setting it up for further use
    g = nx.Graph()
    g.add_nodes_from(range(n_nodes))
    ed = nx.read_edgelist(el_name, nodetype=int)
    g.add_edges_from(ed.edges())
    return g


def get_degrees(graph, n_nodes, outname):
    deg = graph.degree()
    f = open(outname, 'w')
    f.write('\n'.join(map(str, deg.values())))
    f.close()


def get_betweenness_centrality(graph, outname):
    bc = nx.betweenness_centrality(graph)
    f = open(outname, 'w')
    f.write('\n'.join(map(str, bc.values())))
    f.close()


def get_edge_betweenness_centrality(graph, outname):
    ebc = nx.edge_betweenness_centrality(graph)
    f = open(outname, 'w')
    f.write('\n'.join(map(str, ebc.values())))
    f.close()


def clustering_coef(graph, outname):
    cc = nx.clustering(graph)
    f = open(outname, 'w')
    f.write('\n'.join(map(str, cc.values())))
    f.close()


"""
NEED TO FIX THIS STILL
def get_shortest_path_length(graph, n_nodes, outname):
    sp = nx.shortest_path_length(graph)
    zd = [i for i in range(0, n_nodes) if i not in sp.keys()]
    ZeroD = dict(zip(zd, np.zeros(len(zd), dtype=np.int8)))
    outD = dict(sp, **ZeroD)
    f = open(outname, 'w')
    f.write('\n'.join(map(str, outD.values())))
    f.close()
"""

if __name__ == "__main__":
    base_dir = '%s/hicre/regular/' % os.environ['t2']
    groups = ['CB', 'SCB']
    nnodes = 148
    for g in groups:
        for i in np.arange(.10, .61, .1):
            el_pref = '%s.dens_%s.edgelist.gz' % (g, i)
            edgelist = os.path.join(base_dir, 'graphs', el_pref)
            graph = make_networkx_graph(nnodes, edgelist)

            bc_dir = os.path.join(base_dir, 'betweenness_centrality')
            if not os.path.exists(bc_dir):
                os.makedirs(bc_dir)
            bc_outname = os.path.join(bc_dir, '%s.dens_%s.btwn_cntr' % (g, i))
            get_edge_betweenness_centrality(graph, bc_outname)

            cc_dir = os.path.join(base_dir, 'clustering_coefficient')
            if not os.path.exists(cc_dir):
                os.makedirs(cc_dir)
            cc_outname = os.path.join(cc_dir, '%s.dens_%s.clust_coef' % (g, i))
            clustering_coef(graph, cc_outname)

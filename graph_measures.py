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


def get_betweenness_centrality(graph, n_nodes, outname):
    bc = nx.betweenness_centrality(graph)
    zd = [i for i in range(0, n_nodes) if i not in bc.keys()]
    ZeroD = dict(zip(zd, np.zeros(len(zd), dtype=np.int8)))
    outD = dict(bc, **ZeroD)
    f = open(outname, 'w')
    f.write('\n'.join(map(str, outD.values())))
    f.close()


def get_edge_betweenness_centrality(graph, n_nodes, outname):
    ebc = nx.edge_betweenness_centrality(graph)
    zd = [i for i in range(0, n_nodes) if i not in ebc.keys()]
    ZeroD = dict(zip(zd, np.zeros(len(zd), dtype=np.int8)))
    outD = dict(ebc, **ZeroD)
    f = open(outname, 'w')
    f.write('\n'.join(map(str, outD.values())))
    f.close()


def get_shortest_path_length(graph, n_nodes, outname):
    sp = nx.shortest_path_length(graph)
    zd = [i for i in range(0, n_nodes) if i not in sp.keys()]
    ZeroD = dict(zip(zd, np.zeros(len(zd), dtype=np.int8)))
    outD = dict(sp, **ZeroD)
    f = open(outname, 'w')
    f.write('\n'.join(map(str, outD.values())))
    f.close()


if __name__ == "__main__":
    base_dir = '%s/hicre/regular/' % os.environ['t2']
    groups = ['CB', 'SCB']
    nnodes = 148
    for g in groups:
        for i in np.arange(.10, .61, .1):
            el_pref = '%s.dens_%s.edgelist.gz' % (g, i)
            edgelist = os.path.join(base_dir, 'graphs', el_pref)
            graph = make_networkx_graph(nnodes, edgelist)

            deg_dir = os.path.join(base_dir, 'degrees')
            if not os.path.exists(deg_dir):
                os.makedirs(deg_dir)
            deg_outname = os.path.join(deg_dir, '%s.dens_%s.degrees' % (g, i))
            get_degrees(graph, nnodes, deg_outname)

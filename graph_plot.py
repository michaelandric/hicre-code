#!~/anaconda/bin/python

import pandas as pd
import numpy as np
import networkx as nx
import random
import os
from community import *
from shlex import split
from subprocess import call
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def make_plot(graph, outname):
    color_dict = {0:'#FFFF00', 1:'#FF0000', 2:'#33CCCC', 3:'#3399FF', 4:'#FF33CC', 5:'#66FF33'}
    G = graph
    partition = best_partition(G)
    size = float(len(set(partition.values())))
    #pos = nx.spring_layout(G)
    pos = nx.graphviz_layout(G, prog='fdp')
    count = 0.
    for com in set(partition.values()):
        count = count + 1.
        list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
        nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 24, node_color = color_dict[com])
    nx.draw_networkx_edges(G,pos, alpha=0.5)
    plt.axis('off')
    plt.savefig(outname)



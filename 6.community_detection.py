#!/usr/bin/env python
"""This is to convert edgelists to binary encoding for louvain community detection.
Then to run community detection."""
__author__ = 'andric'

import sys
import os
import time
import numpy as np
from shlex import split
from subprocess import call, STDOUT, PIPE, Popen

class COMMUN:

    def __init__(self, edgelist):
        """
        Methods for converting text file edgelist to binary format.
        Doing community detection.
        :param edgelist: The graph
        """
        self.graphname = edgelist

    def zipper(self, method):
        """
        Unzip / zip the graph file for use with Louvain tools.
        :param file: This graph to be unzipped/zipped
        :param method: Either "zip" or "unzip"
        :return: Writes to file the binary formatted graph for Louvain community detection
        """
        try:
            if method == 'zip':
                print 'Zipping up %s -- ' % self.graphname+time.ctime()
                cmds = split('gzip %s' % self.graphname)
                call(cmds)
                print 'DONE. '+time.ctime()
            elif method == 'unzip':
                print 'Unzipping  %s -- ' % self.graphname+time.ctime()
                cmds = split('gunzip %s.gz' % self.graphname)
                call(cmds)
                print 'DONE. '+time.ctime()
        except IOError:
            print 'zipper not working. No file? Flaming... '+time.ctime()
            sys.exit()

    def convert_graph(self):
        """
        This is to convert graph for community detection
        :param graph: The graph made in previous function
        :return: Will convert to binary for Louvain algorithm and write to file
        """
        if os.path.exists(self.graphname):
            f = open('stdout_files/stdout_from_convert.txt', 'w')
            print 'Converting edgelist to binary for community detection -- '+time.ctime()
            cmdargs = split('community_convert -i '+self.graphname+'  -o '+self.graphname+'.bin')
            call(cmdargs, stdout=f, stderr=STDOUT)
            f.close()
            print 'Conversion done. -- '+time.ctime()
        elif os.path.exists(self.graphname+'.gz'):
            print 'You need to unzip the graph! '+time.ctime()
        else:
            print 'Cannot find the graph. Check your configuration and inputs. \nFlaming... '+time.ctime()

    def get_modularity(self, tree_out):
        """
        Do community detection with Louvain algorithm.
        :param tree_out:
        :return: Q value, also writes tree to file.
        """
        fh = open(tree_out, 'w')
        cmdargs = split('community -l -1 '+self.graphname+'.bin')
        m = Popen(cmdargs, stdout=fh, stderr=PIPE).communicate()
        fh.close()
        return float(m[1])


if __name__ == '__main__':
    """NO CMD ARGS HERE ----------------------
    if len(sys.argv) < 4:
        sys.stderr.write("You done screwed up! \n"
                         "Usage: %s <SUBJECT ID> <CONDITION ID> <THRESH DENSITY> \n" %
                         (os.path.basename(sys.argv[0]),))"""

    os.chdir(os.environ['t2']+'/hicre/regular')
    print os.getcwd()

    subjid = 'SCB'
    #subjid = 'Null' 
    thresh_density = '0.1' 
    treedir = 'trees'
    #treedir = 'Null_trees'
    mod_dir = 'modularity'
    #mod_dir = 'Null_modularity'
    niter = 100

    """for i in xrange(niter):
        for ll in ['A', 'B']:"""

    graph_dir = 'graphs'
    #graph_dir = 'Null_graphs'
    #graph = '%s/%s.%s_iter%s.dens_%s.edgelist' % (graph_dir, subjid, ll, i, thresh_density)
    graph = '%s/%s.AG.dens_%s.edgelist' % (graph_dir, subjid, thresh_density)
    cm = COMMUN(graph)
    cm.zipper('unzip')
    cm.convert_graph()
    cm.zipper('zip')
    # Below for doing modularity
    Qs = np.array(np.zeros(niter))
    print 'Doing community detection. \nNumber of iterations: %s -- ' % niter+time.ctime()
    if not os.path.exists(treedir):
        os.makedirs(treedir)
    if not os.path.exists(mod_dir):
        os.makedirs(mod_dir)
    for n in xrange(niter):
        #tree_outname = '%s/iter%s_subiter%s.%s.%s.dens_%s.tree' % (treedir, i, n, subjid, ll, thresh_density)
        tree_outname = '%s/iter%s.%s.dens_%s.tree' % (treedir, n, subjid, thresh_density)
        Qs[n] = cm.get_modularity(tree_outname)
    np.savetxt('%s/%s.dens_%s.Qval' % (mod_dir, subjid, thresh_density), Qs, fmt='%.4f')

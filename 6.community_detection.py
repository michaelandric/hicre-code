#!/usr/bin/env python
"""This is to convert edgelists to binary encoding for
louvain community detection.
Then to run community detection.
@author: andric
"""

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
        :return: Writes to file the binary formatted graph
        for Louvain community detection
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
            print 'Converting edgelist to binary for community detection'
            print time.ctime()
            cmdargs = split('community_convert -i '+self.graphname+'  -o '+self.graphname+'.bin')
            call(cmdargs, stdout=f, stderr=STDOUT)
            f.close()
            print 'Conversion done. -- '+time.ctime()
        elif os.path.exists(self.graphname+'.gz'):
            print 'You need to unzip the graph! '+time.ctime()
        else:
            print 'Cannot find the graph.'
            print 'Check your configuration and inputs.'
            print 'Flaming... '+time.ctime()

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

    os.chdir(os.environ['t2']+'/hicre/regular')
    print os.getcwd()

    treedir = 'trees'
    mod_dir = 'modularity'
    niter = 100
    graph_dir = 'graphs'

    for subjid in ['CB', 'SCB']:
        for thresh_density in ['0.2', '0.3', '0.4', '0.5', '0.6']:
            graph_name = '%s.dens_%s.edgelist' % (subjid, thresh_density)
            graph = os.path.join(graph_dir, graph_name)
            cm = COMMUN(graph)
            cm.zipper('unzip')
            cm.convert_graph()
            cm.zipper('zip')
            # Below for doing modularity
            Qs = np.array(np.zeros(niter))
            print 'Doing community detection.'
            print 'Number of iterations: %s -- ' % niter+time.ctime()
            if not os.path.exists(treedir):
                os.makedirs(treedir)
            if not os.path.exists(mod_dir):
                os.makedirs(mod_dir)
            for n in xrange(niter):
                tree_outname = 'iter%s.%s.dens_%s.tree' % \
                                (n, subjid, thresh_density)
                Qs[n] = cm.get_modularity(os.path.join(treedir, tree_outname))
            Qs_outname = '%s.dens_%s.Qval' % (subjid, thresh_density)
            np.savetxt(os.path.join(mod_dir, Qs_outname), Qs, fmt='%.4f')

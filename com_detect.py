# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 16:20:17 2015

This is to do resampled (9 + 9 from each group CB and SCB)
Originally did this just for the 0.1 density. Need to do at other densities.

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

    os.chdir(os.environ['t2']+'/hicre/')
    print os.getcwd()

    subjid = 'SCB'
    # subjid = 'Null'
    thresh_density = '0.1'
    treedir = 'trees_dens%s' % thresh_density
    mod_dir = 'modularity_dens%s' % thresh_density
    if not os.path.exists(treedir):
        os.makedirs(treedir)
    if not os.path.exists(mod_dir):
        os.makedirs(mod_dir)
    niter = 100
    graph_dir = 'graphs'

    for i in xrange(niter):
        for ll in ['A', 'B']:
            graph = '%s/%s.%s_iter%s.dens_%s.edgelist' % (graph_dir, subjid, ll, i, thresh_density)
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
                tree_outname = '%s/iter%s_subiter%s.%s.%s.dens_%s.tree' % (treedir, i, n, subjid, ll, thresh_density)
                # tree_outname = '%s/iter%s.%s.dens_%s.tree' % (treedir, n, subjid, thresh_density)
                Qs[n] = cm.get_modularity(tree_outname)
                np.savetxt('%s/%s_iter%s.%s.dens_%s.Qval' % (mod_dir, subjid, i, ll, thresh_density), Qs, fmt='%.4f')

#!/usr/bin/env python
"""This parases the tree at the highest hierarchical level"""
__author__ = 'andric'

import sys
import os
from subprocess import Popen, PIPE
from shlex import split
from time import ctime
from collections import Counter
import numpy as np

class TreeParser(object):

    tree_all_levels = None

    def get_hierarchical(self, tree_all_levels, tr_outname):
        """
        Get the hierarchy for the modularity solution.
        Find the highest level. Get the tree at that level. Write tree to file.
        Find the number of modules at that level.
        :param tree_all_levels: the entire tree comprising every level (from community detection)
        :param tr_outname: the output name for the tree at highest hierarchical level
        :return: number of modules at highest hierarchical level
        """
        cmdargs = split('hierarchy -n %s' % tree_all_levels)
        #print 'Parsing trees to find highest hierarchical level -- '+ctime()
        #print cmdargs
        p = Popen(cmdargs, stdout=PIPE).communicate()
        h = int(p[0].split()[3]) - 1
        #print 'Done parsing trees -- '+ctime()
        #print 'Highest level: %s ' % h
        #print 'Getting hierarchy -- '+ctime()
        cmdargs = split('hierarchy -l %d %s' % (h, tree_all_levels))
        tree = Popen(cmdargs, stdout=PIPE).communicate()
        f = open(tr_outname, 'w')
        f.write(tree[0])
        f.close()
        #print ctime()+' :::\n'
        #print 'Done writing the tree. \nNow getting number of modules... '+ctime()

        stree = [tt for tt in tree[0].split('\n')]
        mods = np.array(np.zeros(len(stree)-1), dtype=np.int16)
        for i in xrange(len(mods)):
            mods[i] = stree[i].split()[1]
        cnts = np.array(Counter(mods).values())
        n_mods = len(cnts[np.where(cnts > 1)])
        #print `n_mods`+' is the number of modules (> 1 voxel) '+ctime()
        return n_mods


if __name__ == '__main__':
    """ NOT DOING COMMAND LINE ARGS 
    if len(sys.argv) < 4:
        sys.stderr.write("You done screwed up! \n"
                         "Usage: %s <SUBJECT ID> <CONDITION ID> <THRESH DENSITY> \n" %
                         (os.path.basename(sys.argv[0]),))"""

    os.chdir(os.environ['t2']+'/hicre/noage_gend')
    print os.getcwd()
    subjid = 'SCB'
    # subjid = 'Null'
    thresh_density = '0.1'
    niter = 100   # because I have 100 iterations of the modularity solution, one tree for each

    tp = TreeParser()

    treedir = 'AB_trees'
    # treedir = 'Null_trees'
    tree_hier_dir = 'AB_tree_highest'
    # tree_hier_dir = 'Null_tree_highest'
    n_mods_dir = 'AB_N_mods_nonSingle'
    # n_mods_dir = 'Null_N_mods_nonSingle'
    if not os.path.exists(tree_hier_dir):
        os.makedirs(tree_hier_dir)
    if not os.path.exists(n_mods_dir):
        os.makedirs(n_mods_dir)

    for ll in ['A', 'B']:
        for gr in xrange(100):
            module_count = np.array(np.zeros(niter))
            for n in xrange(niter):
                print 'ITERATION# %s  --  GRAPH %s ' % (n, gr)+ctime()
                # print 'ITERATION# %s  ' % n+ctime()
                main_tree = '%s/iter%s_subiter%s.%s.%s.dens_%s.tree' % (treedir, gr, n, subjid, ll, thresh_density)
                # main_tree = '%s/iter%s.%s.dens_%s.tree' % (treedir, n, subjid, thresh_density)
                tree_out = '%s/iter%s_subiter%s.%s.AG.%s.dens_%s.tree_highest' % (tree_hier_dir, gr, n, subjid, ll, thresh_density)
                # tree_out = '%s/iter%s.%s.dens_%s.tree_highest' % (tree_hier_dir, n, subjid, thresh_density)
                module_count[n] = tp.get_hierarchical(main_tree, tree_out)
            np.savetxt('%s/%s.AG_iter%s.%s.dens_%s.n_mods' % (n_mods_dir, subjid, gr, ll, thresh_density), module_count, fmt='%i')

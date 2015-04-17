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
        :param tree_all_levels: the entire tree comprising
        every level (from community detection)
        :param tr_outname: the output name for the tree at
        highest hierarchical level
        :return: number of modules at highest hierarchical level
        """
        cmdargs = split('hierarchy -n %s' % tree_all_levels)
        p = Popen(cmdargs, stdout=PIPE).communicate()
        h = int(p[0].split()[3]) - 1
        cmdargs = split('hierarchy -l %d %s' % (h, tree_all_levels))
        tree = Popen(cmdargs, stdout=PIPE).communicate()
        f = open(tr_outname, 'w')
        f.write(tree[0])
        f.close()

        stree = [tt for tt in tree[0].split('\n')]
        mods = np.array(np.zeros(len(stree)-1), dtype=np.int16)
        for i in xrange(len(mods)):
            mods[i] = stree[i].split()[1]
        cnts = np.array(Counter(mods).values())
        n_mods = len(cnts[np.where(cnts > 1)])
        return n_mods


if __name__ == '__main__':

    os.chdir(os.environ['t2']+'/hicre/regular')
    print os.getcwd()
    niter = 100

    tp = TreeParser()

    treedir = 'trees'
    tree_hier_dir = 'tree_highest'
    n_mods_dir = 'N_mods_nonSingle'
    if not os.path.exists(tree_hier_dir):
        os.makedirs(tree_hier_dir)
    if not os.path.exists(n_mods_dir):
        os.makedirs(n_mods_dir)

    # go through subjid and densities
    for subjid in ['CB', 'SCB']:
        for thresh_density in ['0.2', '0.3', '0.4', '0.5', '0.6']:
            module_count = np.array(np.zeros(niter))
            for n in xrange(niter):
                print 'ITERATION# %s ' % n+ctime()
                main_tree_name = 'iter%s.%s.dens_%s.tree' % \
                    (n, subjid, thresh_density)
                main_tree = os.path.join(treedir, main_tree_name)
                tree_out_name = 'iter%s.%s.dens_%s.tree_highest' % \
                    (n, subjid, thresh_density)
                tree_out = os.path.join(tree_hier_dir, tree_out_name)
                module_count[n] = tp.get_hierarchical(main_tree, tree_out)
            n_mods_outname = '%s.dens_%s.n_mods' % (subjid, thresh_density)
            np.savetxt(os.path.join(n_mods_dir, n_mods_outname),
                       module_count, fmt='%i')

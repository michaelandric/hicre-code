# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 16:50:05 2015

This is to do resampled (9 + 9 from each group CB and SCB)
Originally did this just for the 0.1 density. Need to do at other densities.

Run this after "com_detect.py" (which, itself, goes after "corr_mats.py")

@author: andric
"""


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
        :param tr_outname: the output name for the tree at \
        highest hierarchical level
        :return: number of modules at highest hierarchical level
        """
        cmdargs = split('hierarchy -n %s' % tree_all_levels)
        p = Popen(cmdargs, stdout=PIPE).communicate()
        h = int(p[0].split()[3]) - 1
        print 'Getting hierarchy -- '+ctime()
        cmdargs = split('hierarchy -l %d %s' % (h, tree_all_levels))
        tree = Popen(cmdargs, stdout=PIPE).communicate()
        f = open(tr_outname, 'w')
        f.write(tree[0])
        f.close()
        print 'Done writing the tree. \n'
        print 'Now getting number of modules... '+ctime()

        stree = [tt for tt in tree[0].split('\n')]
        mods = np.array(np.zeros(len(stree)-1), dtype=np.int16)
        for i in xrange(len(mods)):
            mods[i] = stree[i].split()[1]
        cnts = np.array(Counter(mods).values())
        n_mods = len(cnts[np.where(cnts > 1)])
        print str(n_mods)+' is the number of modules (> 1 voxel) '+ctime()
        return n_mods


if __name__ == '__main__':

    os.chdir(os.environ['t2']+'/hicre/')
    print os.getcwd()

    for subjid in ['CB', 'SCB']:

        for thresh_density in ['0.3', '0.4', '0.5', '0.6']:
            # thresh_density = '0.2'
            niter = 100

            tp = TreeParser()

            treedir = 'trees_dens%s' % thresh_density
            tree_hier_dir = 'AB_tree_highest_dens%s' % thresh_density
            # tree_hier_dir = 'Null_tree_highest'
            n_mods_dir = 'AB_N_mods_nonSingle_dens%s' % thresh_density
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
                        main_tree_name = 'iter%s_subiter%s.%s.%s.dens_%s.tree' % \
                            (gr, n, subjid, ll, thresh_density)
                        main_tree = os.path.join(treedir, main_tree_name)
                        tree_out_name = 'iter%s_subiter%s.%s.%s.dens_%s.tree_highest' % \
                            (gr, n, subjid, ll, thresh_density)
                        tree_out = os.path.join(tree_hier_dir, tree_out_name)
                        module_count[n] = tp.get_hierarchical(main_tree, tree_out)
                    outname = '%s_iter%s.%s.dens_%s.n_mods' % \
                        (n_mods_dir, subjid, gr, ll, thresh_density)
                    np.savetxt(os.path.join(n_mods_dir, outname), module_count, fmt='%i')

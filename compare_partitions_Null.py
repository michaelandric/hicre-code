#!/usr/bin/env python
"""Compare partitions"""
__author__ = 'andric'

import sys
import os
import time
import numpy as np
from itertools import combinations


class COMPARE:
    """
    Methods for comparing partition similarity
    """

    def adjRand(self, p1, p2):
        """
        Get the Adjusted Rand Score, adjusted as
        ARI = (RI - Expected_RI) / (max(RI) - Expected_RI)
        :param p1: Partition 1
        :param p2: Partition 2
        :return: Adjusted Rand score
        """
        ars = adjusted_rand_score(p1, p2)
        return ars

    def normalized_MI(self, p1, p2):
        """
        Get the Normalized Mutual Information
        :param p1: Partition 1
        :param p2: Partition 2
        :return: Normalized Mutual Information measure
        """
        nmi = normalized_mutual_info_score(p1, p2)
        return nmi



if __name__ == '__main__':

    if len(sys.argv) < 3:
        sys.stderr.write("You done screwed up! \n"
                         "Usage: %s <SUBJECT ID> <COMPARE METHOD> \n" %
                         (os.path.basename(sys.argv[0]),))

    subjid = sys.argv[1]
    compare_method = sys.argv[2]
    niter = 100   # because I have 100 iterations of the modularity solution, one tree for each
    n_combinations = ((niter**2)-niter)/2
    compare_out = np.array(np.zeros(n_combinations))   # prep output array
    output_pref = '%s_%s.txt' % (subjid, compare_method)   # output naming prefix

    n_regions = 148
    # Building array of inputs. These are the trees of highest modularity
    tree_mat1 = np.array(np.zeros(niter*n_regions)).reshape(n_regions, niter)
    tree_mat2 = np.array(np.zeros(niter*n_regions)).reshape(n_regions, niter)
    for n in xrange(niter):
        print n
        infile1 = 'null_tree_highest/%s_dens0.1_tree.graph%s.iter0.tree_highest' % ('Null_CB', n)
        in_com = np.loadtxt(infile1)[:,1]
        if len(in_com) == 147:
            in_com = np.append(in_com, in_com[len(in_com)-1])
        tree_mat1[:,n] = in_com   # because these infile actually has one col for indices
        #infile2 = 'null_tree_highest/%s_dens0.1_tree.graph%s.iter0.tree_highest' % ('Null_CB', n)
        #tree_mat2[:,n] = np.loadtxt(infile2)[:,1]   # because these infile actually has one col for indices

    tree_mat2 = tree_mat1   # If comparing for same subject over iterations


    # Main section to run
    cmp = COMPARE()

    if compare_method == 'ARI':
        from sklearn.metrics import adjusted_rand_score
        i = 0
        for combo in combinations(np.arange(100), 2):
            compare_out[i] = cmp.adjRand(tree_mat1[:,combo[0]], tree_mat2[:,combo[1]])
            i = i+1
        np.savetxt(output_pref, compare_out, fmt='%.4f')
    elif compare_method == 'NMI':
        from sklearn.metrics import normalized_mutual_info_score
        i = 0
        for combo in combinations(np.arange(100), 2):
            compare_out[i] = cmp.normalized_MI(tree_mat1[:,combo[0]], tree_mat2[:,combo[1]])
            i = i+1
        np.savetxt(output_pref, compare_out, fmt='%.4f')
    else:
        print 'Where is your method?? \nFlaming... '+time.ctime()
        sys.exit(1)

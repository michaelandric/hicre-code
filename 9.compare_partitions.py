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

    """ NO CMD ARGS ------
    if len(sys.argv) < 3:
        sys.stderr.write("You done screwed up! \n"
                         "Usage: %s <SUBJECT ID> <COMPARE METHOD> \n" %
                         (os.path.basename(sys.argv[0]),))"""

    os.chdir(os.environ['t2']+'/hicre/noage_gend')
    print os.getcwd()

    subjid = 'SCB'
    # subjid1 = 'CB'
    # subjid2 = 'SCB'
    # subjid = 'Null'
    compare_method = 'ARI'
    niter = 100   # because I have 100 iterations of the modularity solution, one tree for each
    n_combinations = ((niter**2)-niter)/2
    compare_out = np.array(np.zeros(n_combinations))   # prep output array
    # output_pref = 'within%s_%s.txt' % (subjid, compare_method)   # output naming prefix
    # output_pref = 'between%s_%s.txt' % ('CB_SCB', compare_method)   # output naming prefix
    # output_pref = '%s_%s.txt' % (subjid, compare_method)   # output naming prefix
    output_pref = 'AGtoReal_%s_%s.txt' % (subjid, compare_method)   # output naming prefix

    # tree_dir = 'tree_highest'
    # tree_dir = 'Null_tree_highest'
    tree_dir = 'tree_highest'
    n_regions = 148
    # Building array of inputs. These are the trees of highest modularity
    tree_mat1 = np.array(np.zeros(niter*n_regions)).reshape(n_regions, niter)
    tree_mat2 = np.array(np.zeros(niter*n_regions)).reshape(n_regions, niter)
    for n in xrange(niter):
        print n
        # a_Qs = np.loadtxt('modularity/%s_iter%d.A.dens_0.1.Qval' % (subjid, n))
        # a_Qs = np.loadtxt('modularity/%s_iter%d.A.dens_0.1.Qval' % (subjid1, n))
        # a_Qs = np.loadtxt('Null_modularity/%s_iter%d.A.dens_0.1.Qval' % (subjid, n))
        # a_max = a_Qs.argmax()
        # b_Qs = np.loadtxt('modularity/%s_iter%d.B.dens_0.1.Qval' % (subjid, n))
        # b_Qs = np.loadtxt('modularity/%s_iter%d.B.dens_0.1.Qval' % (subjid2, n))
        # b_Qs = np.loadtxt('Null_modularity/%s_iter%d.B.dens_0.1.Qval' % (subjid, n))
        # b_max = b_Qs.argmax() 
        # infile1 = '%s/iter%d_subiter%d.%s.A.dens_0.1.tree_highest' % (tree_dir, n, a_max, subjid)
        # infile1 = '%s/iter%d_subiter%d.%s.A.dens_0.1.tree_highest' % (tree_dir, n, a_max, subjid1)
        # infile1 = '%s/iter%d_subiter%d.%s.A.dens_0.1.tree_highest' % (tree_dir, n, a_max, subjid)
        infile1 = '/home/michaeljames.andric/hicre/%s/%s_dens0.1_tree.iter%d.highesttree' % (tree_dir, subjid, n)
        in_com_a = np.loadtxt(infile1)[:, 1]   # because these infile actually has one col for indices
        if len(in_com_a) == 147:
            in_com_a = np.append(in_com_a, in_com_a[len(in_com_a)-1])
        tree_mat1[:, n] = in_com_a
        # infile2 = '%s/iter%d_subiter%d.%s.B.dens_0.1.tree_highest' % (tree_dir, n, b_max, subjid)
        # infile2 = '%s/iter%d_subiter%d.%s.B.dens_0.1.tree_highest' % (tree_dir, n, b_max, subjid2)
        infile2 = '%s/iter%d.%s.dens_0.1.tree_highest' % (tree_dir, n, subjid)
        in_com_b = np.loadtxt(infile2)[:, 1]   # because these infile actually has one col for indices
        if len(in_com_b) == 147:
            in_com_b = np.append(in_com_b, in_com_b[len(in_com_b)-1])
        tree_mat2[:, n] = in_com_b
    # tree_mat2 = tree_mat1   # If comparing for same subject over iterations

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

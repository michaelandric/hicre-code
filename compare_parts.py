# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 17:23:06 2015

This is to do resampled (9 + 9 from each group CB and SCB)
Originally did this just for the 0.1 density. Need to do at other densities.

Run this after "tree_hier.py"

@author: andric
"""


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

    os.chdir(os.environ['t2']+'/hicre/')
    print os.getcwd()

    thresh_density = '0.2'
    # subjid = 'SCB'
    subjid1 = 'CB'
    subjid2 = 'SCB'
    # subjid = 'Null'
    compare_method = 'ARI'
    niter = 100   # because I have 100 iterations of the modularity solution
    n_combinations = ((niter**2)-niter)/2
    compare_out = np.array(np.zeros(n_combinations))   # prep output array
    # output_pref = 'within%s_%s.txt' % (subjid, compare_method)   # output naming prefix
    output_pref = 'between%s_dens%s_%s.txt' % ('CB_SCB', thresh_density, compare_method)   # output naming prefix

    # tree_dir = 'tree_highest'
    # tree_dir = 'Null_tree_highest'
    tree_dir = 'AB_tree_highest_dens%s' % thresh_density
    n_regions = 148
    # Building array of inputs. These are the trees of highest modularity
    tree_mat1 = np.array(np.zeros(niter*n_regions)).reshape(n_regions, niter)
    tree_mat2 = np.array(np.zeros(niter*n_regions)).reshape(n_regions, niter)
    for n in xrange(niter):
        print n
        a_Qs = np.loadtxt('modularity_dens%s/%s_iter%d.A.dens_0.1.Qval' % (thresh_density, subjid1, n))
        a_max = a_Qs.argmax()
        b_Qs = np.loadtxt('modularity_dens%s/%s_iter%d.B.dens_0.1.Qval' % (thresh_density, subjid2, n))
        b_max = b_Qs.argmax() 
        infile1 = '%s/iter%d_subiter%d.%s.A.dens_0.1.tree_highest' % (tree_dir, n, a_max, subjid1)
        in_com_a = np.loadtxt(infile1)[:, 1]   # because these infile actually has one col for indices
        if len(in_com_a) == 147:
            in_com_a = np.append(in_com_a, in_com_a[len(in_com_a)-1])
        tree_mat1[:, n] = in_com_a
        infile2 = '%s/iter%d_subiter%d.%s.B.dens_0.1.tree_highest' % (tree_dir, n, b_max, subjid2)
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
            compare_out[i] = cmp.adjRand(tree_mat1[:, combo[0]], tree_mat2[:, combo[1]])
            i = i+1
        np.savetxt(output_pref, compare_out, fmt='%.4f')
    elif compare_method == 'NMI':
        from sklearn.metrics import normalized_mutual_info_score
        i = 0
        for combo in combinations(np.arange(100), 2):
            compare_out[i] = cmp.normalized_MI(tree_mat1[:, combo[0]], tree_mat2[:, combo[1]])
            i = i+1
        np.savetxt(output_pref, compare_out, fmt='%.4f')
    else:
        print 'Where is your method?? \nFlaming... '+time.ctime()
        sys.exit(1)

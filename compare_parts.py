# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 17:23:06 2015

This is to do resampled (9 + 9 from each group CB and SCB)
Originally did this just for the 0.1 density. Need to do at other densities.

Run this after "tree_hier.py"

@author: andric
"""


import os
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

    for thresh_density in ['0.2', '0.3', '0.4', '0.5', '0.6']:
        # thresh_density = '0.2'
        # subjid1 = 'CB'
        # subjid2 = subjid1
        subjid2 = 'SCB'
        subjid1 = subjid2
        niter = 100
        n_combinations = ((niter**2)-niter)/2
        compare_out = np.array(np.zeros(n_combinations))   # prep output array

        tree_dir = 'AB_tree_highest_dens%s' % thresh_density
        n_regions = 148
        # Building array of inputs. These are the trees of highest modularity
        tree_mat1 = np.array(np.zeros(niter*n_regions))
        tree_mat1 = tree_mat1.reshape(n_regions, niter)
        tree_mat2 = np.array(np.zeros(niter*n_regions))
        tree_mat2 = tree_mat2.reshape(n_regions, niter)

        modularity_dir = 'modularity_dens%s' % thresh_density
        for n in xrange(niter):
            print n

            a_Q_pref = '%s_iter%d.A.dens_%s.Qval' % \
                (subjid1, n, thresh_density)
            a_Qs = np.loadtxt(os.path.join(modularity_dir, a_Q_pref))
            a_max = a_Qs.argmax()
            b_Q_pref = '%s_iter%d.B.dens_%s.Qval' % \
                (subjid2, n, thresh_density)
            b_Qs = np.loadtxt(os.path.join(modularity_dir, b_Q_pref))
            b_max = b_Qs.argmax()

            infile1_name = 'iter%d_subiter%d.%s.A.dens_%s.tree_highest' % \
                (n, a_max, subjid1, thresh_density)
            # because these infile actually has one col for indices:
            in_com_a = np.loadtxt(os.path.join(tree_dir, infile1_name))[:, 1]
            if len(in_com_a) == 147:
                in_com_a = np.append(in_com_a, in_com_a[len(in_com_a)-1])
            tree_mat1[:, n] = in_com_a

            infile2_name = 'iter%d_subiter%d.%s.B.dens_%s.tree_highest' % \
                (n, b_max, subjid2, thresh_density)
            # because these infile actually has one col for indices:
            in_com_b = np.loadtxt(os.path.join(tree_dir, infile2_name))[:, 1]
            if len(in_com_b) == 147:
                in_com_b = np.append(in_com_b, in_com_b[len(in_com_b)-1])
            tree_mat2[:, n] = in_com_b

        # Main section to run. DOING BOTH ARI AND NMI
        cmp = COMPARE()
        from sklearn.metrics import adjusted_rand_score
        # output_pref = 'between%s_dens%s_ARI.txt' % ('CB_SCB', thresh_density)
        # output_pref = 'within%s_dens%s_ARI.txt' % (subjid1, thresh_density)
        output_pref = 'within%s_dens%s_ARI.txt' % (subjid2, thresh_density)
        for i, combo in enumerate(combinations(np.arange(100), 2)):
            tree_a = tree_mat1[:, combo[0]]
            tree_b = tree_mat2[:, combo[1]]
            compare_out[i] = cmp.adjRand(tree_a, tree_b)
        np.savetxt(output_pref, compare_out, fmt='%.4f')

        from sklearn.metrics import normalized_mutual_info_score
        # output_pref = 'between%s_dens%s_NMI.txt' % ('CB_SCB', thresh_density)
        # output_pref = 'within%s_dens%s_NMI.txt' % (subjid1, thresh_density)
        output_pref = 'within%s_dens%s_NMI.txt' % (subjid2, thresh_density)
        for i, combo in enumerate(combinations(np.arange(100), 2)):
            tree_a = tree_mat1[:, combo[0]]
            tree_b = tree_mat2[:, combo[1]]
            compare_out[i] = cmp.normalized_MI(tree_a, tree_b)
        np.savetxt(output_pref, compare_out, fmt='%.4f')

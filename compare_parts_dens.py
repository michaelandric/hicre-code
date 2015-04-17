# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 17:48:15 2015

This determins similarity (Normalized Mutual Info)
between partitions corresponding to max modularity

@author: andric
"""

import os
import numpy as np
from itertools import combinations
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics import normalized_mutual_info_score


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

    os.chdir(os.environ['t2']+'/hicre/regular')
    print os.getcwd()

    tree_dir = 'tree_highest'
    modularity_dir = 'modularity'
    thresh_densities = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6']
    n_combinations = ((len(thresh_densities)**2)-len(thresh_densities))/2
    for subjid in ['CB', 'SCB']:
        compare_out_nmi = np.array(np.zeros(n_combinations))
        compare_out_ari = np.array(np.zeros(n_combinations))

        dens_combo_list = []
        for i, td in enumerate(combinations(thresh_densities, 2)):
            a_Q_pref = '%s.dens_%s.Qval' % (subjid, td[0])
            a_Qs = np.loadtxt(os.path.join(modularity_dir, a_Q_pref))
            a_max = a_Qs.argmax()
            infile1_name = 'iter%d.%s.dens_%s.tree_highest' % \
                (a_max, subjid, td[0])
            in_com_a = np.loadtxt(os.path.join(tree_dir, infile1_name))[:, 1]
            if len(in_com_a) == 147:
                in_com_a = np.append(in_com_a, in_com_a[len(in_com_a)-1])
            tree_a = in_com_a

            b_Q_pref = '%s.dens_%s.Qval' % (subjid, td[1])
            b_Qs = np.loadtxt(os.path.join(modularity_dir, b_Q_pref))
            b_max = b_Qs.argmax()
            infile2_name = 'iter%d.%s.dens_%s.tree_highest' % \
                (b_max, subjid, td[1])
            in_com_b = np.loadtxt(os.path.join(tree_dir, infile2_name))[:, 1]
            if len(in_com_b) == 147:
                in_com_b = np.append(in_com_b, in_com_b[len(in_com_b)-1])
            tree_b = in_com_b

            # DOING BOTH ARI AND NMI
            cmp = COMPARE()
            compare_out_ari[i] = cmp.adjRand(tree_a, tree_b)
            compare_out_nmi[i] = cmp.normalized_MI(tree_a, tree_b)
            dens_combo_list.append(td)
        output_pref_ari = '%s_ARI_density_comparisons.txt' % subjid
        np.savetxt(output_pref_ari,
                   zip(compare_out_ari, dens_combo_list), fmt='%.4f')
        output_pref_nmi = '%s_NMI_density_comparisons.txt' % subjid
        np.savetxt(output_pref_nmi,
                   zip(compare_out_nmi, dens_combo_list), fmt='%.4f')

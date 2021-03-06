# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 14:56:17 2015

This is to do resampled (9 + 9 from each group CB and SCB)
Originally did this just for the 0.1 density. Need to do at other densities.
This is functionally same as and based on 'corrmats.py' but cleaner code.

@author: andric
"""

import sys
import os
import time
import pandas as pd
import numpy as np
import random


class GRAPHS:

    def __init__(self, subjid, inputTS, thresh_density):
        """
        Initialize for hel
        :param subjid: subject identifier
        :param inputTS: the time series for input
        :param thresh_density: This is the threshold
        :return:
        """
        self.ss = subjid
        self.dens = float(thresh_density)
        self.input = inputTS
        print 'Initializing. -- '+time.ctime()

    def make_graph(self, outname):
        """
        Getting the graph by reading the time series input.
        Doing Pearson's correlation. Sort values then threshold by density.
        Find the indices for thresholded values.
        Make binary graph with those as edges.
        Write the list of edges to file.
        :param outname: Outname for the graph
        :return: Writes to text file the outname
        """
        print 'Now making graph -- '+time.ctime()
        ts = self.input.T   # this need to transpose
        n_vox = ts.shape[0]
        compl_graph = int((n_vox*(n_vox-1))/2)
        n_edges = int(compl_graph*self.dens)
        print 'Input is read. \n'
        print 'Now getting the correlation matrix. '+time.ctime()
        corrmat = np.corrcoef(ts)
        corrmat_ut = np.nan_to_num(np.triu(corrmat, k=1))
        print 'Starting sort. -- '+time.ctime()
        corrsrtd = np.sort(corrmat_ut[corrmat_ut > 0], kind='mergesort')
        print 'Sort done. \nThresholding... -- '+time.ctime()
        threshd = corrsrtd[-n_edges:]
        print 'Thresholding done. \nNow getting edge indices -- '+time.ctime()
        ix = np.searchsorted(threshd, corrmat_ut, 'right')
        print 'Found in 1d '+time.ctime()
        n, v = np.where(ix)
        print 'Done getting where coords... '+time.ctime()
        inds = np.array(zip(n, v), dtype=np.int32)
        print 'Got graph edges. \nWriting it to file -- '+time.ctime()
        np.savetxt(outname, inds, fmt='%d')
        print 'Graph edgelist written out. \nDONE. -- '+time.ctime()
        return np.mean(threshd)


if __name__ == "__main__":

    os.chdir(os.environ['t2']+'/hicre/')
    print os.getcwd()
    df = pd.read_csv('CTallregionsBOTH.csv')

    for subjid in ['CB', 'SCB']:

        input_dat = df[df.loc[:, 'Group'] == subjid].iloc[:, 3:]

        for thresh_density in ['0.3', '0.4', '0.5', '0.6']:
            # thresh_density = '0.2'
            n_iter = 100
            a_avg_r = np.zeros(n_iter)
            b_avg_r = np.zeros(n_iter)

            outdir = 'graphs'
            if not os.path.exists(outdir):
                os.makedirs(outdir)

            for i in xrange(n_iter):
                print 'Iteration# %s' % i+' ----- '+time.ctime()
                """# This is for sample between groups
                ind_list_scb = df[df.loc[:, 'Group'] == 'SCB'].index.tolist()
                ind_list_cb = df[df.loc[:, 'Group'] == 'CB'].index.tolist()
                a_scb = random.sample(ind_list_scb, 9)
                b_scb = list(set(ind_list_scb) - set(a_scb))
                a_cb = random.sample(ind_list_cb, 9)
                b_cb = list(set(ind_list_cb) - set(a_cb))
                input_dat_a = df.iloc[random.sample(a_scb+a_cb,
                                                    len(a_scb+a_scb)), 3:]
                input_dat_b = df.iloc[random.sample(b_scb+b_cb,
                                                    len(b_scb+b_scb)), 3:]"""

                # This is for sample within groups
                ind_list = df[df.loc[:, 'Group'] == subjid].index.tolist()
                a = random.sample(ind_list, 9)
                b = list(set(ind_list) - set(a))
                input_dat_a = df.iloc[random.sample(a, len(a)), 3:]
                input_dat_b = df.iloc[random.sample(b, len(b)), 3:]

                graph_outname = '%s/%s.%s_iter%s.dens_%s.edgelist.gz' % (outdir, subjid, 'A', i, thresh_density)
                GR = GRAPHS(subjid, input_dat_a, thresh_density)
                a_avg_r[i] = GR.make_graph(graph_outname)
                graph_outname = '%s/%s.%s_iter%s.dens_%s.edgelist.gz' % (outdir, subjid, 'B', i, thresh_density)
                GR = GRAPHS(subjid, input_dat_b, thresh_density)
                b_avg_r[i] = GR.make_graph(graph_outname)

            np.savetxt('Avg_r_val_%s.A.dens_%s.txt' % (subjid, thresh_density), a_avg_r, fmt='%.4f')
            np.savetxt('Avg_r_val_%s.B.dens_%s.txt' % (subjid, thresh_density), b_avg_r, fmt='%.4f')

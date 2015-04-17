#!/usr/bin/env python
"""
This is to determine the graphs.
Principal method is using Pearson correlation
and binary matrices
@author: andric
"""

import os
import time
import pandas as pd
import numpy as np
# import random


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
        print 'Input is read. '
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

    os.chdir(os.environ['t2']+'/hicre/regular')
    print os.getcwd()
    df = pd.read_csv('CTallregionsBOTH.csv')

    for subjid in ['CB', 'SCB']:
        input_dat = df[df.loc[:, 'Group'] == subjid].iloc[:, 3:]
        for thresh_density in ['0.2', '0.3', '0.4', '0.5', '0.6']:
            avg_r = np.zeros(1)
            outdir = 'graphs'
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            graph_outname = '%s.dens_%s.edgelist.gz' % (subjid, thresh_density)
            GR = GRAPHS(subjid, input_dat, thresh_density)
            avg_r[0] = GR.make_graph(os.path.join(outdir, graph_outname))

            np.savetxt('Avg_r_val_%s_dens%s.txt' %
                       (subjid, thresh_density), avg_r, fmt='%.4f')

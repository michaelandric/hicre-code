#!/usr/bin/env python

import os
import time
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.backends.backend_pdf import PdfPages
from itertools import *

df = pd.read_csv('CTallregionsBOTH.csv')
subjid = 'CB'
rnl = pd.read_csv('region_names_labels.csv')
rnl2_ind = []
for i in xrange(74):
    rnl2_ind.append(i)
    rnl2_ind.append(i+74)

rnl2 = rnl.iloc[tuple(rnl2_ind), ]


for subjid in ['CB', 'SCB']:
    for dens in np.arange(0.1, 0.61, 0.1):
        dens = float(dens)
        input_dat = df[df.loc[:, 'Group'] == subjid].iloc[:, 3:]

        srtd_input_dat = input_dat.reindex_axis(rnl2.sort(['lobe', 'label'], ascending=False).region, axis=1)
        ts = srtd_input_dat.T
        n_vox = ts.shape[0]
        compl_graph = int((n_vox*(n_vox-1))/2)
        n_edges = int(compl_graph*dens)
        corrmat = np.corrcoef(ts)
        corrmat_ut = np.nan_to_num(np.triu(corrmat, k=1))
        corrsrtd = np.sort(corrmat_ut[corrmat_ut > 0], kind='mergesort')
        threshd = corrsrtd[-n_edges:]
        gg = np.searchsorted(threshd, corrmat)

        # full correlation matrix plot
        np.fill_diagonal(corrmat, 0)
        msk_corrmat = np.ma.masked_where(corrmat == 0, corrmat)
        plt.xlim(0, 148)
        plt.ylim(0, 148)
        plt.pcolormesh(np.swapaxes(msk_corrmat, 1, 0), cmap=cm.spectral, vmin=-1, vmax=1)
        plt.colorbar()
        outname = '%s_%s_corrmat.pdf' % (subjid, dens)
        plt.savefig(outname, dpi=300, transparent=True)
        plt.close()

        thr_corrmat = corrmat
        thr_corrmat[np.where(gg == 0)] = 0
        msk_thr_corrmat = np.ma.masked_where(thr_corrmat == 0, thr_corrmat)
        plt.xlim(0, 148)
        plt.ylim(0, 148)
        plt.pcolormesh(np.swapaxes(msk_thr_corrmat, 1, 0), cmap=cm.spectral, vmin=-1, vmax=1)
        plt.colorbar()
        outname_thr = '%s_%s_corrmat_thr.pdf' % (subjid, dens)
        plt.savefig(outname_thr, dpi=300, transparent=True)
        plt.close()

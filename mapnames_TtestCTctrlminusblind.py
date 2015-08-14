# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 15:58:55 2015

@author: andric


How I got the surface node labels from the anot file:

ConvertDset -i lh.aparc.a2009s.annot.niml.dset -o_1Dp \
-prepend_node_index_1D -prefix lh_node_labels
ConvertDset -i rh.aparc.a2009s.annot.niml.dset -o_1Dp \
-prepend_node_index_1D -prefix rh_node_labels
"""

import time
import os
import pandas as pd
import numpy as np

suma_dir = '/Applications/AFNI/suma_MNI_N27/'
basedir = '/Users/andric/Documents/workspace/hicre/'
ct_fname = 'CTallregionsBOTH.csv'
ct = pd.read_csv(os.path.join(basedir, ct_fname))
ctnames = pd.Series(ct.columns[3:151], name='region_name')

# see above for how I made these 1D labels files
lh_labels = np.loadtxt(os.path.join(basedir, 'lh_node_labels.1D.dset'))
rh_labels = np.loadtxt(os.path.join(basedir, 'rh_node_labels.1D.dset'))

# this is same as "lh.aparc.a2009s.annot.1D.cmap" and
# "rh.aparc.a2009s.annot.1D.cmap"
cmap_fname = 'rois.aparc.cmap'
rois = open(os.path.join(basedir, cmap_fname), 'r').readlines()

nm_rows = np.array(rois)[np.arange(1719, 1869, 2)]
idents = np.array(map(int,
                      [rw.split()[5].split('(')[1].split(')')[0]
                          for rw in nm_rows]))
idents_f = np.delete(idents, np.where(np.in1d(idents, 1644825)))
lh_idents_dict = dict(zip(np.array(idents_f), ctnames[0:74]))
rh_idents_dict = dict(zip(np.array(idents_f), ctnames[74:148]))

data_fname = 'TtestCTctrlminusblind2.txt'
data = open(os.path.join(basedir, data_fname)).readlines()
tvals = []
for b in data:
    tvals.append(b.split()[1])

tvals = np.array(tvals, dtype=np.float64)
tvals_table = np.column_stack([ctnames, tvals])
tvals_dict = dict(zip(ctnames, tvals))

for h in ['lh', 'rh']:
    print '%s -- ' % h+time.ctime()
    roi_aparc = '%s.aparc.a2009s.annot.1D.roi' % h
    aparc = np.loadtxt(os.path.join(suma_dir, roi_aparc))
    ncols = 1
    surf_out = np.array(np.zeros(len(aparc)*ncols)).reshape(len(aparc), ncols)
    if h == 'lh':
        lbls = lh_labels
        indents_dict = lh_idents_dict
    elif h == 'rh':
        lbls = rh_labels
        indents_dict = rh_idents_dict

    for i in xrange(len(lbls[:, 1])):
        try:
            region = indents_dict[int(lbls[i, 1])]
            surf_out[i, :] = tvals_dict[region]
        except:
            surf_out[i, :] = np.zeros(ncols)
    labels_out = '%s_TtestCTctrlminusblind2.1D' % h
    np.savetxt(os.path.join(basedir, labels_out),
               np.column_stack((aparc[:, 0], surf_out)), fmt='%i %f')

#!/usr/bin/env python
"""
Major revision on Mon Apr 20 17:18:49 2015

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
ct = pd.read_csv('CTallregionsBOTH.csv')
ctnames = pd.Series(ct.columns[3:151], name='region_name')
clrs = pd.read_csv('colorsSCB_CB.csv')
clrs_frc = []
for i in xrange(len(clrs.loc[:, 'colorRGB'])):
        clrs_frc.append([round(num/255., 5) for num in map(int,
                         clrs.loc[:, 'colorRGB'][i].split())])

# see above for how I made these 1D labels files
lh_labels = np.loadtxt('lh_node_labels.1D.dset')
rh_labels = np.loadtxt('rh_node_labels.1D.dset')

# this is same as "lh.aparc.a2009s.annot.1D.cmap" and
# "rh.aparc.a2009s.annot.1D.cmap"
rois = open('rois.aparc.cmap', 'r').readlines()

for dens in ['0.2', '0.3', '0.4', '0.5', '0.6']:
    CB_inclu = pd.read_csv('CB.inclusionlist.dens_%s.csv' % dens)
    SCB_inclu = pd.read_csv('SCB.inclusionlist.dens_%s.csv' % dens)

    nm_rows = np.array(rois)[np.arange(1719, 1869, 2)]
    idents = np.array(map(int,
                          [rw.split()[5].split('(')[1].split(')')[0]
                              for rw in nm_rows]))
    idents_f = np.delete(idents, np.where(np.in1d(idents, 1644825)))

    lh_idents_dict = dict(zip(np.array(idents_f), ctnames[0:74]))
    rh_idents_dict = dict(zip(np.array(idents_f), ctnames[74:148]))
    CBdict = dict(zip(CB_inclu.iloc[:, 1], CB_inclu.iloc[:, 2]))
    SCBdict = dict(zip(SCB_inclu.iloc[:, 1], SCB_inclu.iloc[:, 2]))

    for g in ['CB', 'SCB']:
        for h in ['lh', 'rh']:
            print '%s -- %s -- ' % (g, h)+time.ctime()
            roi_aparc = '%s.aparc.a2009s.annot.1D.roi' % h
            aparc = np.loadtxt(os.path.join(suma_dir, roi_aparc))
            new_rgb = np.array(np.zeros(len(aparc)*3)).reshape(len(aparc), 3)
            if h == 'lh':
                lbls = lh_labels
                indents_dict = lh_idents_dict
            elif h == 'rh':
                lbls = rh_labels
                indents_dict = rh_idents_dict
            if g == 'CB':
                dd = CBdict
            elif g == 'SCB':
                dd = SCBdict

            for i in xrange(len(lbls[:, 1])):
                try:
                    m = int(dd[indents_dict[int(lbls[:, 1][i])]])
                    tt = clrs[clrs.loc[:, 'group'] == g]
                    new_rgb[i, :] = clrs_frc[tt[tt['module'] == m].index[0]]
                except:
                    new_rgb[i, :] = np.zeros(3)
            mod_labels_out = '%s_%smod_labels.dens_%s.1D' % (h, g, dens)
            np.savetxt(mod_labels_out, np.column_stack((aparc[:, 0], new_rgb)),
                       fmt='%i %f %f %f')

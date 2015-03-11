#!/usr/bin/env python

"""
ConvertDset -i lh.aparc.a2009s.annot.niml.dset -o_1Dp -prepend_node_index_1D -prefix lh_node_labels
ConvertDset -i rh.aparc.a2009s.annot.niml.dset -o_1Dp -prepend_node_index_1D -prefix rh_node_labels
"""

import time
import pandas as pd
import numpy as np

ct = pd.read_csv('CTallregionsBOTH.csv')
ctnames = pd.Series(ct.columns[3:151], name = 'region_name')
clrs = pd.read_csv('colorsSCB_CB.csv')
clrs_frc = []
for i in xrange(len(clrs.loc[:,'colorRGB'])):
        clrs_frc.append([round(num/255.,5) for num in map(int, clrs.loc[:,'colorRGB'][i].split())])

lh_labels = np.loadtxt('lh_node_labels.1D.dset')   # see above for how I made this
rh_labels = np.loadtxt('rh_node_labels.1D.dset')

rois = open('rois.aparc.cmap','r').readlines()   # this is same as "lh.aparc.a2009s.annot.1D.cmap" and "rh.aparc.a2009s.annot.1D.cmap"
CB_inclu = pd.read_csv('CB.inclusionlist.csv')
SCB_inclu = pd.read_csv('SCB.inclusionlist.csv')

nm_rows = np.array(rois)[np.arange(1719, 1869, 2)]
idents = np.array(map(int, [rw.split()[5].split('(')[1].split(')')[0] for rw in nm_rows]))
idents_f = np.delete(idents, np.where(np.in1d(idents, 1644825)))

lh_idents_dict = dict(zip(np.array(idents_f), ctnames[0:74]))
rh_idents_dict = dict(zip(np.array(idents_f), ctnames[74:148]))
CBdict = dict(zip(CB_inclu.iloc[:,1], CB_inclu.iloc[:,2]))
SCBdict = dict(zip(SCB_inclu.iloc[:,1], SCB_inclu.iloc[:,2]))

g = 'SCB'
for h in ['lh','rh']:
    print '%s -- %s -- ' % (g, h)+time.ctime()
    aparc = np.loadtxt('/Applications/AFNI/suma_MNI_N27/%s.aparc.a2009s.annot.1D.roi' % h)
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

    for i in xrange(len(lbls[:,1])):
        try:
            m = int(dd[indents_dict[int(lbls[:,1][i])]])
            tt = clrs[clrs.loc[:,'group']==g]
            new_rgb[i,:] = clrs_frc[tt[tt['module']==m].index[0]]
            #new_rgb[i,:] = clrs_frc[clrs[clrs.loc[:,'module']==m].index[0]]
        except:
            new_rgb[i,:] = np.zeros(3)
    np.savetxt('%s_%smod_labels.1D' % (h, g), np.column_stack((aparc[:,0], new_rgb)), fmt='%i %f %f %f') 


"""
#tt = clrs[clrs.loc[:,'group']=='CB']


spl_ctn = [ct.split('.') for ct in ctnames]
spl_nms = [nm.split('_') for nm in nms]
for i in xrange(len(spl_nms)):
    if spl_nms[i][-1:] == ['wall']:
        print i

# 41 and 117 are '*h medial wall'. These are not in hicre regions. Below takes care of emitting them
#roi_ids = np.concatenate([np.arange(857,898), np.arange(899, 932), np.arange(933,974), np.arange(975,1008)])
#outs = [1644825]
#outs = [898, 932, 974]
#rems = np.where(np.in1d(np.arange(857,1008), outs))
#idents_f = np.delete(idents, np.where(np.in1d(idents, outs)))
#roi_ids = np.delete(inds, rems)

roi_idsS = pd.Series(roi_ids, name='numeric_id')
new_df = pd.concat([ctnames, roi_idsS], axis=1)
new_df.to_csv('hicreregions_to_afniROI.csv', index=False)

#nm_rows = np.array(rois)[np.arange(1719, 2020, 2)]
#idents = np.unique(np.array(map(int, [rw.split()[5].split('(')[1].split(')')[0] for rw in nm_rows])))

clrs = pd.read_csv('colorsSCB_CB.csv')
[num/255. for num in map(int, clrs.loc[:,'colorRGB'][0].split())]   # convert to 0-1 interval
clrs_frc = []
for i in xrange(len(clrs.loc[:,'colorRGB'])):
    clrs_frc.append([round(num/255.,5) for num in map(int, clrs.loc[:,'colorRGB'][i].split())])

#print ' '.join(map(str,pd.Series(clrs_frc)[0]))
#clrs_frc[clrs[clrs.loc[:,'module']==12].index[0]]

afnidict = dict(zip(roi_idsS, ctnames))
CBmods = pd.read_csv('CB.inclusionlist.csv')
CBdict = dict(zip(CBmods.iloc[:,1], CBmods.iloc[:,2]))

#get the region_id to the module_id
m = int(CBdict[afnidict[1007]])
clrs_frc[clrs[clrs.loc[:,'module']==m].index[0]]

#get the module_id to the RGB color
# ' '.join(map(str, clrs_frc[clrs[clrs.loc[:,'module']==m].index[0]]))+'\n'

aparc = np.loadtxt('/Applications/AFNI/suma_MNI_N27/lh.aparc.a2009s.annot.1D.roi')

#for i in xrange(len(apar[:,1])):
new_rgb = np.array(np.zeros(len(aparc)*3)).reshape(len(aparc), 3)
for i in xrange(10):
    r_id = int(aparc[i,:][1])
    m = int(CBdict[afnidict[r_id]])
    new_rgb[i,:] = clrs_frc[clrs[clrs.loc[:,'module']==m].index[0]]









cm_names = []
for i in xrange(len(ctnames)):
    print ctnames[i]
    spn = ctnames[i].split('.')
    print spn
    if spn[0] == 'L':
        cm_names.append('#ctx_lh_%s_and_%s_%s' % (spn[1], spn[2], spn[3]))
    elif spn[0] == 'R':
        cm_names.append('#ctx_rh_%s_and_%s_%s' % (spn[1], spn[2], spn[3]))


import mmap
f = open('rois.aparc.cmap')
s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
if s.find('blabla') != -1:
        print 'true'

"""

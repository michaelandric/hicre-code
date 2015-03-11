#!~/anaconda/bin/python

from subprocess import Popen, PIPE
from shlex import split
import numpy as np
from time import ctime

class TreeParser(object):
    '''This is a method to get the tree parsed at the highest hierarchical level'''

    def get_hierarchical(self, tr, tr_outname, Nmods_name):
        '''This gets the hierarchy tree at the highest level and the number of modules at that level'''
        cmdargs = split('hierarchy -n %s' % tr)
        print ctime()+' :::\n'
        print cmdargs
        p = Popen(cmdargs, stdout=PIPE).communicate()
        h = int(p[0].split()[3]) - 1
        print ctime()+' :::\n'
        print h
        cmdargs = split('hierarchy -l %d %s' % (h, tr))
        #f = open(tr_outname, 'w')
        tree = Popen(cmdargs, stdout=PIPE).communicate()
        #f = open(tr_outname, 'w')
        #f.write(tree[0])
        #f.close()
        print ctime()+' :::\n'
        print 'done writing the tree'
        
        mods = []
        for x in xrange(len(tree[0].split('\n'))-1):
            mods.append(tree[0].split('\n')[x].split()[1])
        m2 = map(int, mods)
        s2 = set(m2)
        toremove = []
        for mod_id in s2:
            if m2.count(mod_id) < 2:
                toremove.append(mod_id)
        for mod_id in toremove:
            s2.remove(mod_id)
        #N_mods = str(len(set(mods)))
        N_mods = str(len(set(s2)))
        print ctime()+' :::\n'
        print N_mods+' is the N_mods'
        ff = open(Nmods_name, 'w')
        ff.write(N_mods+'\n')
        ff.close()
        print ctime()+' :::\n'
        print 'done writing N_mods'


if __name__ == "__main__":

    TP = TreeParser()

    groups = ['CB', 'LB', 'SCB', 'SLB']
    for g in groups:
        for i in np.arange(.10,.61,.1):
            for n in xrange(100):
                for nn in xrange(100):
                    #tree_in = '/home/michaeljames.andric/hicre/trees/%s_dens%s_tree.iter%s.tree' % (g, i, n)
                    #tree_in = '/home/michaeljames.andric/hicre/random_trees/rand_%s_dens%s.iter%s.tree' % (g, i, n)
                    tree_in = '/home/michaeljames.andric/hicre/null_trees/Null_%s_dens%s.graph%s.iter%s.tree' % (g, i, n, nn)
                    #tree_out = '/home/michaeljames.andric/hicre/tree_highest/%s_dens%s_tree.iter%s.highesttree' % (g, i, n)
                    #tree_out = '/home/michaeljames.andric/hicre/random_tree_highest/rand_%s_dens%s.iter%s.highesttree' % (g, i, n)
                    tree_out = '/home/michaeljames.andric/hicre/null_tree_highest/Null_%s_dens%s.graph%s.iter%s.highesttree' % (g, i, n, nn)
                    #Nmodsname = '/home/michaeljames.andric/hicre/N_mods_nonSingle/%s_dens%s.iter%s.Nmods' % (g, i, n)
                    #Nmodsname = '/home/michaeljames.andric/hicre/random_N_mods_nonSingle/rand_%s_dens%s.iter%s.Nmods' % (g, i, n)
                    Nmodsname = '/home/michaeljames.andric/hicre/null_N_mods_nonSingle/Null_%s_dens%s.graph%s.iter%s.Nmods' % (g, i, n, nn)

                    TP.get_hierarchical(tree_in, tree_out, Nmodsname)


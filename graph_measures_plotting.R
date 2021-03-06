# plotting distributions of graph features
library(dplyr)
library(ggplot2)
library(gridExtra)
setwd('~/Documents/workspace/hicre/')

# clustering coefficient data
cb <- read.table('clustering_coefficient/CB.dens_0.1.clust_coef')
scb <- read.table('clustering_coefficient/SCB.dens_0.1.clust_coef')
cc <- tbl_df(data.frame(cb, scb))
names(cc) <- c('cb', 'scb')
h1 <- qplot(cb, data=cc, geom='histogram', ylim=c(0,40), binwidth=.025, xlab='Clustering Coefficients', main='CB') + theme_bw()
h2 <- qplot(scb, data=cc, geom='histogram', ylim=c(0,40), binwidth=.025, xlab='Clustering Coefficients', main='SCB') + theme_bw()
d1 <- qplot(cb, data=cc, geom='density', fill=I('black'), xlab='Clustering Coefficients', main='CB') + theme_bw()
d2 <- qplot(scb, data=cc, geom='density', fill=I('black'), xlab='Clustering Coefficients', main='SCB') + theme_bw()

pdf('clustering_coefficient/Clustering_Coefficients.pdf', width=11)
grid.arrange(h1, h2, ncol=2)
grid.arrange(d1, d2, ncol=2)
dev.off()

cc_diff <- apply(cc, 1, diff)
h1 <- qplot(cc_diff, geom='histogram', xlim=c(-1, 1), binwidth=.05, xlab='Clustering differences', main='Difference between CB and SCB') + theme_bw()
pdf('clustering_coefficient/Clustering_Coefficients_diff.pdf')
h1
dev.off()


# betweenness centrality data
cb <- read.table('betweenness_centrality/CB.dens_0.1.btwn_cntr')
scb <- read.table('betweenness_centrality/SCB.dens_0.1.btwn_cntr')
bc <- tbl_df(data.frame(cb, scb))
names(bc) <- c('cb', 'scb')
h1 <- qplot(cb, data=bc, geom='histogram', ylim=c(0, 450), xlim=c(0, .03), binwidth=.0005, xlab='Betweenness Centrality', main='CB') + theme_bw()
h2 <- qplot(scb, data=bc, geom='histogram', ylim=c(0, 450), xlim=c(0, .03), binwidth=.0005, xlab='Betweenness Centrality', main='SCB') + theme_bw()
d1 <- qplot(cb, data=bc, geom='density', ylim=c(0, 800), xlim=c(0, .03), fill=I('black'), xlab='Betweenness Centrality', main='CB') + theme_bw()
d2 <- qplot(scb, data=bc, geom='density', ylim=c(0, 800), xlim=c(0, .03), fill=I('black'), xlab='Betweenness Centrality', main='SCB') + theme_bw()

pdf('betweenness_centrality/Betweenness_Centrality.pdf', width=11)
grid.arrange(h1, h2, ncol=2)
grid.arrange(d1, d2, ncol=2)
dev.off()


# degree data
cb <- read.table('degrees/CB.dens_0.1.degrees')
scb <- read.table('degrees/SCB.dens_0.1.degrees')
degs <- tbl_df(data.frame(cb, scb))
names(degs) <- c('cb', 'scb')
h1 <- qplot(cb, data=degs, geom='histogram', xlim=c(0, 70), ylim=c(0, 45), binwidth=2.5, xlab='Degrees', main='CB') + theme_bw()
h2 <- qplot(scb, data=degs, geom='histogram', xlim=c(0, 70), ylim=c(0, 45), binwidth=2.5, xlab='Degrees', main='SCB') + theme_bw()
d1 <- qplot(cb, data=degs, geom='density', xlim=c(0, 75), fill=I('black'), xlab='Degrees', main='CB') + theme_bw()
d2 <- qplot(scb, data=degs, geom='density', xlim=c(0, 75), fill=I('black'), xlab='Degrees', main='SCB') + theme_bw()

pdf('degrees/Degree_hists.pdf', width=11)
grid.arrange(h1, h2, ncol=2)
grid.arrange(d1, d2, ncol=2)
dev.off()

deg_diff <- apply(degs, 1, diff)
h1 <- qplot(deg_diff, geom='histogram', binwidth=2.5, xlim=c(-50, 50), xlab='Degree differences', main='Difference between CB and SCB') + theme_bw()
pdf('degrees/Degree_hists_diff.pdf')
h1
dev.off()


# ggplot(cc, aes(cb), ylim=c(0,40)) + geom_histogram(fill='black', binwidth=.025, xlab='Clustering Coefficients') + theme_bw() + ggtitle('CB')
# ggplot(cc, aes(scb)) + geom_histogram(fill='black', binwidth=.025, xlab='Clustering Coefficients') + theme_bw() + ggtitle('SCB')


rn <- read.csv('region_names.csv')
cb <- read.table('clustering_coefficient/CB.dens_0.1.clust_coef')
scb <- read.table('clustering_coefficient/SCB.dens_0.1.clust_coef')
cc <- tbl_df(data.frame(rn, round(cb, 5), round(scb, 5), round(cb-scb, 5)))
names(cc) <- c('region', 'cb', 'scb', 'diff')
write.csv(cc, 'clustering_coefficient/clustering_coefficient_dat.csv', quote=FALSE, row.names=FALSE)

cb <- read.table('degrees/CB.dens_0.1.degrees')
scb <- read.table('degrees/SCB.dens_0.1.degrees')
deg <- tbl_df(data.frame(rn, round(cb, 5), round(scb, 5), round(cb-scb, 5)))
names(deg) <- c('region', 'cb', 'scb', 'diff')
write.csv(deg, 'degrees/degrees_dat.csv', quote=FALSE, row.names=FALSE)
# setting up more plots
# below is data from split (9 v. 9 within groups) and from split between groups
setwd('~/Documents/workspace/hicre/')
library(dplyr)
library(ggplot2)

pdf("plotting_similarity_ARI.pdf", paper="USr", width=8.5)
for (p in seq(.2, .6, .1))
{
    # Adjusted Rand
    cb_ari <- read.table(paste('withinCB_dens',p,'_ARI.txt', sep=''))$V1
    scb_ari <- read.table(paste('withinSCB_dens',p,'_ARI.txt', sep=''))$V1
    b_ari <- read.table(paste('betweenCB_SCB_dens',p,'_ARI.txt', sep=''))$V1
    
    repnames <- c(rep("CB", length(cb_ari)), rep("SCB", length(scb_ari)), rep("BTWN", length(b_ari)))
    ar_df <- tbl_df(data.frame(c(cb_ari, scb_ari, b_ari), repnames))
    names(ar_df) <- c("AdjRand", "Group")
    print(summary(b_ari))
    print(qplot(AdjRand, data = ar_df, geom="density", fill=Group, alpha=I(.66), xlim=c(0,1), main=paste("Density ",p*100,"%", sep=""), xlab="Adjusted Rand Score") + theme(panel.background = element_rect(fill="white")))
}
dev.off()


pdf("plotting_similarity_NMI.pdf", paper="USr", width=8.5)
for (p in seq(.2, .6, .1))
{
# Normalized Mutual Information
cb_nmi <- read.table(paste('withinCB_dens',p,'_NMI.txt', sep=''))$V1
scb_nmi <- read.table(paste('withinSCB_dens',p,'_NMI.txt', sep=''))$V1
b_nmi <- read.table(paste('betweenCB_SCB_dens',p,'_NMI.txt', sep=''))$V1

repnames <- c(rep("CB", length(cb_nmi)), rep("SCB", length(scb_nmi)), rep("BTWN", length(b_nmi)))
nm_df <- tbl_df(data.frame(c(cb_nmi, scb_nmi, b_nmi), repnames))
names(nm_df) <- c("NMI", "Group")
print(summary(b_nmi))
print(qplot(NMI, data = nm_df, geom="density", fill=Group, alpha=I(.66), xlim=c(0,1), main=paste("Density ",p*100,"%", sep=""), xlab="Normalized Mutual Information") + theme(panel.background = element_rect(fill="white")))
}
dev.off()

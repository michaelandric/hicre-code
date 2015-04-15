# below is data from split (9 v. 9 within groups) and from split between groups
setwd('~/Documents/workspace/hicre/')
library(dplyr)

# ks tests
for (p in seq(.2, .6, .1))
{
    # Normalized Mutual Information
    cb_nmi <- read.table(paste('withinCB_dens',p,'_NMI.txt', sep=''))$V1
    scb_nmi <- read.table(paste('withinSCB_dens',p,'_NMI.txt', sep=''))$V1
    b_nmi <- read.table(paste('betweenCB_SCB_dens',p,'_NMI.txt', sep=''))$V1
    
    repnames <- c(rep("CB", length(cb_nmi)), rep("SCB", length(scb_nmi)), rep("BTWN", length(b_nmi)))
    nm_df <- tbl_df(data.frame(c(cb_nmi, scb_nmi, b_nmi), repnames))
    names(nm_df) <- c("NMI", "Group")
    print(paste("Density is",p))
    print(paste("CB and SCB :"))
    print(ks.test(filter(nm_df, Group=='CB')$NMI, filter(nm_df, Group=='SCB')$NMI))
    print(paste("CB and BTWN"))
    print(ks.test(filter(nm_df, Group=='CB')$NMI, filter(nm_df, Group=='BTWN')$NMI))
    print(paste("SCB and BTWN"))
    print(ks.test(filter(nm_df, Group=='SCB')$NMI, filter(nm_df, Group=='BTWN')$NMI))
    print(paste("  ------------------------------------------  "))
}

# means and std dev
for (p in seq(.2, .6, .1))
{
    # Normalized Mutual Information
    cb_nmi <- read.table(paste('withinCB_dens',p,'_NMI.txt', sep=''))$V1
    scb_nmi <- read.table(paste('withinSCB_dens',p,'_NMI.txt', sep=''))$V1
    b_nmi <- read.table(paste('betweenCB_SCB_dens',p,'_NMI.txt', sep=''))$V1
    
    repnames <- c(rep("CB", length(cb_nmi)), rep("SCB", length(scb_nmi)), rep("BTWN", length(b_nmi)))
    nm_df <- tbl_df(data.frame(c(cb_nmi, scb_nmi, b_nmi), repnames))
    names(nm_df) <- c("NMI", "Group")
    print(paste("Density is",p))
    print(paste("Means: "))
    print(tapply(nm_df$NMI, nm_df$Group, mean))
    print(paste("STD: "))
    print(tapply(nm_df$NMI, nm_df$Group, sd))
    print(paste("  ------------------------------------------  "))
}
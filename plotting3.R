# setting up more plots
# below is data from split (9 v. 9 within groups) and from split between groups
library(dplyr)
library(ggplot2)
# Adjusted Rand Index
cb_ari <- read.table('AG_withinCB_ARI.txt')$V1
scb_ari <- read.table('AG_withinSCB_ARI.txt')$V1
b_ari <- read.table('AG_betweenCB_SCB_ARI.txt')$V1   # 'b' is for 'between' as in 'between CB and SCB'

# Normalized Mutual Information
cb_nmi <- read.table('AG_withinCB_NMI.txt')$V1
scb_nmi <- read.table('AG_withinSCB_NMI.txt')$V1
b_nmi <- read.table('AG_betweenCB_SCB_NMI.txt')$V1


repnames <- c(rep("CB", length(cb_ari)), rep("SCB", length(scb_ari)), rep("BTWN", length(b_ari)))
ar_df <- tbl_df(data.frame(c(cb_ari, scb_ari, b_ari), repnames))
names(ar_df) <- c("AdjRand", "Group")

repnames <- c(rep("CB", length(cb_nmi)), rep("SCB", length(scb_nmi)), rep("BTWN", length(b_nmi)))
nm_df <- tbl_df(data.frame(c(cb_nmi, scb_nmi, b_nmi), repnames))
names(nm_df) <- c("NMI", "Group")

pdf("similarity_measures_density_plotsAG.pdf", paper="USr", width=8.5)
qplot(AdjRand, data=ar_df, geom="density", fill=Group, alpha=I(.66)) + theme(panel.background = element_rect(fill="white"))
qplot(NMI, data = nm_df, geom="density", fill=Group, alpha=I(.66)) + theme(panel.background = element_rect(fill="white"))
dev.off()

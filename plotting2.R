# setting up more plots
# below is data from split (9 v. 9 within groups) and from split between groups
library(dplyr)
library(ggplot2)
# Adjusted Rand Index
cb_ari <- read.table('withinCB_ARI.txt')$V1
scb_ari <- read.table('withinSCB_ARI.txt')$V1
b_ari <- read.table('betweenCB_SCB_ARI.txt')$V1   # 'b' is for 'between' as in 'between CB and SCB'
null_ari <- read.table('Null_ARI.txt')$V1
# Normalized Mutual Information
cb_nmi <- read.table('withinCB_NMI.txt')$V1
scb_nmi <- read.table('withinSCB_NMI.txt')$V1
b_nmi <- read.table('betweenCB_SCB_NMI.txt')$V1
null_nmi <- read.table('Null_NMI.txt')$V1

repnames <- c(rep("CB", length(cb_ari)), rep("SCB", length(scb_ari)), rep("BTWN", length(b_ari)), rep("Null", length(null_ari)))
ar_df <- tbl_df(data.frame(c(cb_ari, scb_ari, b_ari, null_ari), repnames))
names(ar_df) <- c("AdjRand", "Group")

#qplot(AdjRand, data = ar_df, geom = "density", fill = Group, position = "stack", xlab = "Adjusted Rand Index") + scale_fill_manual(values = c("gray","dodgerblue","gray50","magenta")) + theme(panel.background = element_rect(fill = "white", colour = "black"))

#qplot(AdjRand, data = ar_df, geom = "density", fill = Group, alpha=I(.5), position = "stack", xlab = "Adjusted Rand Index") + theme(panel.background = element_rect(fill = "white", colour = "black"))
#qplot(AdjRand, data=ar_df, geom="density", fill=Group, alpha=I(.66)) + theme(panel.background = element_rect(fill="white"))

repnames <- c(rep("CB", length(cb_nmi)), rep("SCB", length(scb_nmi)), rep("BTWN", length(b_nmi)), rep("Null", length(null_nmi)))
nm_df <- tbl_df(data.frame(c(cb_nmi, scb_nmi, b_nmi, null_nmi), repnames))
names(nm_df) <- c("NMI", "Group")

#qplot(NMI, data = nm_df, geom="density", fill = Group, alpha=I(.5), position = "stack", xlab = "Normalized Mutual Information") + scale_fill_manual(values = c("gray","dodgerblue","gray50","magenta")) + theme(panel.background = element_rect(fill = "white", colour = "black"))

#qplot(NMI, data = nm_df, geom = "density", colour = Group) + theme(panel.background = element_rect(fill = "white", colour = "black"))

#qplot(NMI, data = nm_dff, fill = Group, alpha=I(.5), position = "stack", xlab = "Normalized Mutual Information") + theme(panel.background = element_rect(fill="white", colour="black"))

pdf("similarity_measures_density_plots.pdf", paper="USr", width=8.5)
qplot(AdjRand, data=ar_df, geom="density", fill=Group, alpha=I(.66)) + theme(panel.background = element_rect(fill="white"))
qplot(NMI, data = nm_df, geom="density", fill=Group, alpha=I(.66)) + theme(panel.background = element_rect(fill="white"))
dev.off()

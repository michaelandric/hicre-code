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

#repnames <- c(rep("CB", length(cb_ari)), rep("SCB", length(scb_ari)), rep("BTWN", length(b_ari)), rep("Null", length(null_ari)))
repnames <- c(rep("CB", length(cb_ari)), rep("SCB", length(scb_ari)), rep("BTWN", length(b_ari)))
#ar_df <- tbl_df(data.frame(c(cb_ari, scb_ari, b_ari, null_ari), repnames))
ar_df <- tbl_df(data.frame(c(cb_ari, scb_ari, b_ari), repnames))
names(ar_df) <- c("AdjRand", "Group")

#qplot(AdjRand, data = ar_df, geom = "density", fill = Group, position = "stack", xlab = "Adjusted Rand Index") + scale_fill_manual(values = c("gray","dodgerblue","gray50","magenta")) + theme(panel.background = element_rect(fill = "white", colour = "black"))

#qplot(AdjRand, data = ar_df, geom = "density", fill = Group, alpha=I(.5), position = "stack", xlab = "Adjusted Rand Index") + theme(panel.background = element_rect(fill = "white", colour = "black"))
#qplot(AdjRand, data=ar_df, geom="density", fill=Group, alpha=I(.66)) + theme(panel.background = element_rect(fill="white"))

#repnames <- c(rep("CB", length(cb_nmi)), rep("SCB", length(scb_nmi)), rep("BTWN", length(b_nmi)), rep("Null", length(null_nmi)))
repnames <- c(rep("CB", length(cb_nmi)), rep("SCB", length(scb_nmi)), rep("BTWN", length(b_nmi)))
#nm_df <- tbl_df(data.frame(c(cb_nmi, scb_nmi, b_nmi, null_nmi), repnames))
nm_df <- tbl_df(data.frame(c(cb_nmi, scb_nmi, b_nmi), repnames))
names(nm_df) <- c("NMI", "Group")

#qplot(NMI, data = nm_df, geom="density", fill = Group, alpha=I(.5), position = "stack", xlab = "Normalized Mutual Information") + scale_fill_manual(values = c("gray","dodgerblue","gray50","magenta")) + theme(panel.background = element_rect(fill = "white", colour = "black"))

#qplot(NMI, data = nm_df, geom = "density", colour = Group) + theme(panel.background = element_rect(fill = "white", colour = "black"))

#qplot(NMI, data = nm_dff, fill = Group, alpha=I(.5), position = "stack", xlab = "Normalized Mutual Information") + theme(panel.background = element_rect(fill="white", colour="black"))

pdf("similarity_measures_density_plots.pdf", paper="USr", width=8.5)
qplot(AdjRand, data=ar_df, geom="density", fill=Group, alpha=I(.66)) + theme(panel.background = element_rect(fill="white"))
qplot(NMI, data = nm_df, geom="density", fill=Group, alpha=I(.66)) + theme(panel.background = element_rect(fill="white"))
dev.off()

pdf("similarity_measure_NMI.pdf", paper="USr", width=8.5)
qplot(NMI, data = nm_df, geom="density", fill=Group, alpha=I(.66), xlim=c(0,1), xlab="Normalized Mutual Information") + theme(panel.background = element_rect(fill="white"))
dev.off()



# ----- below deals with age/gender residuals ----------------
nm_ag_cb <- read.table('AGtoReal_CB_NMI.txt')$V1
nm_ag_scb <- read.table('AGtoReal_SCB_NMI.txt')$V1
ar_ag_cb <- read.table('AGtoReal_CB_ARI.txt')$V1
ar_ag_scb <- read.table('AGtoReal_SCB_ARI.txt')$V1

ar_cb <- read.table("CB_ARI.txt")[,1]
ar_scb <- read.table("SCB_ARI.txt")[,1]
nm_cb <- read.table("CB_NMI.txt")[,1]
nm_scb <- read.table("SCB_NMI.txt")[,1]


repnames <- c(rep("CB", length(cb_nmi)), rep("CB_AG", length(nm_ag_cb)), rep("SCB", length(scb_nmi)), rep("SCB_AG", length(nm_ag_scb)))
#repnames <- c(rep("CB", length(nm_cb)), rep("CB_AG", length(nm_ag_cb)), rep("SCB", length(nm_scb)), rep("SCB_AG", length(nm_ag_scb)))
ag_nm_df <- tbl_df(data.frame(c(cb_nmi, nm_ag_cb, scb_nmi, nm_ag_scb), repnames))
#ag_nm_df <- tbl_df(data.frame(c(nm_cb, nm_ag_cb, nm_scb, nm_ag_scb), repnames))
names(ag_nm_df) <- c("NMI", "Group")

repnames <- c(rep("CB", length(cb_ari)), rep("CB_AG", length(ar_ag_cb)), rep("SCB", length(scb_ari)), rep("SCB_AG", length(ar_ag_scb)))
#repnames <- c(rep("CB", length(ar_cb)), rep("CB_AG", length(ar_ag_cb)), rep("SCB", length(ar_scb)), rep("SCB_AG", length(ar_ag_scb)))
ag_ar_df <- tbl_df(data.frame(c(cb_ari, ar_ag_cb, scb_ari, ar_ag_scb), repnames))
#ag_ar_df <- tbl_df(data.frame(c(ar_cb, ar_ag_cb, ar_scb, ar_ag_scb), repnames))
names(ag_ar_df) <- c("AdjRand", "Group")

qplot(AdjRand, data=ag_ar_df, geom="density", fill=Group, alpha=I(.66)) + theme(panel.background = element_rect(fill="white"))
qplot(NMI, data = ag_nm_df, geom="density", fill=Group, alpha=I(.66)) + theme(panel.background = element_rect(fill="white"))
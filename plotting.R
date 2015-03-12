#testing plots for similarity measures

library(ggplot2)

ar_cb <- read.table("CB_ARI.txt")[,1]
ar_scb <- read.table("SCB_ARI.txt")[,1]
ar_btwn <- read.table("btwnCB_SCB_ARI.txt")[,1]
repnames <- c(rep("CB", length(ar_cb)), rep("SCB", length(ar_cb)), rep("BTWN", length(ar_btwn)))
ar_df <- data.frame(c(ar_cb, ar_scb, ar_btwn), repnames)
names(ar_df) <- c("AdjRand", "Group")


nm_cb <- read.table("CB_NMI.txt")[,1]
nm_scb <- read.table("SCB_NMI.txt")[,1]
nm_btwn <- read.table("btwnCB_SCB_NMI.txt")[,1]
repnames <- c(rep("CB", length(nm_cb)), rep("SCB", length(nm_cb)), rep("BTWN", length(nm_btwn)))
nm_df <- data.frame(c(nm_cb, nm_scb, nm_btwn), repnames)
names(nm_df) <- c("NMI", "Group")


pdf("CB_SCB_similarity_measures.Density.pdf", paper = "USr", width = 8.5)
qplot(AdjRand, data = ar_df, geom = "density", fill = Group, position = "stack", xlab = "Adjusted Rand Index") + scale_fill_manual(values = c("yellow","magenta","cyan")) + theme(panel.background = element_rect(fill = "white", colour = "black"))
qplot(NMI, data = nm_df, geom = "density", fill = Group, position = "stack", xlab = "Normalized Mutual Information") + scale_fill_manual(values = c("yellow","magenta","cyan")) + theme(panel.background = element_rect(fill = "white", colour = "black"))
dev.off()


library(dplyr)
ct <- tbl_df(read.csv('CTallregionsBOTH.csv'))
cb <- filter(ct, Group=='CB')
scb <- filter(ct, Group=='SCB')
ssinfo <- tbl_df(read.table('ss_info.txt'))
names(ssinfo) <- c('Group','ss','gender','Age')

regions <- names(ct)[4:151]

# check the interaction
cb_inters <- c()
scb_inters <- c()
for (i in c(4:151))
{
    tmp_cb <- data.frame(cb[,i], filter(ssinfo, Group=='CB')[,3:4])
    tmp_scb <- data.frame(scb[,i], filter(ssinfo, Group=='SCB')[,3:4])
    names(tmp_cb) <- c('region','gender','Age')
    names(tmp_scb) <- c('region','gender','Age')
    cb_inters <- c(cb_inters, summary(lm(region~gender*Age, data=tmp_cb))$coefficients[,4][[4]])
    scb_inters <- c(scb_inters, summary(lm(region~gender*Age, data=tmp_scb))$coefficients[,4][[4]])
}
print(length(which(cb_inters < 0.05)))
print(length(which(scb_inters < 0.05)))

# Now looking at main effects
cb_resids <- c()
scb_resids <- c()
for (i in c(4:151))
{
    tmp_cb <- data.frame(cb[,i], filter(ssinfo, Group=='CB')[,3:4])
    tmp_scb <- data.frame(scb[,i], filter(ssinfo, Group=='SCB')[,3:4])
    names(tmp_cb) <- c('region','gender','Age')
    names(tmp_scb) <- c('region','gender','Age')
    cb_resids <- c(cb_resids, lm(region~., data=tmp_cb)$residuals)
    scb_resids <- c(scb_resids, lm(region~., data=tmp_scb)$residuals)
}
cb_resids_mat <- matrix(cb_resids, nrow=dim(cb)[1])
scb_resids_mat <- matrix(scb_resids, nrow=dim(scb)[1])

rs_df <- tbl_df(data.frame(rbind(cb_resids_mat, scb_resids_mat)))
rs_df <- tbl_df(data.frame(c(as.character(cb$Group), as.character(scb$Group)), round(rs_df,4)))
names(rs_df) <- c('Group', regions)
rs_df$Group <- c(as.character(cb$Group), as.character(scb$Group))

write.csv(rs_df, "CTage_gender_regr.csv", quote=F, row.names=F)


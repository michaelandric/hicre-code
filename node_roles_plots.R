# plot node roles 
library(dplyr)
library(ggplot2)
setwd('~/Documents/workspace/hicre/node_roles/')
cb_p <- tbl_df(read.table('CB_dens0.1_part_coef.txt'))
cb_wz <- tbl_df(read.table('CB_dens0.1_within_mod_Z.txt'))
scb_p <- tbl_df(read.table('SCB_dens0.1_part_coef.txt'))
scb_wz <- tbl_df(read.table('SCB_dens0.1_within_mod_Z.txt'))

n_reps <- length(cb_p$V1)
value <- c(cb_p$V1, cb_wz$V1, scb_p$V1, scb_wz$V1)
role <- c(rep(c(rep('p_coef', n_reps), rep('within_mod_z', n_reps)), 2))
group <- c(rep('CB', n_reps*2), rep('SCB', n_reps*2))
role_df <- tbl_df(data.frame(value, role, group))

part_coefs <- c(cb_p$V1, scb_p$V1)
within_mod_z <- c(cb_wz$V1, scb_wz$V1)
group <- c(rep('CB', n_reps), rep('SCB', n_reps))
roles_df <- tbl_df(data.frame(part_coefs, within_mod_z, group))

regions_labels <- tbl_df(read.csv('../region_names_labels.csv'))
cb_incl <- tbl_df(read.csv('../CB.inclusionlist.csv'))[,c(2,3)]
scb_incl <- tbl_df(read.csv('../SCB.inclusionlist.csv'))[,c(2,3)]

l_indices <- which(regions_labels$label=='L')
v_indices <- which(regions_labels$label=='V')
cb_p_l <- cb_p[l_indices, ]
scb_p_l <- scb_p[l_indices, ]
cb_wz_l <- cb_wz[l_indices, ]
scb_wz_l <- scb_wz[l_indices, ]
cb_p_v <- cb_p[v_indices, ]
scb_p_v <- scb_p[v_indices, ]
cb_wz_v <- cb_wz[v_indices, ]
scb_wz_v <- scb_wz[v_indices, ]
part_coefs_l <- c(cb_p_l$V1, scb_p_l$V1)
part_coefs_v <- c(cb_p_v$V1, scb_p_v$V1)
part_coefs_lv <- c(part_coefs_l, part_coefs_v)
within_mod_z_l <- c(cb_wz_l$V1, scb_wz_l$V1)
within_mod_z_v <- c(cb_wz_v$V1, scb_wz_v$V1)
within_mod_z_lv <- c(within_mod_z_l, within_mod_z_v)
group_l <- c(rep('CB', length(l_indices)), rep('SCB', length(l_indices)))
group_v <- c(rep('CB', length(v_indices)), rep('SCB', length(v_indices)))
group_lv <- c(group_l, group_v)
region_type <- c(rep('Language', length(l_indices)*2), rep('Visual', length(v_indices)*2))
roles_df_lv <- tbl_df(data.frame(part_coefs_lv, within_mod_z_lv, group_lv, region_type))


pdf('Node_roles_plots.pdf')
ggplot(roles_df, aes(x=part_coefs, y=within_mod_z, color=group)) + geom_point() + scale_x_continuous(breaks=c(.05,.62,.8)) + scale_y_continuous(breaks=c(2.5)) + expand_limits(x=c(0,1), y=c(-2,3)) + xlab('Participation Coef') + ylab('Within-module degree Z') + ggtitle('All regions') + theme_linedraw() 

ggplot(roles_df_lv, aes(x=part_coefs_lv, y=within_mod_z_lv, color=group_lv, shape=region_type)) + geom_point() + scale_x_continuous(breaks=c(.05,.62,.8)) + scale_y_continuous(breaks=c(2.5)) + expand_limits(x=c(0,1), y=c(-2,3)) + xlab('Participation Coef') + ylab('Within-module degree Z') + ggtitle('Language & Visual regions') + theme_linedraw() 
dev.off()

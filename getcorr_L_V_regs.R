# get correlation values
library(dplyr)
ctboth <- tbl_df(read.csv('CTallregionsBOTH.csv'))
regions_labels <- tbl_df(read.csv('region_names_labels.csv'))
cb_incl <- tbl_df(read.csv('CB.inclusionlist.csv'))[,c(2,3)]
scb_incl <- tbl_df(read.csv('SCB.inclusionlist.csv'))[,c(2,3)]

lregions <- filter(regions_labels, label=='L')$region
vregions <- filter(regions_labels, label=='V')$region
xregions <- filter(regions_labels, label=='X')$region
cb_l_filt <- filter(cb_incl, region%in% lregions)
cb_v_filt <- filter(cb_incl, region%in% vregions)
cb_x_filt <- filter(cb_incl, region%in% xregions)
scb_l_filt <- filter(scb_incl, region%in% lregions)
scb_v_filt <- filter(scb_incl, region%in% vregions)
scb_x_filt <- filter(scb_incl, region%in% xregions)

cb_l_table <- matrix(nrow=length(cb_l_filt$region) - 1, ncol=length(cb_l_filt$region))
colnames(cb_l_table) <- cb_l_filt$region
for (reg in cb_l_filt$region)
{
    other_regions <- cb_l_filt$region[which(cb_l_filt$region != reg)]
    reg_cors <- c()
    for (oreg in other_regions)
    {
        fc <- atanh(cor(ctboth[ctboth[,2] == 'CB', reg], ctboth[ctboth[, 2] == 'CB', oreg])[1])
        reg_cors <- c(reg_cors, fc)
    }
    cb_l_table[, reg] <- reg_cors
}

cb_v_table <- matrix(nrow=length(cb_v_filt$region) - 1, ncol=length(cb_v_filt$region))
colnames(cb_v_table) <- cb_v_filt$region
for (reg in cb_v_filt$region)
{
    other_regions <- cb_v_filt$region[which(cb_v_filt$region != reg)]
    reg_cors <- c()
    for (oreg in other_regions)
    {
        fc <- atanh(cor(ctboth[ctboth[,2] == 'CB', reg], ctboth[ctboth[, 2] == 'CB', oreg])[1])
        reg_cors <- c(reg_cors, fc)
    }
    cb_v_table[, reg] <- reg_cors
}

scb_l_table <- matrix(nrow=length(scb_l_filt$region) - 1, ncol=length(scb_l_filt$region))
colnames(scb_l_table) <- scb_l_filt$region
for (reg in scb_l_filt$region)
{
    other_regions <- scb_l_filt$region[which(scb_l_filt$region != reg)]
    reg_cors <- c()
    for (oreg in other_regions)
    {
        fc <- atanh(cor(ctboth[ctboth[,2] == 'SCB', reg], ctboth[ctboth[, 2] == 'SCB', oreg])[1])
        reg_cors <- c(reg_cors, fc)
    }
    scb_l_table[, reg] <- reg_cors
}

scb_v_table <- matrix(nrow=length(scb_v_filt$region) - 1, ncol=length(scb_v_filt$region))
colnames(scb_v_table) <- scb_v_filt$region
for (reg in scb_v_filt$region)
{
    other_regions <- scb_v_filt$region[which(scb_v_filt$region != reg)]
    reg_cors <- c()
    for (oreg in other_regions)
    {
        fc <- atanh(cor(ctboth[ctboth[,2] == 'SCB', reg], ctboth[ctboth[, 2] == 'SCB', oreg])[1])
        reg_cors <- c(reg_cors, fc)
    }
    scb_v_table[, reg] <- reg_cors
}

print(colMeans(cb_l_table))
print(mean(colMeans(cb_l_table)))
print(sd(colMeans(cb_l_table)))

print(colMeans(cb_v_table))
print(mean(colMeans(cb_v_table)))
print(sd(colMeans(cb_v_table)))

print(colMeans(scb_l_table))
print(mean(colMeans(scb_l_table)))
print(sd(colMeans(scb_l_table)))

print(colMeans(scb_v_table))
print(mean(colMeans(scb_v_table)))
print(sd(colMeans(scb_v_table)))
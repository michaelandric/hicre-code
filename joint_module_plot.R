# get joint counts for module to type of region
setwd('~/Documents/workspace/hicre/')
library(dplyr)
library(hexbin)
library(ggplot2)

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


within_l_cb <- c()
outside_l_cb <- c()
within_l_scb <- c()
outside_l_scb <- c()
prop_l_cb <- c()
prop_l_scb <- c()
for (reg in cb_l_filt$region)
{
    reg_com <- cb_l_filt$community[cb_l_filt$region==reg]
    within_l_cb <- c(within_l_cb, length(which(cb_l_filt$community==reg_com)))
    prop_l_cb <- c(prop_l_cb, length(which(cb_l_filt==reg_com))/length(which(reg_com == cb_incl$community)))
    outside_l_cb <- c(outside_l_cb, length(which(cb_v_filt$community==reg_com)))
}
for (reg in scb_l_filt$region)
{
    reg_com <- scb_l_filt$community[scb_l_filt$region==reg]
    within_l_scb <- c(within_l_scb, length(which(scb_l_filt$community==reg_com)))
    prop_l_scb <- c(prop_l_scb, length(which(scb_l_filt==reg_com))/length(which(reg_com == scb_incl$community)))
    outside_l_scb <- c(outside_l_scb, length(which(scb_v_filt$community==reg_com)))
}
cb_l_mod <- tbl_df(data.frame(cb_l_filt$region, within_l_cb, outside_l_cb))
scb_l_mod <- tbl_df(data.frame(scb_l_filt$region, within_l_scb, outside_l_scb))


within_v_cb <- c()
outside_v_cb <- c()
within_v_scb <- c()
outside_v_scb <- c()
prop_v_cb <- c()
prop_v_scb <- c()
for (reg in cb_v_filt$region)
{
    reg_com <- cb_v_filt$community[cb_v_filt$region==reg]
    within_v_cb <- c(within_v_cb, length(which(cb_v_filt$community==reg_com)))
    prop_v_cb <- c(prop_v_cb, length(which(cb_v_filt==reg_com))/length(which(reg_com == cb_incl$community)))
    outside_v_cb <- c(outside_v_cb, length(which(cb_l_filt$community==reg_com)))
}

for (reg in scb_v_filt$region)
{
    reg_com <- scb_v_filt$community[scb_v_filt$region==reg]
    within_v_scb <- c(within_v_scb, length(which(scb_v_filt$community==reg_com)))
    prop_v_scb <- c(prop_v_scb, length(which(scb_v_filt==reg_com))/length(which(reg_com == scb_incl$community)))
    outside_v_scb <- c(outside_v_scb, length(which(scb_l_filt$community==reg_com)))
}
cb_v_mod <- tbl_df(data.frame(cb_v_filt$region, within_v_cb, outside_v_cb))
scb_v_mod <- tbl_df(data.frame(scb_v_filt$region, within_v_scb, outside_v_scb))

cb_x_l <- c()
cb_x_v <- c()
scb_x_l <- c()
scb_x_v <- c()
for (reg in cb_x_filt$region)
{
    reg_com <- cb_x_filt$community[cb_x_filt$region==reg]
    cb_x_l <- c(cb_x_l, length(which(reg_com == cb_l_filt$community)))
    cb_x_v <- c(cb_x_v, length(which(reg_com == cb_v_filt$community)))
}
for (reg in scb_x_filt$region)
{
    reg_com <- scb_x_filt$community[scb_x_filt$region==reg]
    scb_x_l <- c(scb_x_l, length(which(reg_com == scb_l_filt$community)))
    scb_x_v <- c(scb_x_v, length(which(reg_com == scb_v_filt$community)))
}
x_dat <- tbl_df(data.frame(c(cb_x_l, scb_x_l), c(cb_x_v, scb_x_v), c(rep('CB', dim(cb_x_filt)[1]), rep('SCB', dim(scb_x_filt)[1]))))
colnames(x_dat) <- c('Lang', 'Vis', 'gr')

# l_dat <- tbl_df(data.frame(c(cb_l_mod$within_l_cb, scb_l_mod$within_l_scb), c(cb_l_mod$outside_l_cb, scb_l_mod$outside_l_scb), c(prop_l_cb, prop_l_scb), c(rep('CB', dim(cb_l_mod)[1]), rep('SCB', dim(scb_l_mod)[1]))))
l_dat <- tbl_df(data.frame(c(cb_l_mod$within_l_cb, scb_l_mod$within_l_scb), c(cb_l_mod$outside_l_cb, scb_l_mod$outside_l_scb), c(rep('CB', dim(cb_l_mod)[1]), rep('SCB', dim(scb_l_mod)[1]))))
#colnames(l_dat) <- c('within', 'outside', 'prop', 'gr')
colnames(l_dat) <- c('within', 'outside', 'gr')
# hexbinplot(outside ~ within, l_dat)
# v_dat <- tbl_df(data.frame(c(cb_v_mod$within_v_cb, scb_v_mod$within_v_scb), c(cb_v_mod$outside_v_cb, scb_v_mod$outside_v_scb), c(prop_v_cb, prop_v_scb), c(rep('CB', dim(cb_v_mod)[1]), rep('SCB', dim(scb_v_mod)[1]))))
# colnames(v_dat) <- c('within', 'outside', 'prop', 'gr')
v_dat <- tbl_df(data.frame(c(cb_v_mod$within_v_cb, scb_v_mod$within_v_scb), c(cb_v_mod$outside_v_cb, scb_v_mod$outside_v_scb), c(rep('CB', dim(cb_v_mod)[1]), rep('SCB', dim(scb_v_mod)[1]))))
colnames(v_dat) <- c('within', 'outside', 'gr')


# plot(hexbin(cb_l_mod$within_l_cb, cb_l_mod$outside_l_cb))
pdf('Cross_hexplots.pdf')
par(mfcol=c(1,2))
plot(hexbin(cb_l_mod$within_l_cb, cb_l_mod$outside_l_cb), main='CB Language', xlab='Language Regions', ylab='Visual Regions')
plot(hexbin(scb_l_mod$within_l_scb, scb_l_mod$outside_l_scb), main='SCB Language', xlab='Language Regions', ylab='Visual Regions')
plot(hexbin(cb_v_mod$within_v_cb, cb_v_mod$outside_v_cb), main='CB Visual', xlab='Visual Regions', ylab='Language Regions')
plot(hexbin(scb_v_mod$within_v_scb, scb_v_mod$outside_v_scb), main='SCB Visual', xlab='Visual Regions', ylab='Language Regions')
dev.off()

pdf('Cross_balloon_plots.pdf')
lp <- ggplot(l_dat, aes(x=within, y=outside, shape=gr, size=prop)) + geom_point() + scale_size_continuous(range=c(2,10)) + xlab('Connect within Language regions') + ylab('Connect to Visual Regions') + ggtitle('Language') + theme_bw()
lp
vp <- ggplot(v_dat, aes(x=within, y=outside, shape=gr, size=prop)) + geom_point() + scale_size_continuous(range=c(2,10)) + xlab('Connect within Visual regions') + ylab('Connect to Language Regions') + ggtitle('Visual') + theme_bw()
vp
dev.off()

pdf('Cross_comboballoon_plots.pdf')
aa = aggregate(l_dat$within, list(l_dat$gr, l_dat$outside, l_dat$within), length)
lp = ggplot(aa, aes(x=aa$Group.3, y=aa$Group.2, size=aa$x, shape=aa$Group.1)) + geom_point() + scale_size_continuous(range=c(2,10)) + xlab('Connect within Language regions') + ylab('Connect to Visual Regions') + ggtitle('Language') + theme_bw()
lp
aa = aggregate(v_dat$within, list(v_dat$gr, v_dat$outside, v_dat$within), length)
vp = ggplot(aa, aes(x=aa$Group.3, y=aa$Group.2, size=aa$x, shape=aa$Group.1)) + geom_point() + scale_size_continuous(range=c(2,10)) + xlab('Connect within Visual regions') + ylab('Connect to Language Regions') + ggtitle('Visual') + theme_bw()
vp
dev.off()

pdf('Cross_comboballoon_separategroups_bigticks_plots.pdf')
ll = filter(l_dat, gr=='CB')
aa = aggregate(ll$within, list(ll$gr, ll$outside, ll$within), length)
lp = ggplot(aa, aes(x=aa$Group.3, y=aa$Group.2, size=aa$x, shape=aa$Group.1)) + geom_point() + scale_x_continuous(minor_breaks=seq(1,20,1), breaks=seq(5, 20, 5)) + scale_y_continuous(minor_breaks=seq(1,20,1), breaks=seq(5, 20, 5)) + scale_size_continuous(range=c(2,10)) + xlab('Connect within Language regions') + ylab('Connect to Visual Regions') + ggtitle('CB Language') + theme_bw() + theme(panel.grid.minor = element_line(size=1), panel.grid.major= element_line(size=1.5)) + geom_text(aes(x=aa$Group.3, y=aa$Group.2, label=aa$x, size=3), hjust=2, vjust=-1)
lp
ll = filter(l_dat, gr=='SCB')
aa = aggregate(ll$within, list(ll$gr, ll$outside, ll$within), length)
lp = ggplot(aa, aes(x=aa$Group.3, y=aa$Group.2, size=aa$x, shape=aa$Group.1)) + geom_point() + scale_x_continuous(minor_breaks=seq(1,20,1), breaks=seq(5, 20, 5)) + scale_y_continuous(minor_breaks=seq(1,20,1), breaks=seq(5, 20, 5)) + scale_size_continuous(range=c(2,10)) + xlab('Connect within Language regions') + ylab('Connect to Visual Regions') + ggtitle('SCB Language') + theme_bw() + theme(panel.grid.minor = element_line(size=1), panel.grid.major= element_line(size=1.5)) + geom_text(aes(x=aa$Group.3, y=aa$Group.2, label=aa$x, size=3), hjust=2, vjust=-1)
lp
vv = filter(v_dat, gr=='CB')
aa = aggregate(vv$within, list(vv$gr, vv$outside, vv$within), length)
vp = ggplot(aa, aes(x=aa$Group.3, y=aa$Group.2, size=aa$x, shape=aa$Group.1)) + geom_point() + scale_x_continuous(minor_breaks=seq(1,20,1), breaks=seq(5, 20, 5)) + scale_y_continuous(minor_breaks=seq(1,20,1), breaks=seq(5, 20, 5)) + scale_size_continuous(range=c(2,10)) + xlab('Connect within Visual regions') + ylab('Connect to Language Regions') + ggtitle('CB Visual') + theme_bw() + theme(panel.grid.minor = element_line(size=1), panel.grid.major= element_line(size=1.5)) + geom_text(aes(x=aa$Group.3, y=aa$Group.2, label=aa$x, size=3), hjust=2, vjust=-1)
vp
vv = filter(v_dat, gr=='SCB')
aa = aggregate(vv$within, list(vv$gr, vv$outside, vv$within), length)
vp = ggplot(aa, aes(x=aa$Group.3, y=aa$Group.2, size=aa$x, shape=aa$Group.1)) + geom_point() + scale_x_continuous(minor_breaks=seq(1,20,1), breaks=seq(5, 20, 5)) + scale_y_continuous(minor_breaks=seq(1,20,1), breaks=seq(5, 20, 5)) + scale_size_continuous(range=c(2,10)) + xlab('Connect within Visual regions') + ylab('Connect to Language Regions') + ggtitle('SCB Visual') + theme_bw() + theme(panel.grid.minor = element_line(size=1), panel.grid.major= element_line(size=1.5)) + geom_text(aes(x=aa$Group.3, y=aa$Group.2, label=aa$x, size=3), hjust=2, vjust=-1)
vp
dev.off()


pdf('Cross_comboballoon_separategroups_setaxes2.pdf') # "2.pdf" because it reflects updated regions post-neurosynth labels
axlim = 25
ll = filter(l_dat, gr=='CB')
aa = aggregate(ll$within, list(ll$gr, ll$outside, ll$within), length)
lp = ggplot(aa, aes(x=aa$Group.3, y=aa$Group.2, size=aa$x, shape=aa$Group.1, label=aa$x)) + geom_point() + expand_limits(x=c(0,axlim), y=c(0,axlim)) + scale_x_continuous(minor_breaks=seq(0,axlim,1), breaks=seq(0,axlim,5)) + scale_y_continuous(minor_breaks=seq(0,axlim,1), breaks=seq(0,axlim,5)) + scale_size_continuous(range=c(2,10)) + xlab('Connect within Language regions') + ylab('Connect to Visual Regions') + ggtitle('CB Language') + theme_bw() + theme(panel.grid.minor = element_line(size=.2, linetype='dashed', color='gray25'), panel.grid.major= element_line(size=.5, color='gray25')) + geom_text(aes(x=aa$Group.3, y=aa$Group.2, label=aa$x, size=5), hjust=1.75, vjust=-1.5)
lp
ll = filter(l_dat, gr=='SCB')
aa = aggregate(ll$within, list(ll$gr, ll$outside, ll$within), length)
lp = ggplot(aa, aes(x=aa$Group.3, y=aa$Group.2, size=aa$x, label=aa$x)) + geom_point(shape=17) + expand_limits(x=c(0,axlim), y=c(0,axlim)) + scale_x_continuous(minor_breaks=seq(0,axlim,1), breaks=seq(0,axlim,5)) + scale_y_continuous(minor_breaks=seq(0,axlim,1), breaks=seq(0,axlim,5)) + scale_size_continuous(range=c(2,10)) + xlab('Connect within Language regions') + ylab('Connect to Visual Regions') + ggtitle('SCB Language') + theme_bw() + theme(panel.grid.minor = element_line(size=.2, linetype='dashed', color='gray25'), panel.grid.major= element_line(size=.5, color='gray25')) + geom_text(aes(x=aa$Group.3, y=aa$Group.2, label=aa$x, size=5), hjust=1.75, vjust=-1.5)
lp
vv = filter(v_dat, gr=='CB')
aa = aggregate(vv$within, list(vv$gr, vv$outside, vv$within), length)
vp = ggplot(aa, aes(x=aa$Group.3, y=aa$Group.2, size=aa$x, shape=aa$Group.1, label=aa$x)) + geom_point() + expand_limits(x=c(0,axlim), y=c(0,axlim)) + scale_x_continuous(minor_breaks=seq(0,axlim,1), breaks=seq(0,axlim,5)) + scale_y_continuous(minor_breaks=seq(0,axlim,1), breaks=seq(0,axlim,5)) + scale_size_continuous(range=c(2,10)) + xlab('Connect within Visual regions') + ylab('Connect to Language Regions') + ggtitle('CB Visual') + theme_bw() + theme(panel.grid.minor = element_line(size=.2, linetype='dashed', color='gray25'), panel.grid.major= element_line(size=.5, color='gray25')) + geom_text(aes(x=aa$Group.3, y=aa$Group.2, label=aa$x, size=5), hjust=1.75, vjust=-1.5)
vp
vv = filter(v_dat, gr=='SCB')
aa = aggregate(vv$within, list(vv$gr, vv$outside, vv$within), length)
vp = ggplot(aa, aes(x=aa$Group.3, y=aa$Group.2, size=aa$x, label=aa$x)) + geom_point(shape=17) + expand_limits(x=c(0,axlim), y=c(0,axlim)) + scale_x_continuous(minor_breaks=seq(0,axlim,1), breaks=seq(0,axlim,5)) + scale_y_continuous(minor_breaks=seq(0,axlim,1), breaks=seq(0,axlim,5)) + scale_size_continuous(range=c(2,10)) + xlab('Connect within Visual regions') + ylab('Connect to Language Regions') + ggtitle('SCB Visual') + theme_bw() + theme(panel.grid.minor = element_line(size=.2, linetype='dashed', color='gray25'), panel.grid.major= element_line(size=.5, color='gray25')) + geom_text(aes(x=aa$Group.3, y=aa$Group.2, label=aa$x, size=5), hjust=1.75, vjust=-1.5)
vp
dev.off()

pdf('Cross_nonLangVis_shared_comms2.pdf')
cbx = filter(x_dat, gr=='CB')
aa = aggregate(cbx$Lang, list(cbx$gr, cbx$Vis, cbx$Lang), length)
xp = ggplot(aa, aes(x=aa$Group.3, y=aa$Group.2, size=aa$x, label=aa$x, shape=aa$Group.1)) + geom_point() + expand_limits(x=c(0,axlim), y=c(0,axlim)) + scale_x_continuous(minor_breaks=seq(0,axlim,1), breaks=seq(0,axlim,5)) + scale_y_continuous(minor_breaks=seq(0,axlim,1), breaks=seq(0,axlim,5)) + scale_size_continuous(range=c(2,10)) + xlab('Connect to Language regions') + ylab('Connect to Visual Regions') + ggtitle('CB Non-Language/Visual Shared communities') + theme_bw() + theme(panel.grid.minor = element_line(size=.2, linetype='dashed', color='gray25'), panel.grid.major= element_line(size=.5, color='gray25')) + geom_text(aes(x=aa$Group.3, y=aa$Group.2, label=aa$x, size=5), hjust=2, vjust=-2)
xp
scbx = filter(x_dat, gr=='SCB')
aa = aggregate(scbx$Lang, list(scbx$gr, scbx$Vis, scbx$Lang), length)
xp = ggplot(aa, aes(x=aa$Group.3, y=aa$Group.2, size=aa$x, label=aa$x)) + geom_point(shape=17) + expand_limits(x=c(0,axlim), y=c(0,axlim)) + scale_x_continuous(minor_breaks=seq(0,axlim,1), breaks=seq(0,axlim,5)) + scale_y_continuous(minor_breaks=seq(0,axlim,1), breaks=seq(0,axlim,5)) + scale_size_continuous(range=c(2,10)) + xlab('Connect to Language regions') + ylab('Connect to Visual Regions') + ggtitle('SCB Non-Language/Visual Shared communities') + theme_bw() + theme(panel.grid.minor = element_line(size=.2, linetype='dashed', color='gray25'), panel.grid.major= element_line(size=.5, color='gray25')) + geom_text(aes(x=aa$Group.3, y=aa$Group.2, label=aa$x, size=5), hjust=2, vjust=-2)
xp
dev.off()



# Below is experimental
vp = ggplot(aa, aes(x=aa$Group.3, y=aa$Group.2, size=aa$x, label=aa$x)) + geom_point(shape=17) + expand_limits(x=c(0,20), y=c(0,20)) + scale_x_continuous(minor_breaks=seq(0,20,1), breaks=seq(0,20,5)) + scale_y_continuous(minor_breaks=seq(0,20,1), breaks=seq(0,20,5)) + scale_size_continuous(range=c(2,10)) + xlab('Connect within Visual regions') + ylab('Connect to Language Regions') + ggtitle('SCB Visual') + theme_bw() + theme(panel.grid.minor = element_line(size=.2, linetype='dashed', color='gray25'), panel.grid.major= element_line(size=.5, color='gray25'))
vp


my.colors <- function(n)
{
    rev(heat.colors(n))
}
hexbinplot(outside ~ within | gr, data=l_dat, xbins = 12
        , panel = function(x,y, ...)
        {
            panel.hexbinplot(x,y,  ...)
        }
        , xlim = c(-1, 21), ylim = c(-1, 21)
        , xlab = "Within"
        , ylab = "Outside"
        , main = "Language"
        #, colramp = my.colors, colorcut = seq(0, 1, length = 10)
)

hexbinplot(Vis ~ Lang | gr, data=x_dat
           , panel = function(x,y, ...)
               {
               panel.hexbinplot(x, y, ...)
           }
           , xlab = 'Language'
           , ylab = 'Visual'
           , main = 'Shared modules'
)


pdf('Cross_hexplots2.pdf')
par(mfcol=c(1,2))
hexbinplot(cb_l_mod$outside_l_cb ~ cb_l_mod$within_l_cb, main='CB Language', xlab='Language Regions', ylab='Visual Regions', xlim=c(-1,20), ylim=c(-1,20))
hexbinplot(scb_l_mod$outside_l_scb ~ scb_l_mod$within_l_scb, main='SCB Language', xlab='Language Regions', ylab='Visual Regions', xlim=c(-1,20), ylim=c(-1,20))
hexbinplot(cb_v_mod$outside_v_cb ~ cb_v_mod$within_v_cb, main='CB Visual', xlab='Visual Regions', ylab='Language Regions', xlim=c(-1,20), ylim=c(-1,20))
hexbinplot(scb_v_mod$outside_v_scb ~ scb_v_mod$within_v_scb, main='SCB Visual', xlab='Visual Regions', ylab='Language Regions', xlim=c(-1,20), ylim=c(-1,20))
dev.off()



plot(hexbin(scb_v_mod$within_v_scb, scb_v_mod$outside_v_scb), main='SCB Visual', xlab='Visual Regions', ylab='Language Regions')
hexbinplot(scb_v_mod$outside_v_scb ~ scb_v_mod$within_v_scb, xlim=c(0,20))

x <- cb_l_mod$within_l_cb
y <- cb_l_mod$outside_l_cb
cols <- colorRampPalette(c("darkorchid4","darkblue","green","yellow", "red"))
plot(hexbin(x, y), colorcut = seq(0,1,length.out=10), colramp = function(n) cols(10))

freqs <- c()
freqs2 <- c()
for (i in cb_l_mod$within_l_cb)
{
    freqs <- c(freqs, length(which(cb_l_mod$within_l_cb==i)))
    freqs2 <- c(freqs2, length(which(cb_l_mod$outside_l_cb==i)))
}
p <- ggplot(cb_l_mod, aes(x=within_l_cb, y=outside_l_cb, size=freqs))+
    geom_point()+
    geom_smooth(method=lm, color="red")+
    theme_bw()
p
p <- ggplot(cb_l_mod, aes(x=within_l_cb, y=outside_l_cb, size=freqs))+
    geom_point()+
    theme_bw()
p

p <- ggplot(l_dat, aes(x=within, y=outside))+
    geom_point()+
    theme_bw()
p

p <- ggplot(l_dat, aes(x=within, y=outside, colour=gr)) + geom_point()
p + scale_size_continuous(range = c(2, 20))
aa = aggregate(l_dat$within, list(l_dat$gr, l_dat$within, l_dat$outside), length)

freqs <- c()
freqs2 <- c()
for (i in l_dat$within)
{
    freqs <- c(freqs, length(which(cb_l_mod$within_l_cb==i)))
    freqs2 <- c(freqs2, length(which(cb_l_mod$outside_l_cb==i)))
}
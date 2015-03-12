# taking quick look at the modularity from hicre data
#---- Reading in modularity values
library(dplyr)
library(pipeR)

groups <- c("CB", "LB", "SCB", "SLB")
densities <- as.factor(seq(.1,.6,.1))
n.1 <- read.csv('N_modules_all_nonSingle_dens0.1.csv')[,2:5]
n.2 <- read.csv('N_modules_all_nonSingle_dens0.2.csv')[,2:5]
n.3 <- read.csv('N_modules_all_nonSingle_dens0.3.csv')[,2:5]
n.4 <- read.csv('N_modules_all_nonSingle_dens0.4.csv')[,2:5]
n.5 <- read.csv('N_modules_all_nonSingle_dens0.5.csv')[,2:5]
n.6 <- read.csv('N_modules_all_nonSingle_dens0.6.csv')[,2:5]
N_each_length <- dim(n.1)[1]*dim(n.2)[2]
Ndf <- tbl_df(data.frame(rbind(stack(n.1), stack(n.2), stack(n.3), stack(n.4), stack(n.5), stack(n.6)), as.factor(rep(seq(.1,.6,.1), each=N_each_length))))
names(Ndf) <- c("Nmod", "group", "dens")
#---- Matrix with MAX N_modules value from the 100 iterations per group
Nall <- tapply(Ndf$Nmod, list(Ndf$dens, Ndf$group), max)
colnames(Nall) <- colnames(N.1)
writeLines('Max N modules values:\n')
print(Nall)
NallSD <- tapply(Ndf$Nmod, list(Ndf$dens, Ndf$group), sd)
writeLines('SD for N modules values:\n')
print(NallSD)


#--- Random Q vals ---------------
rn.1 <- read.csv('rand_N_modules_all_dens0.1.csv')[,2:5]
rn.2 <- read.csv('rand_N_modules_all_dens0.2.csv')[,2:5]
rn.3 <- read.csv('rand_N_modules_all_dens0.3.csv')[,2:5]
rn.4 <- read.csv('rand_N_modules_all_dens0.4.csv')[,2:5]
rn.5 <- read.csv('rand_N_modules_all_dens0.5.csv')[,2:5]
rn.6 <- read.csv('rand_N_modules_all_dens0.6.csv')[,2:5]
rn_each_length <- dim(rn.1)[1]*dim(rn.2)[2]   # intentional that dims from two different frames, will raise problem if they are different dims (because they shouldn't be)
rndf <- tbl_df(data.frame(rbind(stack(rn.1), stack(rn.2), stack(rn.3), stack(rn.4), stack(rn.5), stack(rn.6)), as.factor(rep(seq(.1,.6,.1), each=rn_each_length))))
names(rndf) <- c("rNmod", "group", "dens")
#---- Like above, matrix with MAX modularity value for random nets (with matched degrees)
rNall <- tapply(rndf$rNmod, list(rndf$dens, rndf$group), max)
colnames(rNall) <- colnames(rn.1)
writeLines('Max random iteration modularity values:\n')
print(rNall)
rNallSD <- tapply(rndf$rNmod, list(rndf$dens, rndf$group), sd)
writeLines('SD for random modularity values:\n')
print(rNallSD)


#---- Simple plot of the values
plot(Nall[1,], type="b", pch=19, col=1, ylim=c(min(c(rNall,Nall)),max(c(rNall,Nall))), xaxt="n", lwd=2, xlab="Group", ylab="N modules")
axis(1, at=1:length(groups),labels=colnames(Nall))
lines(rNall[1,], type="o", pch=22, col=1, lty=2, lwd=2)
for (i in 2:dim(Nall)[1])
{
    lines(Nall[i,], type="b", pch=19, col=i, lwd=2)
    lines(rNall[i,], type="o", pch=22, col=i, lty=2, lwd=2)
}
legend("topright", col=c(1:6), pch=16, legend=c(.1, .2, .3, .4, .5, .6))

#----- Q vs. N mods ----------------
#----- group by group instead of across groups, otherwise would jump back and forth
plot(Nall[,1], qall[,1], type="b", pch=19, col=1, ylim=c(min(qall),max(qall)), xlim=c(min(Nall),max(Nall)), lwd=2, xlab="N modules", ylab="Modularity")
#axis(1, at=1:length(densities),labels=densities)
for (i in 2:dim(Nall)[2])
{
    lines(Nall[,i], qall[,i], type="b", pch=19, col=i, lwd=2)
}
legend("topright", col=c(1:4), pch=16, legend=c(colnames(qall)))





pdf("Modularity_value_hists.pdf")
par(mfrow=c(2,2))
for (d in densities)
{
    for (g in groups)
    {
        hist(filter(qdf, dens==d & group==g)$Q, xlab = "modularity values", main=paste(g,' ',d,' density', sep=''))
    }
}
dev.off()

#--- Tests ---
#different than random by density and group
for (d in densities)
{
    for (g in groups)
    {
        print(paste(d,g))
        print(ks.test(filter(Ndf, dens==d & group==g)$Nmod, filter(rndf, dens==d & group==g)$rNmod))
    }
}

#group difference at each density?
for (d in densities)
{
    print(friedman.test(matrix(filter(qdf, dens==d)$Q, nrow =100)))
}

#Do SCB v. CB differ? Do SLB vs. LB differ?
for (d in densities)
{
    writeLines("Difference LB and SLB?")
    print(ks.test(filter(qdf, dens==d & group=='LB')$Q, filter(qdf, dens==d & group=='SLB')$Q))
    writeLines("Difference CB and SCB?")
    print(ks.test(filter(qdf, dens==d & group=='CB')$Q, filter(qdf, dens==d & group=='SCB')$Q))
}

for (i in c(1,2,3,4,5,6))
{
    dat <- get(paste("q.",i,sep=""))
    rnd <- get(paste("rq.",i,sep=""))
    print(wilcox.test(dat$CB,sample(rnd,length(q.1$CB)), alternative="greater"))
    print(wilcox.test(dat$LB,sample(rnd,length(q.1$CB)), alternative="greater"))
    print(wilcox.test(dat$scb,sample(rnd,length(q.1$CB)), alternative="greater"))
    print(wilcox.test(dat$slb,sample(rnd,length(q.1$CB)), alternative="greater"))
}





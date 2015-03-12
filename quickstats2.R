# taking quick look at the modularity from hicre data
#---- Reading in modularity values
library(dplyr)
library(pipeR)

groups <- c("CB", "LB", "SCB", "SLB")
densities <- as.factor(seq(.1,.6,.1))
q.1 <- read.csv('Qscores_all_dens0.1.csv')[,2:5]
q.2 <- read.csv('Qscores_all_dens0.2.csv')[,2:5]
q.3 <- read.csv('Qscores_all_dens0.3.csv')[,2:5]
q.4 <- read.csv('Qscores_all_dens0.4.csv')[,2:5]
q.5 <- read.csv('Qscores_all_dens0.5.csv')[,2:5]
q.6 <- read.csv('Qscores_all_dens0.6.csv')[,2:5]
q_each_length <- dim(q.1)[1]*dim(q.2)[2]
qdf <- tbl_df(data.frame(rbind(stack(q.1), stack(q.2), stack(q.3), stack(q.4), stack(q.5), stack(q.6)), as.factor(rep(seq(.1,.6,.1), each=q_each_length))))
names(qdf) <- c("Q", "group", "dens")
#---- Matrix with MAX modularity value from the 100 iterations per group
qall <- tapply(qdf$Q, list(qdf$dens, qdf$group), max)
colnames(qall) <- colnames(q.1)
writeLines('Max modularity values:\n')
print(qall)
qallSD <- tapply(qdf$Q, list(qdf$dens, qdf$group), sd)
writeLines('SD for modularity values:\n')
print(qallSD)


#--- Random Q vals ---------------
rq.1 <- read.csv('randQscores_dens0.1')[,2:5]
rq.2 <- read.csv('randQscores_dens0.2')[,2:5]
rq.3 <- read.csv('randQscores_dens0.3')[,2:5]
rq.4 <- read.csv('randQscores_dens0.4')[,2:5]
rq.5 <- read.csv('randQscores_dens0.5')[,2:5]
rq.6 <- read.csv('randQscores_dens0.6')[,2:5]
rq_each_length <- dim(rq.1)[1]*dim(rq.2)[2]   # intentional that dims from two different frames, will raise problem if they are different dims (because they shouldn't be)
rqdf <- tbl_df(data.frame(rbind(stack(rq.1), stack(rq.2), stack(rq.3), stack(rq.4), stack(rq.5), stack(rq.6)), as.factor(rep(seq(.1,.6,.1), each=rq_each_length))))
names(rqdf) <- c("rQ", "group", "dens")
#---- Like above, matrix with MAX modularity value for random nets (with matched degrees)
rqall <- tapply(rqdf$rQ, list(rqdf$dens, rqdf$group), max)
colnames(rqall) <- colnames(rq.1)
writeLines('Max random iteration modularity values:\n')
print(rqall)
rqallSD <- tapply(rqdf$rQ, list(rqdf$dens, rqdf$group), sd)
writeLines('SD for random modularity values:\n')
print(rqallSD)


#---- Simple plot of the values
plot(qall[1,], type="b", pch=19, col=1, ylim=c(min(c(rqall,qall)),max(c(rqall,qall))), xaxt="n", lwd=2, xlab="Group", ylab="Modularity value")
axis(1, at=1:length(groups),labels=colnames(qall))
lines(rqall[1,], type="o", pch=22, col=1, lty=2, lwd=2)
for (i in 2:dim(qall)[1])
{
    lines(qall[i,], type="b", pch=19, col=i, lwd=2)
    lines(rqall[i,], type="o", pch=22, col=i, lty=2, lwd=2)
}
legend("topright", col=c(1:6), pch=16, legend=c(.1, .2, .3, .4, .5, .6))

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

ksstats <- c()
ksps <- c()
#--- Tests ---
#different than random by density and group
for (d in densities)
{
    for (g in groups)
    {
        print(paste(d,g))
        #print(ks.test(filter(qdf, dens==d & group==g)$Q, filter(rqdf, dens==d & group==g)$rQ))
        ksOut <- ks.test(filter(qdf, dens==d & group==g)$Q, filter(rqdf, dens==d & group==g)$rQ)
        ksstats <- c(ksstats, ksOut$statistic)
        ksps <- c(ksps, ksOut$p.value)
    }
}
vsrand_ksD <- matrix(ksstats, nrow=length(densities), ncol=length(groups), byrow=T)
vsrand_ksP <- matrix(ksps, nrow=length(densities), ncol=length(groups), byrow=T)
colnames(vsrand_ksD) <- groups
rownames(vsrand_ksD) <- densities
colnames(vsrand_ksP) <-  groups
rownames(vsrand_ksP) <- densities
#group difference at each density?
for (d in densities)
{
    print(friedman.test(matrix(filter(qdf, dens==d)$Q, nrow =100)))
}

#Do SCB v. CB differ? Do SLB vs. LB differ?
ksstats <- c()
ksps <- c()
for (d in densities)
{
    #writeLines(paste("Difference LB and SLB?",d))
    #print(ks.test(filter(qdf, dens==d & group=='LB')$Q, filter(qdf, dens==d & group=='SLB')$Q))
    writeLines(paste("Difference CB and SCB?",d))
    print(ks.test(filter(qdf, dens==d & group=='CB')$Q, filter(qdf, dens==d & group=='SCB')$Q))
    ksout <- ks.test(filter(qdf, dens==d & group=='CB')$Q, filter(qdf, dens==d & group=='SCB')$Q)
    ksstats <- c(ksstats, ksout$statistic)
    ksps <- c(ksps, ksout$p.value)
}
CBvsSCB <- cbind(ksstats, ksps)
colnames(CBvsSCB) <- c("KSstat","KSpvalue")
rownames(CBvsSCB) <- densities

for (i in c(1,2,3,4,5,6))
{
    dat <- get(paste("q.",i,sep=""))
    rnd <- get(paste("rq.",i,sep=""))
    print(wilcox.test(dat$CB,sample(rnd,length(q.1$CB)), alternative="greater"))
    print(wilcox.test(dat$LB,sample(rnd,length(q.1$CB)), alternative="greater"))
    print(wilcox.test(dat$scb,sample(rnd,length(q.1$CB)), alternative="greater"))
    print(wilcox.test(dat$slb,sample(rnd,length(q.1$CB)), alternative="greater"))
}





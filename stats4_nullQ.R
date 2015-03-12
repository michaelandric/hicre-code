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


#--- Null Q vals ---------------
nq.1 <- read.csv('Null_Qscores_maxQ_dens0.1.csv')[,2]
nq.2 <- read.csv('Null_Qscores_maxQ_dens0.2.csv')[,2]
nq.3 <- read.csv('Null_Qscores_maxQ_dens0.3.csv')[,2]
nq.4 <- read.csv('Null_Qscores_maxQ_dens0.4.csv')[,2]
nq.5 <- read.csv('Null_Qscores_maxQ_dens0.5.csv')[,2]
nq.6 <- read.csv('Null_Qscores_maxQ_dens0.6.csv')[,2]
nq_each_length <- length(nq.1)   # intentional that dims from two different frames, will raise problem if they are different dims (because they shouldn't be)
nqdf <- tbl_df(data.frame(c(nq.1, nq.2, nq.3, nq.4, nq.5, nq.6), as.factor(rep(seq(.1,.6,.1), each=nq_each_length))))
names(nqdf) <- c("nQ", "dens")
#---- Like above, matrix with MAX modularity value for random nets (with matched degrees)
nqall <- tapply(nqdf$nQ, list(nqdf$dens), max)
colnames(nqall) <- colnames(nq.1)
writeLines('Max random iteration modularity values:\n')
print(nqall)
nqallSD <- tapply(nqdf$rQ, list(nqdf$dens, nqdf$group), sd)
writeLines('SD for random modularity values:\n')
print(nqallSD)


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

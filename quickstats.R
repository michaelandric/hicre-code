# taking quick look at the modularity from hicre data
#---- Reading in modularity values
library(dplyr)
library(pipeR)

q.1 <- read.csv('Qscores_all_dens0.1.csv')[,2:5]
q.2 <- read.csv('Qscores_all_dens0.2.csv')[,2:5]
q.3 <- read.csv('Qscores_all_dens0.3.csv')[,2:5]
q.4 <- read.csv('Qscores_all_dens0.4.csv')[,2:5]
q.5 <- read.csv('Qscores_all_dens0.5.csv')[,2:5]
q.6 <- read.csv('Qscores_all_dens0.6.csv')[,2:5]
qdf <- tbl_df(data.frame(rbind(stack(q.1), stack(q.2), stack(q.3), stack(q.4), stack(q.5), stack(q.6)), as.factor(rep(seq(.1,.6,.1), each=400))))
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
rqdf <- tbl_df(data.frame(rbind(stack(rq.1), stack(rq.2), stack(rq.3), stack(rq.4), stack(rq.5), stack(rq.6)), as.factor(rep(seq(.1,.6,.1), each=400))))
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
axis(1, at=1:4,labels=colnames(qall))
lines(rqall[1,], type="o", pch=22, col=1, lty=2, lwd=2)
for (i in 2:dim(qall)[1])
{
    lines(qall[i,], type="b", pch=19, col=i, lwd=2)
    lines(rqall[i,], type="o", pch=22, col=i, lty=2, lwd=2)
}
legend("topright", col=c(1:6), pch=16, legend=c(.1, .2, .3, .4, .5, .6))

#--- Tests ---
print(friedman.test(matrix(filter(qdf, dens=='0.1')$Q, nrow =100)))
print(friedman.test(matrix(filter(qdf, dens=='0.2')$Q, nrow =100)))
print(friedman.test(matrix(filter(qdf, dens=='0.3')$Q, nrow =100)))
print(friedman.test(matrix(filter(qdf, dens=='0.4')$Q, nrow =100)))
print(friedman.test(matrix(filter(qdf, dens=='0.5')$Q, nrow =100)))
print(friedman.test(matrix(filter(qdf, dens=='0.6')$Q, nrow =100)))


for (i in c(1,2,3,4,5,6))
{
dat <- get(paste("q.",i,sep=""))
rnd <- get(paste("rq.",i,sep=""))
print(wilcox.test(dat$CB,sample(rnd,length(q.1$CB)), alternative="greater"))
print(wilcox.test(dat$LB,sample(rnd,length(q.1$CB)), alternative="greater"))
print(wilcox.test(dat$scb,sample(rnd,length(q.1$CB)), alternative="greater"))
print(wilcox.test(dat$slb,sample(rnd,length(q.1$CB)), alternative="greater"))
}




